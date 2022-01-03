from flask import Blueprint, render_template, redirect, url_for, request,session, flash, jsonify
from db import run_query_fetchall, run_query_commit, run_query_fetchone
import library, os
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

@product.route('/product/frmgallery/<id>')
def frmgallery(id) :
    SQL = f"SELECT No, ProductId, ImageFile FROM Gallery WHERE ProductId = '{id}' ORDER BY No ASC"
    DATAGELLERY = run_query_fetchall(SQL) 
    return render_template('Product/FrmGallery.html', DATA = DATAGELLERY, ID = id) 

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
        if request.form.get('Active') :
            Active = True
        Description = request.form["txtDescription"]
        ImageFile = request.files["ImageFile"]
        # ===== SAVE DATA
        if mode == "add" :
            row = library.TableWhere("Product", "Id", Id)
            if row > 0 :        
                flash("ไม่สามารถทำรายการได้ !", "error")        
                return redirect(f"/product/frmproduct?mode={mode}")
            if ImageFile.filename != "" :
                Fil_Folder = 'static/image/product'
                App_Folder = os.path.dirname(__name__)
                Img_Folder = os.path.join(App_Folder, Fil_Folder)
                Fil_Name = ImageFile.filename.split('.')[0]
                Picture = ImageFile.filename.replace(Fil_Name, Id)
                IsExist = os.path.exists(os.path.join(Img_Folder, Picture))
                if IsExist :
                    os.remove(os.path.join(Img_Folder, Picture))
                ImageFile.save(os.path.join(Img_Folder, Picture))
                sql = "INSERT INTO Product (Id, Name, Price, Active, Description, CategoryId, ImageFile) VALUE (%s, %s, %s, %s, %s, %s, %s)"
                executes = (Id, Name, Price, Active, Description, CategoryId, Picture)
                run_query_commit(sql, executes)
                flash("บันทึกข้อมูลเรียบร้อย !", "success-save")
                return redirect("/product") 
            else :
                sql = "INSERT INTO Product (Id, Name, Price, Active, Description, CategoryId, ImageFile) VALUE (%s, %s, %s, %s, %s, %s, %s)"
                executes = (Id, Name, Price, Active, Description, CategoryId, "")
                run_query_commit(sql, executes)
                flash("บันทึกข้อมูลเรียบร้อย !", "success-save")
                return redirect("/product")
        # ===== EDIT DATA
        elif mode == "edit" :
            if ImageFile.filename != "" :
                Fil_Folder = 'static/image/product'
                App_Folder = os.path.dirname(__name__)
                Img_Folder = os.path.join(App_Folder, Fil_Folder)
                Fil_Name = ImageFile.filename.split('.')[0]
                Picture = ImageFile.filename.replace(Fil_Name, Id)
                IsExist = os.path.exists(os.path.join(Img_Folder, Picture))
                if IsExist :
                    os.remove(os.path.join(Img_Folder, Picture))
                ImageFile.save(os.path.join(Img_Folder, Picture))
                sql ="UPDATE Product SET Name = %s, Price = %s, Active = %s, Description = %s, CategoryId = %s, ImageFile = %s WHERE Id = %s"
                executes = (Name, Price, Active, Description, CategoryId, Picture, Id)
                run_query_commit(sql, executes)
                flash("แก้ไขข้อมูลเรียบร้อย !", "success-save")
                return redirect("/product") 
            else :
                sql ="UPDATE Product SET Name = %s, Price = %s, Active = %s, Description = %s, CategoryId = %s WHERE Id = %s"
                executes = (Name, Price, Active, Description, CategoryId, Id)
                run_query_commit(sql, executes)
                flash("แก้ไขข้อมูลเรียบร้อย !", "success-save")
                return redirect("/product") 
        else :
            flash("ไม่สามารถทำรายการได้ !", "error")
            return redirect(f"/product/frmproduct?mode={mode}") 

@product.route('/product/deletedata/<id>', methods=["POST", "GET"])
def deletedata(id):
    row = library.TableWhere("OrderSub", "ProductId", id)
    if row > 0 :         
        flash("ไม่สามารถทำรายการได้ !", "error")       
        return redirect('/product')
    sql = f"SELECT ImageFile FROM Product WHERE Id = {id}"
    Picture = run_query_fetchone(sql)
    if Picture[0] :
        Fil_Folder = 'static/image/product'
        App_Folder = os.path.dirname(__name__)
        Img_Folder = os.path.join(App_Folder, Fil_Folder)
        IsExist = os.path.exists(os.path.join(Img_Folder, Picture[0]))
        if IsExist :
            os.remove(os.path.join(Img_Folder, Picture[0]))
    sql = "DELETE FROM Product WHERE Id = %s"
    executes = (id)
    run_query_commit(sql, executes)
    flash("ลบข้อมูลเรียบร้อย !", "success-delete")
    return redirect('/product')

@product.route('/product/savegallery', methods=["POST"])
def savegallery() :
    if request.method == 'POST':
        PRODUCTID = request.form["id"]
        IMAGEFILE = request.files["ImageFile"]
        if IMAGEFILE.filename != "" :
            ROW_COUNT = library.TableWhere("Gallery", "ProductId", PRODUCTID)
            if ROW_COUNT == 4 :
                flash("ไม่สามารถทำรายการได้ !", "error")
                return redirect(f'/product/frmgallery/{PRODUCTID}')      
            NO = 0
            SQL = f"SELECT No FROM Gallery ORDER BY No DESC"
            ROW_INFO = run_query_fetchone (SQL)
            if ROW_INFO == None :
                NO = 1   
            else :
                NO = ROW_INFO[0] + 1
            Fil_Folder = 'static/image/product'
            App_Folder = os.path.dirname(__name__)
            Img_Folder = os.path.join(App_Folder, Fil_Folder)
            Fil_Name = IMAGEFILE.filename.split('.')[0]
            NAMEFILE = PRODUCTID + "_" + str(NO) 
            PICTURE = IMAGEFILE.filename.replace(Fil_Name, NAMEFILE)
            IsExist = os.path.exists(os.path.join(Img_Folder, PICTURE))
            if IsExist :
                os.remove(os.path.join(Img_Folder, PICTURE))
            IMAGEFILE.save(os.path.join(Img_Folder, PICTURE))
            sql = "INSERT INTO Gallery (ProductId, ImageFile) VALUE (%s, %s)"
            executes = (PRODUCTID, PICTURE)
            run_query_commit(sql, executes)
            flash("บันทึกข้อมูลเรียบร้อย !", "success")
            return redirect(f'/product/frmgallery/{PRODUCTID}') 
        else :
            flash("ไม่สามารถทำรายการได้ !", "error")
            return redirect(f'/product/frmgallery/{PRODUCTID}') 

@product.route('/product/delete/gallery', methods=["POST"])
def deleteGallery() :
    if request.method == 'POST':
        NO = request.form["No"]
        PRODUCTID = request.form["ProductId"]
        IMAGEFILE = request.form["ImageFile"]
        Fil_Folder = 'static/image/product'
        App_Folder = os.path.dirname(__name__)
        Img_Folder = os.path.join(App_Folder, Fil_Folder)
        IsExist = os.path.exists(os.path.join(Img_Folder, IMAGEFILE))
        if IsExist :
            os.remove(os.path.join(Img_Folder, IMAGEFILE))
    sql = "DELETE FROM Gallery WHERE No = %s AND ProductId = %s"
    executes = (NO, PRODUCTID)
    run_query_commit(sql, executes)
    flash("ลบรูปภาพเรียบร้อย !", "success")
    return redirect(f'/product/frmgallery/{PRODUCTID}') 