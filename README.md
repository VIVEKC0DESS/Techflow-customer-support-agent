# TechFlow Customer Support Agent

An AI-powered customer support agent for TechFlow that uses persistent memory to remember customer support history across conversations.

## Overview

TechFlow Customer Support Agent helps customers troubleshoot problems with the TechFlow business application without requiring them to repeatedly explain their previous support history.

The agent uses **Hindsight** as its persistent memory layer. It can recall useful information from previous support interactions and use that context when the same customer returns later.

## Problem

Traditional AI support chatbots often treat each conversation as a new interaction.

When a customer returns with the same or related issue, they may have to repeat:

- What problem they experienced
- Error messages they received
- Their environment or setup
- What troubleshooting was already attempted
- Which information was relevant to the previous resolution

This creates unnecessary repetition and makes support interactions less continuous.

## Solution

TechFlow Customer Support Agent maintains persistent customer-specific support memory.

The workflow is:

1. Customer reports an issue.
2. The agent checks the customer's previous support history.
3. Relevant information is used to understand the current issue.
4. The agent provides troubleshooting guidance.
5. Useful support information is retained in Hindsight.
6. When the customer returns later, the agent can recall the previous context.

This allows the support interaction to continue with context instead of starting from zero.

## Why Persistent Memory Matters

The main feature of this project is not simply generating an AI response.

The important part is that the agent can **remember customer-specific support history across separate sessions**.

For example:

### First interaction

A customer reports:

> I can't upload PDF invoices to the application. It keeps giving me an error.

The customer later provides additional information:

- Error: `Upload failed`
- Browser: Chrome
- Operating system: Windows
- PDF size: 2 MB
- Issue occurs with PDFs containing scanned images

The useful information is retained as customer support memory.

### Returning customer

The chat session can then be cleared.

When the same customer returns and says:

> I'm having the PDF upload problem again.

The agent can recall the relevant support history and continue the conversation with that context.

The customer does not need to repeat the complete history.

## How Hindsight Is Used

Hindsight provides the persistent memory layer for the customer support agent.

The application uses two important memory operations:

### Recall

Before generating a response, the agent retrieves relevant memories associated with the customer.

The recalled information is then provided to the AI model as verified customer history.

### Retain

After a support interaction, useful information from the interaction is stored in Hindsight so it can be recalled during future support sessions.

### Memory Flow

```text
Customer Message
       |
       v
Customer ID
       |
       v
Hindsight Recall
       |
       v
Relevant Customer History
       |
       v
AI Support Agent
       |
       v
Support Response
       |
       v
Hindsight Retain

## Architecture

                 +----------------------+
                 |      Customer        |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |   Streamlit UI       |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 | Customer Support     |
                 | Agent                |
                 +----+------------+----+
                      |            |
             Recall   |            |  Retain
                      v            v
              +--------------------------+
              |        Hindsight         |
              |   Persistent Memory      |
              +--------------------------+
                      |
                      v
              Customer Support History

                 Agent
                   |
                   v
              Groq LLM
                   |
                   v
            Support Response
 ## Key Features

- AI-powered customer support
- Customer-specific persistent memory
- Cross-session support history
- Hindsight recall and retention
- Customer ID based memory retrieval
- Streamlit chat interface
- Groq-powered language model
- Environment-variable based API key management
- Memory inspection for demonstrating recalled customer history

## Demo Scenario

The main demonstration uses a fictional customer called `AcmeCorp`.

### Step 1 — First Support Session

Customer reports a PDF invoice upload problem.

The agent asks for relevant troubleshooting information.

### Step 2 — Customer Provides Details

The customer explains:

- The error message
- Browser
- Operating system
- PDF size
- Type of PDF causing the problem

### Step 3 — Memory Retention

Useful support information is retained in Hindsight.

### Step 4 — Clear the Chat

The current Streamlit chat session is cleared.

This does **not** delete the customer's persistent Hindsight memory.

### Step 5 — Returning Customer

The customer reports the same problem again.

### Step 6 — Memory Recall

Hindsight retrieves relevant customer history and the agent continues the support conversation with that context.

## Before vs After Persistent Memory

### Without Persistent Memory

```text
Customer returns
      |
      v
New conversation
      |
      v
"Please explain the problem again."

### With Hindsight

```text
Customer returns
      |
      v
Hindsight recalls history
      |
      v
Agent understands previous context
      |
      v
Continue troubleshooting

## Tech Stack

- Python
- Streamlit
- Groq
- Hindsight
- python-dotenv

## Project Structure

```text
techflow-customer-support-agent/
│
├── app.py
├── customer_agent.py
├── clear_blank.py
├── test_connection.py
├── requirements.txt
├── .gitignore
├── .env
└── README.md

> `.env` contains private API credentials and is excluded from Git using `.gitignore`.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/VIVEKC0DESS/Techflow-customer-support-agent.git
cd Techflow-customer-support-agent

### 2. Create a virtual environment

```bash
python -m venv venv

### 3. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate

### 4. Install dependencies

```bash
pip install -r requirements.txt

## Environment Variables

Create a `.env` file in the project root:

```env
HINDSIGHT_API_KEY=your_hindsight_api_key
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
GROQ_API_KEY=your_groq_api_key
BANK_ID=customer-support-bank

## Running the Application

Start the Streamlit application with:

```bash
streamlit run app.py

## Hindsight Memory Flow

1. Customer reports a problem.
2. The agent recalls relevant customer history from Hindsight.
3. The agent provides support using the available context.
4. Useful support information is retained in Hindsight.
5. When the customer returns, the agent recalls the previous history.
6. The customer does not need to repeat the same information.

## Limitations

This project is a prototype demonstrating persistent customer support memory.

Current limitations include:

- The support knowledge is limited to the application's available context.
- Troubleshooting guidance is generated by an AI model and should be validated for production use.
- The demonstration uses a fictional TechFlow business application.
- Customer identity is represented using a customer ID rather than a full production authentication system.
- Production deployment would require additional security, monitoring, authentication, access control, and evaluation.

## Future Improvements

Potential future improvements include:

- More structured customer memory
- Better memory filtering and relevance ranking
- Support ticket history integration
- Knowledge-base integration
- Human support escalation
- Authentication and role-based access
- Support analytics dashboard
- Automated evaluation of support responses
- Production monitoring and observability

## Team

This project was developed by a team of six members as an AI customer support project demonstrating persistent memory with Hindsight.

### Team Members

- TEJOPRANAV Daruri
- Vivek Vattipalli
- Shiva ganesh Ramasani
- Aakash varma Dandu
- Raghavendra Keshaboina
- Ram charan Goda

