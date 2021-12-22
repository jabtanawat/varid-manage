from flask import Blueprint, render_template, redirect, url_for, request,session, flash, jsonify
from db import run_query_fetchall, run_query_commit, run_query_fetchone
import library

banks = Blueprint('bank', __name__)

# =================================================================================
# === BANK GET
# =================================================================================

@banks.route('/bank')
def index() :
    sql = "SELECT AccountCode, AccountName, BankName FROM Bank"
    dt =  run_query_fetchall(sql) 
    return render_template('Bank/Index.html', data = dt) 

@banks.route('/bank/frmbank')
def frmbank() :
    return render_template('Bank/FrmBank.html') 

# =================================================================================
# === BANK POST
# =================================================================================

@banks.route('/bank/savedata', methods=["POST"])
def savedata():
    if request.args.get('mode') :
        mode = str(request.args.get('mode'))
    else :
        return jsonify("error")
    Status = False
    if request.method == 'POST' :     
        AccountCode = request.form["AccountCode"]   
        AccountName = request.form["AccountName"]        
        BankName = request.form["BankName"]
        if request.form["Status"] == "true" :
            Status = True
        # ===== Add
        if mode == "add" :
            row = library.TableWhere("Bank", "AccountCode", AccountCode)
            if row > 0 :                
                return jsonify("error")
            sql = "INSERT INTO Bank (AccountCode, AccountName, BankName, Status) VALUE (%s, %s, %s, %s)"
            executes = (AccountCode, AccountName, BankName, Status)
            run_query_commit(sql, executes)
            flash("บันทึกข้อมูลเรียบร้อย !", "success-save")
            return jsonify("success")
        # ===== Edit
        elif mode == "edit" :
            sql ="UPDATE Bank SET AccountName = %s, BankName = %s, Status = %s  where AccountCode = %s"
            executes = (AccountName, BankName, Status, AccountCode)
            run_query_commit(sql, executes)
            flash("แก้ไขข้อมูลเรียบร้อย !", "success-save")
            return jsonify("success")
        else :
            return jsonify("error")
    return jsonify("error")

@banks.route('/bank/deletedata/<id>', methods=["POST", "GET"])
def deletedata(id):
    row = library.TableWhere("Payment", "AccountBank", id)
    if row > 0 :                
        flash("ไม่สามารถทำรายการได้ !", "error")
        return redirect('/bank')
    sql = "DELETE FROM Bank where AccountCode = %s"
    executes = (id)
    run_query_commit(sql, executes)
    flash("ลบข้อมูลเรียบร้อย !", "success-save")
    return redirect('/bank')