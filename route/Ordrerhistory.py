from flask import Blueprint, render_template, redirect, request, flash, make_response
from db import run_query_fetchall, run_query_commit, run_query_fetchone
import library
from datetime import datetime

orderhistorys = Blueprint('orderhistory', __name__)

# =================================================================================
# === ORDER HISTORY GET
# =================================================================================

@orderhistorys.route('/orderhistory')
def orderhistory() :
    USERNAME_DASHBOARD = request.cookies.get('varid14Dashboard') 
    if not USERNAME_DASHBOARD :
        flash("หมดอายุการใช้งาน กรุณาเข้าสู่ระบบใหม่อีกครั้ง", "warning")
        res = make_response(redirect('/login'))
        res.set_cookie('varid14Dashboard', value = '', expires = 0)
        return res
    sql = "SELECT OrderId, Name, DocDate, DocTime, Status FROM Orders LEFT JOIN Member ON Orders.MemberId = Member.MemberId WHERE Status IN (5)"
    dt_now = run_query_fetchall(sql) 
    dt =[]
    for x in dt_now :
        order = x[0]
        menber = x[1]
        date = str(library.FormatDate(x[2])) + ' ' + str(x[3])
        status = x[4]
        dt.append([order, menber, date, status])
    return render_template('/OrderHistory/Index.html', NAME_USER = library.GET_USERNAME_COOKIE(USERNAME_DASHBOARD)[1], data = dt)

@orderhistorys.route('/orderdetail/<id>')
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
     
    data1 =  run_query_fetchone(f"SELECT O_Id,O_MemberId,O_Date,O_Status,O_Phone,O_Address,O_Time,(select Name from member where MemberId=O_MemberId ) as O_MemberName  FROM orders where O_Id='{id}' ")     
    info = order(str(data1[0]),str(data1[1]),library.FormatDate(data1[2]) ,str(data1[3]),str(data1[4]),str(data1[5]),str(data1[6]),str(data1[7])) 
    Dt =  run_query_fetchall(f"SELECT O_ProductId,(select P_Name from product where O_ProductId=P_Id  ) as O_Productname, O_Productcount FROM ordersdetail where O_Id='{id}' ") 
    return render_template('orderdetail.html',info=info,data=Dt)
