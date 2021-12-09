from flask import Blueprint, render_template, redirect, url_for, request,session, flash, jsonify
from ssh_db import run_query_fetchall, run_query_commit, run_query_fetchone
import library
from decimal import Decimal

product = Blueprint('product', __name__)

# =================================================================================
# === สินค้า GET
# =================================================================================

@product.route('/product')
def index():
    sql = "SELECT Id, Name,(Select Name FROM Category where Id = CategoryId) as Category, case when Active = true then 'ใช้งาน' else 'ปิดใช้งาน' end as Active, Price FROM Product"
    dt =  run_query_fetchall(sql) 
    return render_template('Product/index.html', data = dt) 

@product.route('/product/frmproduct')
def frmcategory():
    category = run_query_fetchall("SELECT Id, Name FROM Category") 
    return render_template('Product/FrmProduct.html', data = category) 

# =================================================================================
# === สินค้า POST
# =================================================================================

@product.route('/product/savedata', methods=["POST"])
def savedata():
    if request.args.get('mode') :
        mode = str(request.args.get('mode'))
    else :
        return jsonify("error")
    Active = False
    if request.method == 'POST':
        Id = request.form["Id"]
        Name = request.form["Name"]
        CategoryId = request.form["CategoryId"]
        Price = request.form["Price"].replace(",", "")
        if request.form["Active"] == "true" :
            Active = True
        Description = request.form["Description"]
        if mode == "add" :
            row = library.TableWhere("Product", "Id", Id)
            if row > 0 :                
                return jsonify("error")
            sql = "INSERT INTO Product (Id, Name, Price, Active, Description, CategoryId) VALUE (%s, %s, %s, %s, %s, %s)"
            executes = (Id, Name, Price, Active, Description, CategoryId)
            run_query_commit(sql, executes)
            flash("บันทึกข้อมูลเรียบร้อย !", "success-save")
            return jsonify("success")
        elif mode == "edit" :
            sql ="update Product set Name = %s, Price = %s, Active = %s, Description = %s, CategoryId= %s where Id = %s"
            executes = (Name, Price, Active, Description, CategoryId, Id)
            run_query_commit(sql, executes)
            flash("แก้ไขข้อมูลเรียบร้อย !", "success-save")
            return jsonify("success")
        else :
            return jsonify("error")

@product.route('/product/deletedata/<id>', methods=["POST", "GET"])
def deletedata(id):
    #row = library.TableWhere("Product", "P_CategoryId", id)
    #if row > 0 :                
    #    return jsonify("error")
    sql = "delete from Product where Id = %s"
    executes = (id)
    run_query_commit(sql, executes)
    flash("ลบข้อมูลเรียบร้อย !", "success-save")
    return redirect('/product')