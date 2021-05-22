import requests
  
URL = "http://localhost:9090/user"

r = requests.post(url = URL)

pastebin_url = r.text
print("The content is: %s"%pastebin_url)