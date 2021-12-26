from flask import Blueprint, render_template, redirect, url_for, request,session, flash, jsonify
from db import run_query_fetchall, run_query_commit, run_query_fetchone
import library
from datetime import datetime

payment = Blueprint('payment', __name__)

# =================================================================================
# === PAYMENT GET
# =================================================================================

@payment.route('/payment')
def Index() :     
    sql = f"SELECT DocDate, DocNo, OrderId, Name, Price FROM Payment"  
    dt =  run_query_fetchall(sql) 
    return render_template('Payment/Index.html', data = dt)