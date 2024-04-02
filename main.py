import base64
import os
from datetime import datetime
from typing import Optional, Callable

import requests
from fastapi import FastAPI, Form
from pytz import timezone
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from config import CLIENT_ID, CLIENT_SECRET_KEY, REDIRECT_URI, TOKEN_URL, GRANT_TYPE, \
    SERVER_URL, ACCESS_TOKEN_INFO_URL, LOGOUT_URL, TARGET_ID_TYPE, RESPONSE_TYPE, \
    AUTHORIZE_URL, REFRESH_URL, REFRESH_GRANT_TYPE, USER_INFO_URL

app = FastAPI()
templates = Jinja2Templates(directory="templates/")


def base64url_decode(input_str):
    # Base64Url로 인코딩된 문자열을 표준 Base64로 변환
    rem = len(input_str) % 4
    if rem > 0:
        input_str += '=' * (4 - rem)
    return base64.urlsafe_b64decode(input_str)


current_time: Callable[[], str] = lambda: datetime.now(timezone('Asia/Seoul')).strftime("%Y%m%d%H%M%S")


@app.get(path="/")
async def root():
    return RedirectResponse(
        url=f"{AUTHORIZE_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type={RESPONSE_TYPE}",
    )


@app.get(path="/authorize")
async def _(request: Request,
            code: Optional[str] = None,
            error: Optional[str] = None,
            error_description: Optional[str] = None,
            state: Optional[str] = None, ):
    return templates.TemplateResponse(
        name="authorize.html",
        context=dict(
            request=request,
            code=code,  # 토큰 받기 요청에 필요한 인가 코드
            error=error,  # 인증 실패 시 반환되는 에러 코드
            error_description=error_description,  # 인증 실패 시 반환되는 에러 메시지
            state=state,  # 요청 시 전달한 state 값과 동일한 값

            SERVER_URL=SERVER_URL,
        )
    )


@app.post(path="/token")
def _(request: Request,
      code: str = Form(...), ):
    response = requests.post(
        url=TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"},
        data=dict(
            grant_type=GRANT_TYPE,
            client_id=CLIENT_ID,
            redirect_uri=REDIRECT_URI,
            code=code,
            client_secret=CLIENT_SECRET_KEY,
        )
    )

    json = response.json()
    token_type = json.get("token_type")
    access_token = json.get("access_token")
    id_token = json.get("id_token")
    expires_in = json.get("expires_in")
    refresh_token = json.get("refresh_token")
    refresh_token_expires_in = json.get("refresh_token_expires_in")

    return templates.TemplateResponse(
        name="token.html",
        context=dict(
            request=request,
            token_type=token_type,
            access_token=access_token,
            id_token=id_token,
            expires_in=expires_in,
            refresh_token=refresh_token,
            refresh_token_expires_in=refresh_token_expires_in,

            SERVER_URL=SERVER_URL,
        )
    )


@app.post(path="/refresh")
def _(request: Request,
      refresh_token: str = Form(...), ):
    response = requests.post(
        url=REFRESH_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"},
        data=dict(
            grant_type=REFRESH_GRANT_TYPE,
            client_id=CLIENT_ID,
            refresh_token=refresh_token,
            client_secret=CLIENT_SECRET_KEY,
        )
    )

    json = response.json()
    token_type = json.get("token_type")
    access_token = json.get("access_token")
    id_token = json.get("id_token")
    expires_in = json.get("expires_in")
    refresh_token = json.get("refresh_token")
    refresh_token_expires_in = json.get("refresh_token_expires_in")

    return templates.TemplateResponse(
        name="token.html",
        context=dict(
            request=request,
            token_type=token_type,
            access_token=access_token,
            id_token=id_token,
            expires_in=expires_in,
            refresh_token=refresh_token,
            refresh_token_expires_in=refresh_token_expires_in,

            SERVER_URL=SERVER_URL,
        )
    )


@app.post(path="/access_token_info")
def _(request: Request,
      access_token: str = Form(...), ):
    response = requests.get(
        url=ACCESS_TOKEN_INFO_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                 "Authorization": f"Bearer {access_token}", },
    )

    json = response.json()
    id = json.get("id")
    expires_in = json.get("expires_in")
    app_id = json.get("app_id")

    return templates.TemplateResponse(
        name="access_token_info.html",
        context=dict(
            request=request,
            id=id,
            expires_in=expires_in,
            app_id=app_id,

            SERVER_URL=SERVER_URL,
            access_token=access_token,
        )
    )


@app.post(path="/user_info")
def _(request: Request,
      access_token: str = Form(...), ):
    response = requests.get(
        url=USER_INFO_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                 "Authorization": f"Bearer {access_token}", },
    )

    json = response.json()
    id = json.get("id")
    has_signed_up = json.get("has_signed_up")
    connected_at = json.get("connected_at")
    synched_at = json.get("synched_at")
    properties = json.get("properties")
    nickname = properties.get("nickname")
    profile_image = properties.get("profile_image")
    thumbnail_image = properties.get("thumbnail_image")
    kakao_account = json.get("kakao_account")
    profile_needs_agreement = kakao_account.get("profile_needs_agreement")
    profile_nickname_needs_agreement = kakao_account.get("profile_nickname_needs_agreement")
    profile_image_needs_agreement = kakao_account.get("profile_image_needs_agreement")
    profile = kakao_account.get("profile")
    nickname = profile.get("nickname")
    thumbnail_image_url = profile.get("thumbnail_image_url")
    profile_image_url = profile.get("profile_image_url")
    is_default_image = profile.get("is_default_image")
    name_needs_agreement = kakao_account.get("name_needs_agreement")
    name = kakao_account.get("name")
    email_needs_agreement = kakao_account.get("email_needs_agreement")
    is_email_valid = kakao_account.get("is_email_valid")
    is_email_verified = kakao_account.get("is_email_verified")
    email = kakao_account.get("email")
    age_range_needs_agreement = kakao_account.get("age_range_needs_agreement")
    age_range = kakao_account.get("age_range")
    birthyear_needs_agreement = kakao_account.get("birthyear_needs_agreement")
    birthyear = kakao_account.get("birthyear")
    birthday_needs_agreement = kakao_account.get("birthday_needs_agreement")
    birthday = kakao_account.get("birthday")
    birthday_type = kakao_account.get("birthday_type")
    gender_needs_agreement = kakao_account.get("gender_needs_agreement")
    gender = kakao_account.get("gender")
    phone_number_needs_agreement = kakao_account.get("phone_number_needs_agreement")
    phone_number = kakao_account.get("phone_number")
    ci_needs_agreement = kakao_account.get("ci_needs_agreement")
    ci = kakao_account.get("ci")
    ci_authenticated_at = kakao_account.get("ci_authenticated_at")
    for_partner = json.get("for_partner")
    # uuid = for_partner.get("uuid")

    return templates.TemplateResponse(
        name="user_info.html",
        context=dict(
            request=request,

            id=id,
            has_signed_up=has_signed_up,
            connected_at=connected_at,
            synched_at=synched_at,
            properties=properties,
            nickname=nickname,
            profile_image=profile_image,
            thumbnail_image=thumbnail_image,
            kakao_account=kakao_account,
            profile_needs_agreement=profile_needs_agreement,
            profile_nickname_needs_agreement=profile_nickname_needs_agreement,
            profile_image_needs_agreement=profile_image_needs_agreement,
            profile=profile,
            thumbnail_image_url=thumbnail_image_url,
            profile_image_url=profile_image_url,
            is_default_image=is_default_image,
            name_needs_agreement=name_needs_agreement,
            user_name=name,
            email_needs_agreement=email_needs_agreement,
            is_email_valid=is_email_valid,
            is_email_verified=is_email_verified,
            email=email,
            age_range_needs_agreement=age_range_needs_agreement,
            age_range=age_range,
            birthyear_needs_agreement=birthyear_needs_agreement,
            birthyear=birthyear,
            birthday_needs_agreement=birthday_needs_agreement,
            birthday=birthday,
            birthday_type=birthday_type,
            gender_needs_agreement=gender_needs_agreement,
            gender=gender,
            phone_number_needs_agreement=phone_number_needs_agreement,
            phone_number=phone_number,
            ci_needs_agreement=ci_needs_agreement,
            ci=ci,
            ci_authenticated_at=ci_authenticated_at,
            for_partner=for_partner,
            # uuid=uuid,

            SERVER_URL=SERVER_URL,
            access_token=access_token,
        )
    )


@app.post(path="/logout")
def _(request: Request,
      access_token: str = Form(...),
      target_id: str = Form(...), ):
    response = requests.post(
        url=LOGOUT_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                 "Authorization": f"Bearer {access_token}"},
        data=dict(
            target_id_type=TARGET_ID_TYPE,
            target_id=target_id,
        )
    )

    json = response.json()
    id = json.get("id")

    return templates.TemplateResponse(
        name="logout.html",
        context=dict(
            request=request,
            id=id,

            SERVER_URL=SERVER_URL,
        )
    )


if __name__ == '__main__':
    os.system("uvicorn main:app --reload")
