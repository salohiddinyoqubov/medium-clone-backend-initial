import requests

url = "http://127.0.0.1:8000/articles/"
data = {
    "title": "Test Article",
    "summary": "2323",
    "content": "213123",
    "topic_ids": [1, 2]
}
files = {
    "thumbnail": requests.get("https://storage.kun.uz/source/10/s7RZIX7vJSbjA5rF7gicmU5yHMem7OS2.jpg", stream=True).raw
}

print(files)
response = requests.post(url, data=data, files=files)
print(response.status_code)
print(response.json())
