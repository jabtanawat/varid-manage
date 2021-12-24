from flask import Blueprint, render_template, redirect, url_for, request,session, flash, jsonify
from db import run_query_fetchall, run_query_commit, run_query_fetchone
import library
from datetime import datetime

orders = Blueprint('order', __name__)

# =================================================================================
# === ORDER GET
# =================================================================================

@orders.route('/order')
def Index() :     
    sql = f"SELECT OrderId, Name, DocDate, DocTime, Status FROM Orders LEFT JOIN Member ON Orders.MemberId = Member.MemberId WHERE Status IN (1, 2, 3)"  
    dt_now =  run_query_fetchall(sql) 
    dt1 =[]
    for x in dt_now :
        order = x[0]
        menber = x[1]
        date = str(library.FormatDate(x[2])) + ' ' + str(x[3])
        status = x[4]
        dt1.append([order, menber, date, status])
    sql = f"SELECT OrderId, Name, DocDate, DocTime, Status FROM Orders LEFT JOIN Member ON Orders.MemberId = Member.MemberId WHERE Status IN (4)"
    dt_last =  run_query_fetchall(sql) 
    dt2 =[]
    for x in dt_last :
        order = x[0]
        menber = x[1]
        date = str(library.FormatDate(x[2])) + ' ' + str(x[3])
        status = x[4]
        dt2.append([order, menber, date, status])
    DateNow = library.FormatDate(datetime.now()) 
    TimeNow = library.FormatTime(datetime.now())
    return render_template('Order/Index.html', data = dt1, data2 = dt2, datenow = DateNow, timenow = TimeNow)

# =================================================================================
# === ORDER POST
# =================================================================================

@orders.route('/order/confirmorder', methods=["POST"])
def confirm() :
    if request.method == 'POST' :     
        OrderId = request.form["OrderId"]
        Status = 4
        Transport = request.form["Transport"]
        TransportName = request.form["TransportName"]
        sql = f"SELECT Status FROM Orders WHERE OrderId = '{OrderId}'"
        info = run_query_fetchone(sql)
        if info[0] == 2 or info[0] == 3 :
            if Transport != "" or TransportName != ""  :
                Status = 5
            sql ="UPDATE Orders SET Status = %s, Transport = %s, TransportName = %s WHERE OrderId = %s"
            executes = (Status, Transport, TransportName, OrderId)
            run_query_commit(sql, executes)
            flash(f"ยืนยันคำสั่งซื้อลเขที่ {OrderId} เรียยบร้อยคะ" , "success-save")
            return jsonify("success")
        return jsonify("error")
    return jsonify("error")



