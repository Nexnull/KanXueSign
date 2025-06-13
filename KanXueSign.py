import http.client
import json
import time

COOKIE = "YOURCOOKIE"  

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
    request_url = "https://bbs.kanxue.com/user-signin.htm"
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

def start(cookie):
    if not check_COOKIE(cookie):
        return

    print('COOKIE检查通过')
    check_in_result = check_in(cookie)

    if check_in_result and 'code' in check_in_result:
        message = check_in_result['message']
        code = check_in_result['code']

        current_time = time.strftime("【%Y年%m月%d日 %H:%M:%S】", time.localtime())

        if code == "0":
            if isinstance(message, int):
                msg = f"{current_time}看雪论坛自动签到成功，获得 {message} 雪币"
            else:
                msg = f"{current_time}看雪论坛自动签到成功"
            print(msg)
        elif code == "-1" and message == "您今日已签到成功":
            msg = f"{current_time}您今日已签到成功，无需重复签到！"
            print(msg)
        else:
            msg = f"{current_time}签到失败！原因：{message}"
            print(msg)
    else:
        print('无法解析签到结果')

if __name__ == "__main__":
    start(COOKIE)


