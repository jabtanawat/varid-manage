from flask import Blueprint, render_template, redirect, url_for, request,session, flash, jsonify
from db import run_query_fetchall, run_query_commit, run_query_fetchone
import library
from datetime import datetime

orders = Blueprint('order', __name__)

@orders.route('/order')
def order() :     
    Dt =  run_query_fetchall(f"SELECT OrderId, MemberId, DocTime, Status FROM Orders where Status <> 0 and DocDate='{datetime.today().strftime('%Y-%m-%d')}' ") 
    Dt1 =  run_query_fetchall(f"SELECT OrderId, MemberId, DocTime, Status FROM Orders where Status =  0 and DocDate='{datetime.today().strftime('%Y-%m-%d')}'  ") 
    DateNow = library.FormatDate(datetime.now()) 
    TimeNow = library.FormatTime(datetime.now())
    return render_template('order.html', data = Dt, data2 = Dt1, datenow = DateNow, timenow = TimeNow)

@orders.route('/orderdetail/<id>')
def orderdetail(id):
    class order:
        def __init__(self, O_Id, O_MemberId, O_Date, O_Status, O_Phone, O_Address, O_Time, O_MemberName):
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
    Dt =  run_query_fetchall(f"SELECT O_ProductId,(select Name from Product where O_ProductId=ID  ) as O_Productname, O_ProductAmount FROM ordersdetail where O_Id='{id}' ") 
    return render_template('orderdetail.html',info=info,data=Dt)


