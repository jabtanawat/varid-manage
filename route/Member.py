from flask import Blueprint, render_template, redirect, request, flash, jsonify, make_response
from db import run_query_fetchall, run_query_commit, run_query_fetchone
import library
from decimal import Decimal

members = Blueprint('member', __name__)

# =================================================================================
# === MEMBER GET
# =================================================================================

@members.route('/member')
def member() :
    USERNAME_DASHBOARD = request.cookies.get('varid14Dashboard') 
    if not USERNAME_DASHBOARD :
        flash("หมดอายุการใช้งาน กรุณาเข้าสู่ระบบใหม่อีกครั้ง", "warning")
        res = make_response(redirect('/login'))
        res.set_cookie('varid14Dashboard', value = '', expires = 0)
        return res
    sql = "SELECT MemberId, Name FROM Member"
    dt =  run_query_fetchall(sql)    
    return render_template('Member/Index.html', NAME_USER = library.GET_USERNAME_COOKIE(USERNAME_DASHBOARD)[1], data = dt) 

@members.route('/member/frmmember')
def frmmember() :
    USERNAME_DASHBOARD = request.cookies.get('varid14Dashboard') 
    if not USERNAME_DASHBOARD :
        flash("หมดอายุการใช้งาน กรุณาเข้าสู่ระบบใหม่อีกครั้ง", "warning")
        res = make_response(redirect('/login'))
        res.set_cookie('varid14Dashboard', value = '', expires = 0)
        return res
    if request.args.get('mode') :
        mode = str(request.args.get('mode'))
    if mode == "add" :
        DocRunning = library.GETRUNNING("Member")
        return render_template('Member/FrmMember.html', NAME_USER = library.GET_USERNAME_COOKIE(USERNAME_DASHBOARD)[1], DocRunning = DocRunning) 
    else :
        return render_template('Member/FrmMember.html', NAME_USER = library.GET_USERNAME_COOKIE(USERNAME_DASHBOARD)[1], DocRunning = "") 

# =================================================================================
# === MEMBER POST
# =================================================================================

@members.route('/member/savedata', methods=["POST"])
def savedata():
    if request.args.get('mode') :
        mode = str(request.args.get('mode'))
    else :
        return jsonify("error")
    if request.method == 'POST':        
        Id = request.form["Id"]
        Name = request.form["Name"]
        Tel = request.form["Tel"]
        Email = request.form["Email"]
        Address = request.form["Address"]
        User = request.form["User"]
        Pass = request.form["Pass"]
        if mode == "add" :
            Id = library.GETRUNNING("Member")
            if Id == "" :
                Id = request.form["Id"]
            row = library.TableWhere("Member", "MemberId", Id)
            if row > 0 :                
                return jsonify("error")
            row = library.TableWhere("Member", "User", User)
            if row > 0 :                
                return jsonify("error")
            sql = "INSERT INTO Member (MemberId, Name, Email, Address, Tel, User, Pass) VALUE (%s, %s, %s, %s, %s, %s, %s)"
            executes = (Id, Name, Email, Address, Tel, User, Pass)
            run_query_commit(sql, executes)
            library.SETRUNNING("Member", Id)
            flash("บันทึกข้อมูลเรียบร้อย !", "success-save")
            return jsonify("success")
        elif mode == "edit" :
            print("edit")
            sql ="update Member set Name = %s, Email = %s, Address = %s, Tel = %s, User = %s, Pass = %s where MemberId = %s"
            executes = (Name, Email, Address, Tel, User, Pass, Id)
            run_query_commit(sql, executes)
            flash("แก้ไขข้อมูลเรียบร้อย !", "success-save")
            return jsonify("success")
        else :
            return jsonify("error")

@members.route('/member/deletedata/<id>', methods=["POST", "GET"])
def deletedata(id):
    row = library.TableWhere("Orders", "MemberId", id)
    if row > 0 :                
        flash("ไม่สามารถทำรายการได้ !", "error")
        return redirect('/member')
    sql = "delete from Member where MemberId = %s"
    executes = (id)
    run_query_commit(sql, executes)
    flash("ลบข้อมูลเรียบร้อย !", "success-save")
    return redirect('/member')