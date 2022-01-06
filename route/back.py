from flask import Blueprint, render_template,redirect, url_for,request,session, flash, make_response
from db import run_query_fetchall, run_query_commit,run_query_fetchone
from datetime import datetime
import library
import os
import flask
import requests_oauthlib
from requests_oauthlib.compliance_fixes import facebook_compliance_fix



FB_CLIENT_ID="544685966615545"
FB_CLIENT_SECRET="8b9c14cae7b40bae00335b550163d59f"


FB_AUTHORIZATION_BASE_URL = "https://www.facebook.com/dialog/oauth"
FB_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"

URL = "https://05f5-2403-6200-88a8-8845-00-58e.ngrok.io"

URL = "http://27.254.174.33:5001/"

FB_SCOPE = ["email"]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
back = Blueprint('back', __name__)


##run_query_fetchall("SELECT * FROM product")
#executes = ("10000", "aaaaa","20000", "bbbbb")
##run_query_commit("INSERT INTO product (id, name) VALUE (%s, %s)", executes)

@back.route('/')
def index() :
    USERNAME_DASHBOARD = request.cookies.get('varid14Dashboard') 
    if not USERNAME_DASHBOARD :
        flash("หมดอายุการใช้งาน กรุณาเข้าสู่ระบบใหม่อีกครั้ง", "warning")
        res = make_response(redirect('/login'))
        res.set_cookie('varid14Dashboard', value = '', expires = 0)
        return res
    SQLDATENOW = f"SELECT COUNT(OrderId) FROM Orders WHERE DocDate = '{library.ConvertDate(datetime.now())}'"
    INFODATENOW = run_query_fetchone(SQLDATENOW) # จำนวนคำสั่งซื้อวันนี้
    SQLDATEALL = f"SELECT COUNT(OrderId) FROM Orders"
    INFODATEALL = run_query_fetchone(SQLDATEALL) # ยอดสั่งซื้อวันนี้
    SQLSUMNOW = f"SELECT IFNULL(SUM(Price), 0) FROM Orders WHERE DocDate = '{library.ConvertDate(datetime.now())}'"
    INFOSUMNOW = run_query_fetchone(SQLSUMNOW) # จำนวนคำสั่งซื้อทั้งหมด
    SQLSUMALL = f"SELECT IFNULL(SUM(Price), 0) FROM Orders"
    INFOSUMALL = run_query_fetchone(SQLSUMALL) # ยอดสั่งซื้อทั้งหมด
    DATAOVERVIEW = [INFODATENOW[0], library.CNUMBER(INFOSUMNOW[0]), INFODATEALL[0], library.CNUMBER(INFOSUMALL[0])]
    TODAY = datetime.now().strftime("%Y")
    YEAR = int(TODAY) + 543
    return render_template('index.html', DATAOVERVIEW = DATAOVERVIEW, NAME_USER = library.GET_USERNAME_COOKIE(USERNAME_DASHBOARD)[1], YEAR = YEAR)

@back.route('/bn/login')
def login():
    return render_template('bn/login.html')

@back.route('/bn/loginfacebook')
def loginfacebook():
	facebook = requests_oauthlib.OAuth2Session(
        FB_CLIENT_ID, redirect_uri=URL + "/fb-callback", scope=FB_SCOPE
	)
	authorization_url, _ = facebook.authorization_url(FB_AUTHORIZATION_BASE_URL)

	return flask.redirect(authorization_url)


@back.route("/fb-callback")
def callback():
    facebook = requests_oauthlib.OAuth2Session(
        FB_CLIENT_ID, scope=FB_SCOPE, redirect_uri=URL + "/fb-callback"
    )

    # we need to apply a fix for Facebook here
    facebook = facebook_compliance_fix(facebook)

    facebook.fetch_token(
        FB_TOKEN_URL,
        client_secret=FB_CLIENT_SECRET,
        authorization_response=flask.request.url,
    )

    # Fetch a protected resource, i.e. user profile, via Graph API

    facebook_user_data = facebook.get(
        "https://graph.facebook.com/me?fields=id,name,email,picture{url}"
    ).json()

    email = facebook_user_data["email"]
    name = facebook_user_data["name"]
    picture_url = facebook_user_data.get("picture", {}).get("data", {}).get("url")

    return f"""
    User information: <br>
    Name: {name} <br>
    Email: {email} <br>
    Avatar <img src="{picture_url}"> <br>
    <a href="/">Home</a>
    """