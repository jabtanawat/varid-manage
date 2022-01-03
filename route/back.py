from flask import Blueprint, render_template,redirect, url_for,request,session, flash
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
    SQLDATENOW = f"SELECT COUNT(OrderId) FROM Orders WHERE DocDate = '{library.ConvertDate(datetime.now())}'"
    INFODATENOW = run_query_fetchone(SQLDATENOW)
    SQLDATEALL = f"SELECT COUNT(OrderId) FROM Orders"
    INFODATEALL = run_query_fetchone(SQLDATEALL)
    SQLSUMNOW = f"SELECT IFNULL(SUM(Price), 0) FROM Orders WHERE DocDate = '{library.ConvertDate(datetime.now())}'"
    INFOSUMNOW = run_query_fetchone(SQLSUMNOW)
    SQLSUMALL = f"SELECT IFNULL(SUM(Price), 0) FROM Orders"
    INFOSUMALL = run_query_fetchone(SQLSUMALL)
    return render_template('index.html')

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








@back.route('/saveproduct',methods=["POST"])
def saveproduct():
    if request.method == 'POST':
        P_Id = request.form["P_Id"]
        P_Name = request.form["P_Name"]
        P_Group = request.form["P_Group"]
        P_Price = request.form["P_Price"]
        P_Count = ""
        P_Date = datetime.DateNow()
        P_Detail = request.form["P_Detail"]
      
        
        sql = "INSERT INTO product (P_Id, P_Name,P_Group,P_Price,P_Count,P_Date,P_Detail ,P_Status,P_Color) VALUE (%s, %s, %s, %s, %s, %s, %s, %s,%s)"
        executes = (P_Id, P_Name,P_Group, P_Price,P_Count,library.ConvertDate(P_Date),P_Detail,True, "")
        run_query_commit(sql, executes)

        Dt =  run_query_fetchall("SELECT P_Id,P_Name,(Select Name  FROM productgroup  where Id=P_Group) as P_GroupName,case when P_Status=true then 'ใช้งาน' else 'ปิดใช้งาน'  end as P_Status,P_Group,P_Price,P_Count,P_Date  FROM product") 
    return render_template('bn/product.html',data=Dt) 



@back.route('/bn/productdetail/<id>')
def productdetail(id):
    class product:
        def __init__(self,P_Id, P_Name, P_Group,P_Price,P_Date,P_Detail,P_Count,P_Status):
            self.P_Id = P_Id
            self.P_Name = P_Name
            self.P_Group = P_Group
            self.P_Price = P_Price
            self.P_Date = P_Date
            self.P_Detail = P_Detail
            self.P_Count = P_Count
            self.P_Status = P_Status
    data =  run_query_fetchone(f"SELECT P_Id,P_Name,P_Group,P_Price,P_Date,P_Detail,P_Count,case when P_Status=true then 'ใช้งาน' else 'ปิดใช้งาน'  end as P_Status  FROM product where P_Id='{id}' ") 

    info = product(str(data[0]),str(data[1]),str(data[2]),str(data[3]),library.FormatDate(data[4]),str(data[5]),str(data[6]),str(data[7]))
    Dt1 = run_query_fetchall("SELECT Id,Name  FROM productgroup where Status=true") 
    return render_template('bn/productdetail.html',info=info,data=Dt1)

@back.route('/bn/productedit/<id>')
def productedit(id):
    class product:
        def __init__(self,P_Id, P_Name, P_Group,P_Price,P_Date,P_Detail,P_Count,P_Status):
            self.P_Id = P_Id
            self.P_Name = P_Name
            self.P_Group = P_Group
            self.P_Price = P_Price
            self.P_Date = P_Date
            self.P_Detail = P_Detail
            self.P_Count = P_Count
            self.P_Status = P_Status
    data =  run_query_fetchone(f"SELECT P_Id,P_Name,P_Group,P_Price,P_Date,P_Detail,P_Count,case when P_Status=true then 'ใช้งาน' else 'ปิดใช้งาน'  end as P_Status  FROM product where P_Id='{id}' ") 


    info = product(str(data[0]),str(data[1]),str(data[2]),str(data[3]),library.FormatDate(data[4]),str(data[5]),str(data[6]),str(data[7]))
    Dt1 = run_query_fetchall("SELECT Id,Name  FROM productgroup where Status=true") 
    return render_template('bn/productedit.html',info=info,data=Dt1)











@back.route('/editproduct', methods=["POST"])
def editproduct():
    if request.method == 'POST':
        P_Id = request.form["P_Id"]
        P_Name = request.form["P_Name"]
        P_Group = request.form["P_Group"]
        P_Price = request.form["P_Price"]
        
     
        P_Detail = request.form["P_Detail"]
        sql ="update product set P_Id=%s,P_Name=%s,P_Group=%s,P_Price=%s,P_Detail=%s  where Id=%s"
        executes = (P_Id, P_Name, P_Group,P_Price,P_Detail)
        run_query_commit(sql, executes)
    
        Dt =  run_query_fetchall(f"SELECT *  FROM product where Status=true") 
    return render_template('bn/product.html',data=Dt) 












@back.route('/bn/runing')
def runing():
  
    return render_template('bn/runing.html')

