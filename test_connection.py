import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

bank_id = os.getenv("BANK_ID")

print("BANK:", bank_id)
print("\nTesting Hindsight RETAIN...")

client.retain(
    bank_id=bank_id,
    content="AcmeCorp uses Debian 12 with PostgreSQL 16 on port 5432."
)

print("✅ Retain successful!")

print("\nTesting Hindsight RECALL...")

result = client.recall(
    bank_id=bank_id,
    query="What operating system and database does AcmeCorp use?"
)

print("\n--- HINDSIGHT RECALL RESULT ---")

for memory in result.results:
    print(memory.text)

print("\n✅ Hindsight connection test completed!")