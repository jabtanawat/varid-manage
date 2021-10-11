from flask import Blueprint, render_template,redirect, url_for,request,session, flash
from ssh_db import run_query_fetchall, run_query_commit,run_query_fetchone
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
def index():
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



@back.route('/bn/product/')
def product():
    Dt =  run_query_fetchall("SELECT P_Id,P_Name,(Select Name  FROM productgroup  where Id=P_Group) as P_GroupName,case when P_Status=true then 'ใช้งาน' else 'ปิดใช้งาน'  end as P_Status,P_Group,P_Price,P_Count,P_Date,P_Detail FROM product") 
    Dt1 = run_query_fetchall("SELECT Id,Name  FROM productgroup where Status=true") 
    return render_template('bn/product.html',data=Dt,data1=Dt1)

@back.route('/bn/productadd')
def productadd():
    Dt1 = run_query_fetchall("SELECT Id,Name  FROM productgroup where Status=true") 
    return render_template('bn/productadd.html',data=Dt1)


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

# =================================================================================
# === หมวดหมู่ GET
# =================================================================================


@back.route('/bn/productgroup')
def productgroup():
    Dt =  run_query_fetchall("SELECT Id, Name FROM productgroup where Status=true") 
    return render_template('bn/product/productgroup.html', data=Dt) 

@back.route('/bn/frmgroup')
def frmgroup():
    return render_template('bn/product/frmgroup.html') 

# =================================================================================
# === หมวดหมู่ POST
# =================================================================================

@back.route('/savegroupproduct', methods=["POST"])
def savegroupproduct():
    if request.method == 'POST':
        groupid = request.form["groupid"]
        groupname = request.form["groupname"]
        row = library.TableWhere("productgroup", "Id", groupid)
        if row > 0 :
            flash("ไม่สามารถบันทึกข้อมูลได้ !")
            return render_template('bn/product/frmgroup.html')
        sql = "INSERT INTO productgroup (Id, Name, Status) VALUE (%s, %s, %s)"
        executes = (groupid, groupname, True)
        run_query_commit(sql, executes)
        return redirect('/bn/productgroup') 

@back.route('/editproductgroup', methods=["POST"])
def editproductgroup():
    if request.method == 'POST':
        groupid = request.form["groupid"]
        groupname = request.form["groupname"]
        sql ="update productgroup set Id = %s, Name = %s where Id = %s"
        executes = (groupid, groupname, groupid)
        run_query_commit(sql, executes)
        return redirect('/bn/productgroup')

@back.route('/deletegroup/<id>', methods=["POST", "GET"])
def deletegroup(id):
    sql = "delete from productgroup where Id = %s"
    executes = (id)
    run_query_commit(sql, executes)
    flash("ลบข้อมูลเรียบร้อยแล้ว !")
    return redirect('/bn/productgroup')


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

@back.route('/bn/empolyee')
def empolyee():
    Dt =  run_query_fetchall("SELECT *  FROM employee where Status=true") 
    return render_template('bn/empolyee.html',data=Dt) 


@back.route('/saveemployee',methods=["POST"])
def saveemployee():
    if request.method == 'POST':
        EmpId = request.form["EmpId"]
        Prefix = request.form["Prefix"]
        F_Name = request.form["F_Name"]
        L_Name = request.form["L_Name"]
        Idcard = request.form["Idcard"]
        Sex = request.form["Sex"]
        Age = request.form["Age"]
        Address = request.form["Address"]
        Birthday = request.form["Birthday"]
        Phone = request.form["Phone"]
       # Picpath = request.form["files"]
        Status = request.form["Status"]
      
      
        
        sql = "INSERT INTO employee (EmpId, Prefix,F_Name,L_Name,Idcard,Sex,Age,Address,Birthday,Phone,Picpath,Status) VALUE (%s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s, %s)"
        executes = (EmpId, Prefix,F_Name,L_Name,Idcard,Sex,Age,Address,library.ConvertDate(Birthday) ,Phone,"",Status)
        run_query_commit(sql, executes)

    Dt =  run_query_fetchall("SELECT *  FROM employee where Status=true") 
    return render_template('bn/empolyee.html',data=Dt) 

@back.route('/bn/order')
def order():
     
     Dt =  run_query_fetchall(f"SELECT O_Id,O_MemberId,O_Time,O_Status  FROM orders where O_Status <> 0 and O_Date='{datetime.today().strftime('%Y-%m-%d')}' ") 
     Dt1 =  run_query_fetchall(f"SELECT O_Id,O_MemberId,O_Time,O_Status  FROM orders where O_Status =  0 and O_Date='{datetime.today().strftime('%Y-%m-%d')}'  ") 
     DateNow = library.FormatDate(datetime.now()) 
     TimeNow = library.FormatTime(datetime.now())

     return render_template('bn/order.html',data=Dt,data2=Dt1,datenow=DateNow,timenow=TimeNow)


@back.route('/bn/orderdetail/<id>')
def orderdetail(id):
    class order:
        def __init__(self,O_Id, O_MemberId, O_Date,O_Status,O_Phone,O_Address,O_Time,O_MemberName):
            self.O_Id = O_Id
            self.O_MemberId = O_MemberId
            self.O_Date = O_Date
            self.O_Status = O_Status
            self.O_Phone = O_Phone
            self.O_Address = O_Address
            self.O_Time = O_Time
            self.O_MemberName = O_MemberName
     
    data1 =  run_query_fetchone(f"SELECT O_Id,O_MemberId,O_Date,O_Status,O_Phone,O_Address,O_Time,(select Name from member where Id=O_MemberId ) as O_MemberName  FROM orders where O_Id='{id}' ")     
    info = order(str(data1[0]),str(data1[1]),library.FormatDate(data1[2]) ,str(data1[3]),str(data1[4]),str(data1[5]),str(data1[6]),str(data1[7])) 
    Dt =  run_query_fetchall(f"SELECT O_ProductId,(select P_Name from product where O_ProductId=P_Id  ) as O_Productname, O_Productcount FROM ordersdetail where O_Id='{id}' ") 
    return render_template('bn/orderdetail.html',info=info,data=Dt)



@back.route('/bn/member')
def member():

    return render_template('bn/member.html') 


@back.route('/bn/bank')
def bank():
    Dt =  run_query_fetchall("SELECT Bankid,Bankaccount,Bankname  FROM bank where Status=true") 
    return render_template('bn/bank.html',data=Dt) 


@back.route('/savebank',methods=["POST"])
def savebank():
    if request.method == 'POST':
        BankId = request.form["BankId"]
        Bankname = request.form["Bankname"]
        Bankaccount = request.form["Bankaccount"]
     
      
      
        
        sql = "INSERT INTO bank (Bankid, Bankname,Bankaccount,Status) VALUE (%s, %s, %s, %s)"
        executes = (BankId, Bankname,Bankaccount,True)
        run_query_commit(sql, executes)

        Dt =  run_query_fetchall("SELECT *  FROM bank where Status=true") 
        return render_template('bn/bank.html',data=Dt) 


@back.route('/editbank',methods=["POST"])
def editbank():
   if request.method == 'POST':
        BankId = request.form["BankId"]
        Bankname = request.form["Bankname"]
        Bankaccount = request.form["Bankaccount"]
        
            
        sql =f"update  bank  set Bankid={BankId},Bankname={Bankname},Bankaccount={Bankaccount}  where BankId={BankId} "
      
        run_query_commit(sql, "")
    
        Dt =  run_query_fetchall(f"SELECT *  FROM bank where Status=true") 
        return render_template('bn/bank.html',data=Dt) 

@back.route('/bn/runing')
def runing():
  
    return render_template('bn/runing.html')

@back.route('/bn/ordrerhistory')
def ordrerhistory():
    Dt =  run_query_fetchall("SELECT  O_Id ,(select Name from member  where Id=O_MemberId) as Name,O_Date FROM orders where O_Status='2'") 
    return render_template('bn/ordrerhistory.html',data= Dt)