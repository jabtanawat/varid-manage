from flask import Blueprint, render_template, redirect, url_for, request,session, flash, jsonify
from db import run_query_fetchall, run_query_commit, run_query_fetchone
import library
from decimal import Decimal

members = Blueprint('member', __name__)

@members.route('/member')
def member():

    return render_template('member.html') 

@members.route('/savemember',methods=["POST"])
def savemember():
    if request.method == 'POST':
        MemberId = request.form["MemberId"]
        Name = request.form["Name"]
        Phone = request.form["Phone"]
        Address = request.form["Address"]
        
      
      
        
        sql = "INSERT INTO member (MemberId, Name,Tel,Address) VALUE (%s, %s, %s,%s)"
        executes = (MemberId, Name,Phone,Address)
        run_query_commit(sql, executes)

    Dt =  run_query_fetchall("SELECT *  FROM member") 
    return render_template('member.html',data=Dt) 