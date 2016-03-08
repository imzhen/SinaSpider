import requests
import json
import base64


class WeiboLogin:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        username = base64.b64encode(self.username.encode('utf-8')).decode('utf-8')
        post_data = {
            "entry": "sso",
            "gateway": "1",
            "from": "null",
            "savestate": "30",
            "useticket": "0",
            "pagerefer": "",
            "vsnf": "1",
            "su": username,
            "service": "sso",
            "sp": self.password,
            "sr": "1440*900",
            "encoding": "UTF-8",
            "cdult": "3",
            "domain": "sina.com.cn",
            "prelt": "0",
            "returntype": "TEXT",
        }
        login_url = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
        session = requests.Session()
        res = session.post(login_url, data=post_data)
        json_str = res.content.decode('gbk')
        info = json.loads(json_str)
        if info["retcode"] == "0":
            print("login successfully")
            # add cookie to header, it is essential
            cookies = session.cookies.get_dict()
            cookies = [key + "=" + value for key, value in cookies.items()]
            cookies = "; ".join(cookies)
            session.headers["cookie"] = cookies
        else:
            print("login unsuccessfully： %s" % info["reason"])
        return session
