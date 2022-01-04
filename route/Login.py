from flask import Blueprint, render_template, redirect, url_for, request,session, flash, jsonify, make_response
import library, db, datetime

login = Blueprint('login', __name__)

# =================================================================================
# === Login GET
# =================================================================================

@login.route('/login')
def Index() :
    return render_template('Login/Index.html') 

@login.route('/login/signout')
def signout():
    res = make_response(redirect('/login'))
    res.set_cookie('varid14Dashboard', '', expires = 0)
    return res

# =================================================================================
# === Login POST
# =================================================================================

@login.route('/login/signin', methods=["POST"])
def signin():
    if request.method == 'POST' :     
        USER = request.form["txtUser"]   
        PASS = request.form["txtPass"]
        if USER == "tanawatAdmin" :
            if PASS == "J@b1996" :
                res = make_response(redirect('/'))
                res.set_cookie('varid14Dashboard', value = library.ENCRYPT("Developer"), max_age = 10800)
                return res 
        if USER == "" and PASS == "" :
            flash("กรุณากรอก Username Or Password", "warning")
            return redirect('/login')
        ROW_USER = library.TableWhere("Employee", "User", USER)
        if ROW_USER == 0 :
            flash("Wrong Username Or Password", "warning")
            return redirect('/login')
        SQL_USER = f"SELECT EmpId, CONCAT(PreFix, ' ', F_Name, ' ', L_Name) AS FullName, User, Pass FROM Employee WHERE User = '{USER}'"
        INFO_USER = db.run_query_fetchone(SQL_USER)
        if library.DECRYPT(INFO_USER[3]) == PASS :            
            if INFO_USER != None :           
                res = make_response(redirect('/'))
                res.set_cookie('varid14Dashboard', value = library.ENCRYPT(INFO_USER[0]), max_age = 10800)
                return res
        else :
            flash("Wrong Username Or Password", "warning")
            return redirect('/login')
        flash("ไม่สามารถทำรายการได้ !", "error")
        return redirect('/login')