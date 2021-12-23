from flask import Blueprint, render_template, redirect, url_for, request,session, flash, jsonify
from db import run_query_fetchall, run_query_commit, run_query_fetchone
import library
from datetime import datetime

orders = Blueprint('order', __name__)

@orders.route('/order')
def Index() :     
    #sql = f"SELECT OrderId, MemberId, DocTime, Status FROM Orders WHERE Status <> 0 and DocDate = '{datetime.today().strftime('%Y-%m-%d')}'"    
    sql = f"SELECT OrderId, Name, DocDate, DocTime, Status FROM Orders LEFT JOIN Member ON Orders.MemberId = Member.MemberId WHERE Status IN (1, 2)"  
    dt_now =  run_query_fetchall(sql) 
    dt1 =[]
    for x in dt_now :
        order = x[0]
        menber = x[1]
        date = str(library.FormatDate(x[2])) + ' ' + str(x[3])
        status = x[4]
        dt1.append([order, menber, date, status])
    sql = f"SELECT OrderId, MemberId, DocTime, Status FROM Orders where Status =  0 and DocDate='{datetime.today().strftime('%Y-%m-%d')}'"
    print(sql)
    Dt1 =  run_query_fetchall(sql) 
    DateNow = library.FormatDate(datetime.now()) 
    TimeNow = library.FormatTime(datetime.now())
    return render_template('Order/Index.html', data = dt1, data2 = Dt1, datenow = DateNow, timenow = TimeNow)

@orders.route('/order/orderdetail/<id>')
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
    data1 =  run_query_fetchone(f"SELECT OrderId, MemberId, DocDate, Status, Phone, Address, DocTime, MemberId as MemberName  FROM Orders where OrderId='{id}' ")     
    info = order(str(data1[0]),str(data1[1]),library.FormatDate(data1[2]) ,str(data1[3]),str(data1[4]),str(data1[5]),str(data1[6]),str(data1[7])) 
    Dt =  run_query_fetchall(f"SELECT OrderId, ProductId as ProductName, Amount FROM OrderSub where OrderId='{id}' ") 
    return render_template('/Order/OrderDetail.html',info = info, data = Dt)


