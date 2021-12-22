from flask import Blueprint, render_template, redirect, url_for, request,session, flash, jsonify
from db import run_query_fetchall, run_query_commit, run_query_fetchone
import library
from decimal import Decimal

empolyees = Blueprint('empolyee', __name__)

# =================================================================================
# === EMPLOYEE GET
# =================================================================================

@empolyees.route('/employee')
def index() :
    sql = "SELECT EmpId, CONCAT(PreFix, ' ', F_Name, ' ', L_Name) AS FullName FROM Employee"
    dt =  run_query_fetchall(sql) 
    return render_template('Employee/Index.html', data = dt) 

@empolyees.route('/employee/frmemployee')
def frmempolyee() :
    return render_template('Employee/FrmEmployee.html') 

# =================================================================================
# === EMPLOYEE POST
# =================================================================================

@empolyees.route('/employee/savedata', methods=["POST"])
def savedata():
    if request.args.get('mode') :
        mode = str(request.args.get('mode'))
    else :
        return jsonify("error")
    Status = False
    if request.method == 'POST' :     
        EmpId = request.form["EmpId"]   
        PreFix = request.form["PreFix"]        
        F_Name = request.form["F_Name"]
        L_Name = request.form["L_Name"]
        User = request.form["User"]
        Pass = request.form["Pass"]
        if request.form["Status"] == "true" :
            Status = True
        # ===== Add
        if mode == "add" :
            row = library.TableWhere("Employee", "EmpId", EmpId)
            if row > 0 :                
                return jsonify("error")
            sql = "INSERT INTO Employee (EmpId, PreFix, F_Name, L_Name, User, Pass, Status) VALUE (%s, %s, %s, %s, %s, %s, %s)"
            executes = (EmpId, PreFix, F_Name, L_Name, User, Pass, Status)
            run_query_commit(sql, executes)
            flash("บันทึกข้อมูลเรียบร้อย !", "success-save")
            return jsonify("success")
        # ===== Edit
        elif mode == "edit" :
            sql ="UPDATE Employee SET PreFix = %s, F_Name = %s, L_Name = %s, User = %s, Pass = %s, Status = %s  WHERE EmpId = %s"
            executes = (PreFix, F_Name, L_Name, User, Pass, Status, EmpId)
            run_query_commit(sql, executes)
            flash("แก้ไขข้อมูลเรียบร้อย !", "success-save")
            return jsonify("success")
        else :
            return jsonify("error")
    return jsonify("error")

@empolyees.route('/employee/deletedata/<id>', methods=["POST", "GET"])
def deletedata(id):
    sql = "DELETE FROM Employee WHERE EmpId = %s"
    executes = (id)
    run_query_commit(sql, executes)
    flash("ลบข้อมูลเรียบร้อย !", "success-save")
    return redirect('/employee')