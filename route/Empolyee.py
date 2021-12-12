from flask import Blueprint, render_template, redirect, url_for, request,session, flash, jsonify
from ssh_db import run_query_fetchall, run_query_commit, run_query_fetchone
import library
from decimal import Decimal

empolyees = Blueprint('empolyee', __name__)

@empolyees.route('/empolyee')
def empolyee():
    Dt =  run_query_fetchall("SELECT *  FROM employee where Status=true") 
    return render_template('empolyee.html',data=Dt) 


@empolyees.route('/saveemployee',methods=["POST"])
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
    return render_template('empolyee.html',data=Dt) 

@empolyees.route('/editempolyees',methods=["POST"])
def editempolyees():
    if request.method == 'POST':
        EmpId = request.form["EmpId"]