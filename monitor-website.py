import requests

response = requests.get("http://172-104-226-116.ip.linodeusercontent.com:8080")

if response.status_code == 200:
    print("Application is running")
else:
    print("Application Down. Fix it")
