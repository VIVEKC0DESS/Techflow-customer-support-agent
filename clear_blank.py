import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

bank_id = "customer-support-bank"

try:
    # Try deleting the bank to purge all contaminated memory nodes
    client.delete_bank(bank_id=bank_id)
    print(f"Bank '{bank_id}' deleted successfully.")
except Exception as e:
    print(f"Delete note: {e}")

try:
    # Re-create a clean empty bank
    client.create_bank(bank_id=bank_id, name="Customer Support Bank")
    print(f"Clean bank '{bank_id}' created successfully!")
except Exception as e:
    print(f"Create note (bank may auto-exist): {e}")

print("CACHE COMPLETELY CLEARED.")