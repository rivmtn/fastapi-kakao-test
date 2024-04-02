import os

from dotenv import load_dotenv

load_dotenv()

AUTHORIZE_URL = "https://kauth.kakao.com/oauth/authorize"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET_KEY = os.getenv("CLIENT_SECRET_KEY")
SERVER_URL = os.getenv("SERVER_URL")
REDIRECT_URI = SERVER_URL + "/authorize"
RESPONSE_TYPE = "code"
TOKEN_URL = "https://kauth.kakao.com/oauth/token"
GRANT_TYPE = "authorization_code"
REFRESH_URL = "https://kauth.kakao.com/oauth/token"
REFRESH_GRANT_TYPE = "refresh_token"
ACCESS_TOKEN_INFO_URL = "https://kapi.kakao.com/v1/user/access_token_info"
USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"
LOGOUT_URL = "https://kapi.kakao.com/v1/user/logout"
TARGET_ID_TYPE = "user_id"

