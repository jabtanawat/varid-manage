from flask import Blueprint, render_template, redirect, url_for, request,session, flash
from ssh_db import run_query_fetchall, run_query_commit, run_query_fetchone
import library

category = Blueprint('category', __name__)

# =================================================================================
# === หมวดหมู่ GET
# =================================================================================

@category.route('/category')
def index():
    sql = "SELECT Id, Name FROM productgroup where Status=true"
    dt =  run_query_fetchall(sql) 
    return render_template('Category/index.html', data = dt) 

@category.route('/category/frmcategory')
def frmcategory():
    return render_template('Category/FrmCategory.html') 

# =================================================================================
# === หมวดหมู่ POST
# =================================================================================

@category.route('/category/savedata', methods=["POST"])
def savegroupproduct():
    if request.method == 'POST':
        groupid = request.form["groupid"]
        groupname = request.form["groupname"]
        row = library.TableWhere("productgroup", "Id", groupid)
        if row > 0 :
            flash("ไม่สามารถบันทึกข้อมูลได้ !")
            return render_template('bn/product/frmgroup.html')
        sql = "INSERT INTO productgroup (Id, Name, Status) VALUE (%s, %s, %s)"
        executes = (groupid, groupname, True)
        run_query_commit(sql, executes)
        return redirect('/bn/productgroup') 

@category.route('/category/editdata', methods=["POST"])
def editproductgroup():
    if request.method == 'POST':
        groupid = request.form["groupid"]
        groupname = request.form["groupname"]
        sql ="update productgroup set Id = %s, Name = %s where Id = %s"
        executes = (groupid, groupname, groupid)
        run_query_commit(sql, executes)
        return redirect('/bn/productgroup')

@category.route('/category/deletedata/<id>', methods=["POST", "GET"])
def deletegroup(id):
    sql = "delete from productgroup where Id = %s"
    executes = (id)
    run_query_commit(sql, executes)
    flash("ลบข้อมูลเรียบร้อยแล้ว !")
    return redirect('/bn/productgroup')