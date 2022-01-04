from flask import Blueprint, render_template, redirect, request, flash, make_response
from db import run_query_fetchall, run_query_commit, run_query_fetchone
import library
from datetime import datetime

payment = Blueprint('payment', __name__)

# =================================================================================
# === PAYMENT GET
# =================================================================================

@payment.route('/payment')
def Index() : 
    USERNAME_DASHBOARD = request.cookies.get('varid14Dashboard') 
    if not USERNAME_DASHBOARD :
        flash("หมดอายุการใช้งาน กรุณาเข้าสู่ระบบใหม่อีกครั้ง", "warning")
        res = make_response(redirect('/login'))
        res.set_cookie('varid14Dashboard', value = '', expires = 0)
        return res    
    sql = f"SELECT DocDate, DocNo, OrderId, Name, Price FROM Payment"  
    dt =  run_query_fetchall(sql) 
    return render_template('Payment/Index.html', NAME_USER = library.GET_USERNAME_COOKIE(USERNAME_DASHBOARD)[1], data = dt)