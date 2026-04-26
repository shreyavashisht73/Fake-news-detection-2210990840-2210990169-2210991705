import requests
import pandas as pd

API_KEY = "53946c31a306a067aea76b83b701b5e3"

url = f"http://api.mediastack.com/v1/news?access_key={API_KEY}&languages=en&limit=10"

response = requests.get(url)
data = response.json()

rows = []

for item in data["data"]:
    title = item["title"]
    rows.append([title, "REAL"])

df = pd.DataFrame(rows, columns=["text", "label"])

old = pd.read_csv("dataset.csv")

new = pd.concat([old, df], ignore_index=True)

new.to_csv("dataset.csv", index=False)

print("New news added successfully!")