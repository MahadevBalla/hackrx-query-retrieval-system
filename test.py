import requests

API_URL = "http://127.0.0.1:8000/api/v1/hackrx/run"
BEARER_TOKEN = "696d83a5cdaa28f8d2f8985201e0e79549a9ac52ec8a624359f92411f2fa4022"

payload = {
    "documents": "https://hackrx.blob.core.windows.net/assets/Arogya%20Sanjeevani%20Policy%20-%20CIN%20-%20U10200WB1906GOI001713%201.pdf?sv=2023-01-03&st=2025-07-21T08%3A29%3A02Z&se=2025-09-22T08%3A29%3A00Z&sr=b&sp=r&sig=nzrz1K9Iurt%2BBXom%2FB%2BMPTFMFP3PRnIvEsipAX10Ig4%3D",
    "questions": [
        "What is the sum insured for the Arogya Sanjeevani policy?",
        "Is cataract surgery covered under this policy?",
        "Are AYUSH treatments included?",
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
