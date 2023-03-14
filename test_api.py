import requests

url = "http://localhost:8082/collections/landsat-c2l1/items/LC09_L1GT_019032_20211031_20220118_02_T2/update-item-cids"
headers = {
    "Content-Type": "application/json",
}
payload = {
    "id": "LC09_L1GT_019032_20211031_20220118_02_T2",
    "assets": {
        "coastal": {
            "alternate": {"IPFS": "QmRtciFJLQNrTq3vDnTbNVCzR9JyX9nHKsddC6sW8zUvcZ"}
        }
    },
}

response = requests.put(url, headers=headers, json=payload)

print(response.status_code)
print(response.text)
