import os
import requests

def sendApi(message):
    url = os.environ["MATTERMOST_WEBHOOK_URL"]
    response = requests.post(url, json={"text": message})
    if response.status_code == 200:
        print("[INFO] 게시 성공!")
    else:
        print("[ERROR] 무언가 오류 발생")
