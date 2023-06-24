from datetime import datetime
import time

current_time = datetime.now().time() #hour(시간) ,minute(분)
week_day = datetime.today().weekday() #월(0), 화(1) ~ 일(6)

print(current_time.minute)
print(week_day)

while(True):
    current_time = datetime.now().time() #hour(시간), miute(분)
    week_day = datetime.today().weekday() #월(0), 화(1) ~ 일(6)
    
    if week_day != 6:
        if current_time.minute == 28:
            print("sms 보내기")
    time.sleep(60)
    
#sms
import hmac, hashlib, base64
import time, requests, json

def make_signature(secret_key, access_key, timestamp, uri):
    secret_key = bytes(secret_key, 'UTF-8')
    method = "POST"
    message = method + " "  + uri + "\\n" + timestamp + "\\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey

access_key = ""
secret_key = ""

# <https://api.ncloud-docs.com/docs/ko/ai-application-service-sens-smsv2>
url = "<https://sens.apigw.ntruss.com>"
uri = f"/sms/v2/services/{service_key}/messages"

timestamp = int(time.time() * 1000)
timestamp = str(timestamp)

# 받는 상대방
number = "01000000000"

# message 내용
contents = "조명이 켜집니다."

header = {
    "Content-Type": "application/json; charset=utf-8",
    "x-ncp-apigw-timestamp": timestamp,
    "x-ncp-iam-access-key": access_key,
    "x-ncp-apigw-signature-v2": make_signature(secret_key, access_key, timestamp, uri)
}

# from : SMS 인증한 사용자만 가능
data = {
    "type":"SMS",
    "from":"01000000000",
    "content":contents,
    "subject":"SENS",
    "messages":[
        {
            "to":number,
        }
    ]
}

res = requests.post(url+uri,headers=header,data=json.dumps(data))
datas = json.loads(res.text)
reid = datas['requestId']

print("메시지 전송 상태")
print(res.text+"\\n")