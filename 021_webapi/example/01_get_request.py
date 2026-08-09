import requests
import json

# 郵便番号"7830060"で検索する例
# https://zipcloud.ibsnet.co.jp/api/search?zipcode=7830060

# Assign API to variable
url: str = "https://zipcloud.ibsnet.co.jp/api/search"

# Receive the zipcode entered by the user
zip: str = input("Zipcode =>")

# Set the postal code entered by the user as a parameter
param: dict[str, str] = {"zipcode" : zip}

# "HTTP GET" request is sent to the "API", and the response is stored in "res".
res: requests.Response = requests.get(url, param)

# Convert JSON-formatted response data to a dictionary　type
data: dict = json.loads(res.text)

# Output
print(data)

print("*" * 50)

# Extract the necessary information from the response data
if data['results'] is not None:

    address_info = data['results'][0]

    zipcode = address_info['zipcode']

    address = f"{address_info['address1']}{address_info['address2']}{address_info['address3']}"

    print(f"Zipcode : {zipcode} Address : {address}")

else:
    print("No address information was found.")