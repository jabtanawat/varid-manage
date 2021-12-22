from flask import Blueprint, render_template, redirect, url_for, request,session, flash, jsonify
from db import run_query_fetchall, run_query_commit, run_query_fetchone
import library

category = Blueprint('category', __name__)

# =================================================================================
# === หมวดหมู่ GET
# =================================================================================

@category.route('/category')
def index():
    sql = "SELECT Id, Name FROM Category"
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
    if request.args.get('mode') :
        mode = str(request.args.get('mode'))
    else :
        return jsonify("error")
    if request.method == 'POST':
        Id = request.form["Id"]
        Name = request.form["Name"]
        Description = request.form["Description"]
        if mode == "add" :
            row = library.TableWhere("Category", "Id", Id)
            if row > 0 :                
                return jsonify("error")
            sql = "INSERT INTO Category (Id, Name, Description) VALUE (%s, %s, %s)"
            executes = (Id, Name, Description)
            run_query_commit(sql, executes)
            flash("บันทึกข้อมูลเรียบร้อย !", "success-save")
            return jsonify("success")
        elif mode == "edit" :
            sql ="update Category set Name = %s, Description = %s where Id = %s"
            executes = (Name, Description, Id)
            run_query_commit(sql, executes)
            flash("แก้ไขข้อมูลเรียบร้อย !", "success-save")
            return jsonify("success")
        else :
            return jsonify("error")

@category.route('/category/deletedata/<id>', methods=["POST", "GET"])
def deletedata(id):
    row = library.TableWhere("Product", "CategoryId", id)
    if row > 0 :                
        flash("ไม่สามารถทำรายการได้ !", "error")
        return redirect('/category')
    sql = "delete from Category where Id = %s"
    executes = (id)
    run_query_commit(sql, executes)
    flash("ลบข้อมูลเรียบร้อย !", "success-save")
    return redirect('/category')