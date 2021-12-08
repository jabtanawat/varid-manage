from flask import Blueprint, render_template, redirect, url_for, request,session, flash, jsonify
from ssh_db import run_query_fetchall, run_query_commit, run_query_fetchone
import library

product = Blueprint('product', __name__)

# =================================================================================
# === สินค้า GET
# =================================================================================

@product.route('/product')
def index():
    sql = "SELECT P_Id, P_Name,(Select Name  FROM Category  where Id = P_CategoryId) as P_GroupName, case when P_Status = true then 'ใช้งาน' else 'ปิดใช้งาน' end as P_Status, P_CategoryId, P_Price P_Detail FROM Product"
    dt =  run_query_fetchall(sql) 
    return render_template('Product/index.html', data = dt) 

@product.route('/product/frmproduct')
def frmcategory():
    Dt1 = run_query_fetchall("SELECT Id, Name FROM Category") 
    return render_template('Product/FrmProduct.html', data = Dt1) 

# =================================================================================
# === สินค้า POST
# =================================================================================

@product.route('/category/savedata', methods=["POST"])
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
            return jsonify("success")
        elif mode == "edit" :
            sql ="update Category set Name = %s, Description = %s where Id = %s"
            executes = (Name, Description, Id)
            run_query_commit(sql, executes)
            return jsonify("success")
        else :
            return jsonify("error")

@product.route('/category/deletedata/<id>', methods=["POST", "GET"])
def deletedata(id):
    row = library.TableWhere("Product", "P_CategoryId", id)
    if row > 0 :                
        return jsonify("error")
    sql = "delete from Category where Id = %s"
    executes = (id)
    run_query_commit(sql, executes)
    return jsonify("success")