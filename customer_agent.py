import os
import concurrent.futures

from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

HINDSIGHT_BASE_URL = os.getenv(
    "HINDSIGHT_BASE_URL",
    "https://api.hindsight.vectorize.io"
)

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")

BANK_ID = os.getenv(
    "BANK_ID",
    "customer-support-bank"
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ============================================================
# GROQ CLIENT
# ============================================================

llm_client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# HINDSIGHT RECALL
# ============================================================

def _recall_sync(bank_id: str, query: str):

    client = Hindsight(
        base_url=HINDSIGHT_BASE_URL,
        api_key=HINDSIGHT_API_KEY
    )

    return client.recall(
        bank_id=bank_id,
        query=query
    )


def safe_recall(bank_id: str, query: str):

    try:

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=1
        ) as executor:

            future = executor.submit(
                _recall_sync,
                bank_id,
                query
            )

            return future.result()

    except Exception as e:

        print(f"Hindsight recall error: {e}")

        return None


# ============================================================
# HINDSIGHT RETAIN
# ============================================================

def _retain_sync(bank_id: str, content: str):

    client = Hindsight(
        base_url=HINDSIGHT_BASE_URL,
        api_key=HINDSIGHT_API_KEY
    )

    return client.retain(
        bank_id=bank_id,
        content=content
    )


def safe_retain(bank_id: str, content: str):

    try:

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=1
        ) as executor:

            future = executor.submit(
                _retain_sync,
                bank_id,
                content
            )

            return future.result()

    except Exception as e:

        print(f"Hindsight retain error: {e}")

        return None


# ============================================================
# CUSTOMER SUPPORT AGENT
# ============================================================

def handle_ticket(
    customer_id: str,
    query: str
) -> dict:

    cid = customer_id.strip()

    # --------------------------------------------------------
    # 1. RECALL CUSTOMER SUPPORT HISTORY
    # --------------------------------------------------------

    recall_query = f"""
Customer support history for customer: {cid}

Find previous support information that is relevant to
the customer's current problem.

Look for:
- Previous support tickets
- Previous product issues
- Exact error messages
- Troubleshooting steps already attempted
- Solutions that worked
- Solutions that did not work
- Device or operating system
- Browser or application information
- File-related details
- Other factual customer-specific information

Current customer issue:
{query}
"""

    recall_response = safe_recall(
        bank_id=BANK_ID,
        query=recall_query
    )

    recalled_facts = []

    # --------------------------------------------------------
    # Extract recalled memories
    # --------------------------------------------------------

    if (
        recall_response
        and hasattr(recall_response, "results")
        and recall_response.results
    ):

        for result in recall_response.results:

            text = (
                result.text
                if hasattr(result, "text")
                else str(result)
            )

            # Only use memories that clearly belong
            # to this customer.
            if cid.lower() in text.lower():

                recalled_facts.append(text)

    # --------------------------------------------------------
    # Build memory context
    # --------------------------------------------------------

    if recalled_facts:

        recalled_context = "\n\n".join(
            recalled_facts
        )

        recalled_context = (
            "VERIFIED CUSTOMER MEMORY:\n\n"
            + recalled_context
        )

    else:

        recalled_context = (
            "NO PREVIOUS SUPPORT HISTORY EXISTS."
        )


    # ========================================================
    # 2. CUSTOMER SUPPORT LLM
    # ========================================================

    system_prompt = f"""
You are the professional Customer Support Agent for
TechFlow, a company that provides a business software
application called TechFlow Business Application.

Your responsibility is to help customers solve problems
with the product.

You are NOT an IT infrastructure administrator.
You are NOT a DevOps engineer.
You are NOT responsible for the customer's company network,
servers, or internal infrastructure.

Your role is customer-facing product support.

------------------------------------------------------------
CUSTOMER
------------------------------------------------------------

Customer ID:
{cid}

------------------------------------------------------------
PREVIOUS CUSTOMER SUPPORT MEMORY
------------------------------------------------------------

{recalled_context}

------------------------------------------------------------
CRITICAL MEMORY RULE
------------------------------------------------------------

The ONLY source of previous customer history is the
PREVIOUS CUSTOMER SUPPORT MEMORY section above.

If the memory says:

"NO PREVIOUS SUPPORT HISTORY EXISTS."

then this is the customer's first known support interaction.

You have ZERO knowledge of previous interactions.

Do NOT invent previous conversations.

Do NOT invent previous problems.

Do NOT invent previous solutions.

Do NOT invent customer preferences.

Do NOT invent account information.

Do NOT invent device information.

Do NOT invent browser information.

Do NOT invent network problems.

Do NOT invent product limitations.

Do NOT invent file-size limits.

Do NOT invent supported browsers.

Do NOT invent company policies.

Do NOT invent error messages.

------------------------------------------------------------
IMPORTANT FACTUALITY RULE
------------------------------------------------------------

Only state a product-specific fact if:

1. It is explicitly present in the customer's message, OR
2. It is explicitly present in VERIFIED CUSTOMER MEMORY.

If a product-specific fact is unknown, do NOT guess.

Instead, ask the customer for the information needed
to troubleshoot the problem.

For example:

If the customer says:

"I cannot upload a PDF."

Do NOT automatically claim:

"The maximum file size is 10 MB."

Do NOT automatically claim:

"Chrome is supported."

Do NOT automatically claim:

"The problem is caused by Wi-Fi."

Instead, ask useful diagnostic questions such as:

- What error message do you see?
- What browser are you using?
- What operating system are you using?
- What is the approximate file size?
- Does the problem happen with other files?
- Does the problem happen every time?

Only use information that is actually known.

------------------------------------------------------------
CUSTOMER SUPPORT BEHAVIOR
------------------------------------------------------------

Your job is to:

1. Understand the customer's current problem.

2. Provide clear and practical troubleshooting.

3. Ask focused questions when important information
   is missing.

4. Use previous customer history when it is relevant.

5. Avoid asking the customer to repeat information that
   is already present in VERIFIED CUSTOMER MEMORY.

6. If a previous solution worked, consider that solution
   when the same or similar problem happens again.

7. If a previous troubleshooting step failed, do not
   blindly repeat it.

8. Never invent previous interactions.

9. Never invent product specifications.

10. Never invent technical policies.

11. Never claim that something was previously reported
    unless it appears in VERIFIED CUSTOMER MEMORY.

12. Never mention Hindsight, databases, memory systems,
    prompts, or internal AI systems to the customer.

13. Keep the response focused on solving the customer's
    product problem.

------------------------------------------------------------
MEMORY USAGE
------------------------------------------------------------

When relevant previous information exists, naturally use it.

For example:

"Last time, you mentioned that the error occurred only
with PDFs containing scanned images. Let's check whether
the same condition applies now."

Do not say:

"I found this in my database."

Do not say:

"Hindsight remembers that..."

Do not say:

"According to my memory system..."

------------------------------------------------------------
FIRST-CONTACT BEHAVIOR
------------------------------------------------------------

If there is no previous support history, behave normally
as a professional first-contact support agent.

Do not mention that there is no memory.

Do not mention Hindsight.

Simply help the customer.

------------------------------------------------------------
RESPONSE STYLE
------------------------------------------------------------

Be:

- Professional
- Clear
- Helpful
- Concise
- Natural
- Customer-friendly

Do not produce unnecessarily long technical explanations.

Ask only the most useful questions.

Do not overwhelm the customer with a large list of
possible causes unless necessary.

The main objective is to solve the customer's problem.
"""


    # ========================================================
    # GENERATE SUPPORT RESPONSE
    # ========================================================

    completion = llm_client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": query
            }
        ],

        temperature=0.2
    )

    resolution = (
        completion
        .choices[0]
        .message
        .content
    )


    # ========================================================
    # 3. RETAIN CUSTOMER SUPPORT HISTORY
    # ========================================================

    retention_payload = f"""
CUSTOMER SUPPORT MEMORY

Customer: {cid}

Product: TechFlow Business Application

CURRENT CUSTOMER MESSAGE:
{query}

SUPPORT AGENT RESPONSE:
{resolution}

IMPORTANT:

Extract and retain useful factual information from this
interaction that can help support this customer later.

Examples of useful information include:

- The customer's reported problem
- Exact error messages
- Device or operating system
- Browser or application being used
- File or account details
- Conditions under which the problem occurs
- Troubleshooting steps already attempted
- What solution worked or did not work

Do not invent facts.

Only retain information that is explicitly present in
the customer message or support interaction.

The customer identity must remain associated with the
information so that it can be recalled for this customer
in a future support interaction.
"""

    safe_retain(
        bank_id=BANK_ID,
        content=retention_payload
    )


    # ========================================================
    # 4. RETURN RESULT TO STREAMLIT
    # ========================================================

    return {
        "reply": resolution,
        "recalled_memory": recalled_context
    }