import base64
import json
import requests

# Target URL
BASE_URL = "https://web.cryptohack.org/no-way-jose"

# Step 1: Create the JWT header
header = {"typ": "JWT", "alg": "none"}
header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")

# Step 2: Create the JWT payload
payload = {"admin": True}
payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")

# Step 3: Construct the token
# No signature is added for the "none" algorithm
token = f"{header_b64}.{payload_b64}."

# Step 4: Send the crafted token
url = f"{BASE_URL}/authorise/{token}/"
response = requests.get(url)

# Step 5: Display the response
print(response.text)

