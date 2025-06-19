import http.client
import json
import time

# 配置信息
COOKIE = "看雪cookie" # 替换为你的 看雪cookie
SCKEY = "你的 Server酱 SCKEY"    # 替换为你的 Server酱 SCKEY

def check_COOKIE(cookie):
    if not cookie.strip():
        print('不存在 COOKIE ，请重新检查')
        return False

    pairs = cookie.split(';')
    for pair_str in pairs:
        if '=' not in pair_str:
            print(f'存在不正确的 COOKIE: {pair_str}，请重新检查')
            return False
    return True

def check_in(cookie):
    request_url = "/user-signin.htm"
    conn = http.client.HTTPSConnection('bbs.kanxue.com')

    headers = {
        'User-Agent': 'HD1910(Android/7.1.2) (pediy.UNICFBC0DD/1.0.5) Weex/0.26.0 720x1280',
        'Cookie': cookie,
        'Connection': 'keep-alive',
        'Accept': '*/*'
    }

    try:
        conn.request(method="POST", url=request_url, headers=headers)
        response = conn.getresponse()
        print(f'Status: {response.status}, Reason: {response.reason}')
        content_type = response.getheader('Content-Type')
        print(f'Content-Type: {content_type}')

        res = response.read().decode('utf-8')
        print(f'Response Body: {res}')

        resp = json.loads(res)
        return resp
    except json.JSONDecodeError as e:
        print(f'JSON Decode Error: {e}')
        return None
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

def send_wechat_notification(title, content, sckey=SCKEY):
    if not sckey or sckey == "YOUR_SCKEY":
        print("未配置有效的 SCKEY，跳过微信通知")
        return

    conn = http.client.HTTPSConnection("sc.ftqq.com")
    payload = f"title={title}&desp={content}".encode("utf-8")
    headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}

    try:
        conn.request("POST", f"/{sckey}.send", body=payload, headers=headers)
        response = conn.getresponse()
        result = response.read().decode()
        print("Server酱推送结果：", result)
    except Exception as e:
        print("推送失败:", str(e))

def start(cookie):
    if not check_COOKIE(cookie):
        return

    print('COOKIE检查通过')
    check_in_result = check_in(cookie)

    current_time = time.strftime("【%Y年%m月%d日 %H:%M:%S】", time.localtime())

    if check_in_result and 'code' in check_in_result:
        message = check_in_result['message']
        code = check_in_result['code']

        if code == "0":
            if isinstance(message, int):
                msg = f"{current_time}看雪论坛自动签到成功，获得 {message} 雪币"
            else:
                msg = f"{current_time}看雪论坛自动签到成功"
            print(msg)
            send_wechat_notification("✅ 看雪签到成功", msg)

        elif code == "-1" and message == "您今日已签到成功":
            msg = f"{current_time}您今日已签到成功，无需重复签到！"
            print(msg)
            send_wechat_notification("ℹ️ 看雪签到提醒", msg)

        else:
            msg = f"{current_time}签到失败！原因：{message}"
            print(msg)
            send_wechat_notification("❌ 看雪签到失败", msg)

    else:
        msg = "无法解析签到结果，请检查网络或 COOKIE 是否有效"
        print(msg)
        send_wechat_notification("⚠️ 看雪签到异常", msg)

if __name__ == "__main__":
    start(COOKIE)
