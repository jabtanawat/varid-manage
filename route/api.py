from flask import Blueprint, render_template, request, jsonify
from ssh_db import run_query_fetchall, run_query_commit, run_query_fetchone
from library import *

api = Blueprint('api', __name__)

# =================================================================================
# === หมวดหมู่ API
# =================================================================================

@api.route('/api/category/<id>', methods=['POST', 'GET'])
def category(id):
    sql = f"select Id, Name, Description from Category where Id = '{id}'"
    data =  run_query_fetchone(sql)
    #page = int(page) #เลขที่หน้า
    #record = 12 #จำนวนสินค้าที่จะแสดง
    #offset = (page - 1) * record #หาเลขเริ่มต้น
    #if category == 'all' :
    #    sql_row = "select * from product"
    #    sql = f"select P_Id, P_Name, P_Detail, CONVERT(P_Price, CHAR) from product limit {offset}, {record}"
    #else :
    #    sql_row = f"select * from product where P_Group = '{category}'"
    #    sql = f"select P_Id, P_Name, P_Detail, CONVERT(P_Price, CHAR) from product where P_Group = '{category}' limit {offset}, {record}"
    #Product =  run_query_fetchall(sql)
    #Row =  run_query_fetchall(sql_row)
    #Count = len(Row) 
    #PageTotal = math.ceil(Count/record) #จำนวนหน้าที่แสดง
    return jsonify(data)

# =================================================================================
# === สินค้า API
# =================================================================================

@api.route('/api/product/<id>', methods=['POST', 'GET'])
def product(id):
    sql = f"select Id, Name, CategoryId, CONVERT(Price, CHAR), IF(Active, 'true', 'false') AS Active, Description from Product where Id = '{id}'"
    data =  run_query_fetchone(sql)
    return jsonify(data)