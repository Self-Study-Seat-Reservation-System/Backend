import requests
from utils.logz import create_logger

class WX:
    APPID = ""
    SECRET = ""
    ACCESS_TOKEN = ""
    logger = create_logger("wx")

    @staticmethod
    def get_openid(code):
        url = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            "appid": WX.APPID,
            "secret": WX.SECRET,
            "js_code": code,
            "grant_type": "authorization_code"
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            return "wx server error"
        
        errcode =  response.json().get("errcode")
        match errcode:
            case 40029:
                error_msg = "Invalid code"
            case 45011:
                error_msg = "Frequent request"
            case 40226:
                error_msg = "code blocked"
            case -1:
                error_msg = "system error"
            case 0:
                return response.json()
        
        WX.logger.error(f"Error getting openid: {error_msg}")
        return error_msg
    
    @staticmethod
    def send_subscribe(message):
        url = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send"
        params = {
            "access_token": WX.ACCESS_TOKEN
        }

        response = requests.post(url, params=params, json=message)
    
    @staticmethod
    def update_access_token():
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": WX.APPID,
            "secret": WX.SECRET
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            return "wx server error"
        
        WX.ACCESS_TOKEN = response.json().get("access_token")
        return WX.ACCESS_TOKEN