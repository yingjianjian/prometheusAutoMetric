import requests
def isciasStatus(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    try:
        response  = requests.get(url,headers=headers)
        return response.status_code
    except:
        return 500

