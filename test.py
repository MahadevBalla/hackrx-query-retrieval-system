import requests

API_URL = "http://127.0.0.1:8000/api/v1/hackrx/run"
BEARER_TOKEN = "696d83a5cdaa28f8d2f8985201e0e79549a9ac52ec8a624359f92411f2fa4022"

payload = {
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?",
        "Does this policy cover maternity expenses, and what are the conditions?",
        "What is the waiting period for cataract surgery?",
        "Are the medical expenses for an organ donor covered under this policy?",
        "What is the No Claim Discount (NCD) offered in this policy?",
        "Is there a benefit for preventive health check-ups?",
        "How does the policy define a 'Hospital'?",
        "What is the extent of coverage for AYUSH treatments?",
        "Are there any sub-limits on room rent and ICU charges for Plan A?",
    ],
}

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

try:
    response = requests.post(API_URL, json=payload, headers=headers)

    if response.ok:
        print("\nAPI responded successfully!")
        print("Answers:\n")
        for idx, answer in enumerate(response.json().get("answers", []), 1):
            print(f"{idx}. {answer}")
    else:
        print("\nAPI request failed!")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
except Exception as e:
    print("\n Request crashed!")
    print("Error:", str(e))
