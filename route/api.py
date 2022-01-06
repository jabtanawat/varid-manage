from flask import Blueprint, render_template, request, jsonify
from db import run_query_fetchall, run_query_commit, run_query_fetchone
import library, calendar, decimal
from datetime import datetime

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
    sql = f"SELECT Id, Name, CategoryId, CONVERT(Price, CHAR), IF(Active, 'true', 'false') AS Active, Description, ImageFile FROM Product WHERE Id = '{id}'"
    data =  run_query_fetchone(sql)
    return jsonify(data)

# =================================================================================
# === MEMBER API
# =================================================================================

@api.route('/api/member/<id>', methods=['POST', 'GET'])
def member(id):
    sql = f"select MemberId, Name, Tel, Email, Address, User, Pass from Member where MemberId = '{id}'"
    data =  run_query_fetchone(sql)
    return jsonify(data)

# =================================================================================
# === BANK API
# =================================================================================

@api.route('/api/bank/<id>', methods=['POST', 'GET'])
def bank(id):
    sql = f"SELECT AccountCode, AccountName, BankId, IF(Status, 'true', 'false') AS Status FROM Bank WHERE AccountCode = '{id}'"
    data =  run_query_fetchone(sql)
    return jsonify(data)

# =================================================================================
# === EMPLOYEE API
# =================================================================================

@api.route('/api/employee/<id>', methods=['POST', 'GET'])
def employee(id):
    sql = f"SELECT EmpId, PreFix, F_Name, L_Name, User, Pass, IF(Status, 'true', 'false') AS Status FROM Employee WHERE EmpId = '{id}'"
    info =  run_query_fetchone(sql)
    data = [info[0], info[1], info[2], info[3], info[4], library.DECRYPT(info[5]), info[6]]
    return jsonify(data)

# =================================================================================
# === OVERVIEW API 
# =================================================================================

@api.route('/api/chart', methods=['POST', 'GET'])
def chart() :
    today = datetime.today()

    MONTH_1_F = datetime(today.year, 1, 1)
    MONTH_2_F = datetime(today.year, 2, 1)
    MONTH_3_F = datetime(today.year, 3, 1)
    MONTH_4_F = datetime(today.year, 4, 1)
    MONTH_5_F = datetime(today.year, 5, 1)
    MONTH_6_F = datetime(today.year, 6, 1)
    MONTH_7_F = datetime(today.year, 7, 1)
    MONTH_8_F = datetime(today.year, 8, 1)
    MONTH_9_F = datetime(today.year, 9, 1)
    MONTH_10_F = datetime(today.year, 10, 1)
    MONTH_11_F = datetime(today.year, 11, 1)
    MONTH_12_F = datetime(today.year, 12, 1)

    MONTH_1_L = datetime(today.year, 1, calendar.monthrange(today.year, 1)[1])
    MONTH_2_L = datetime(today.year, 2, calendar.monthrange(today.year, 2)[1])
    MONTH_3_L = datetime(today.year, 3, calendar.monthrange(today.year, 3)[1])
    MONTH_4_L = datetime(today.year, 4, calendar.monthrange(today.year, 4)[1])
    MONTH_5_L = datetime(today.year, 5, calendar.monthrange(today.year, 5)[1])
    MONTH_6_L = datetime(today.year, 6, calendar.monthrange(today.year, 6)[1])
    MONTH_7_L = datetime(today.year, 7, calendar.monthrange(today.year, 7)[1])
    MONTH_8_L = datetime(today.year, 8, calendar.monthrange(today.year, 8)[1])
    MONTH_9_L = datetime(today.year, 9, calendar.monthrange(today.year, 9)[1])
    MONTH_10_L = datetime(today.year, 10, calendar.monthrange(today.year, 10)[1])
    MONTH_11_L = datetime(today.year, 11, calendar.monthrange(today.year, 11)[1])
    MONTH_12_L = datetime(today.year, 12, calendar.monthrange(today.year, 12)[1])

    INFO_1 =  run_query_fetchone(f"SELECT IFNULL(SUM(Price), 0) FROM Orders WHERE DocDate >= '{MONTH_1_F}' AND DocDate <= '{MONTH_1_L}'")
    INFO_2 =  run_query_fetchone(f"SELECT IFNULL(SUM(Price), 0) FROM Orders WHERE DocDate >= '{MONTH_2_F}' AND DocDate <= '{MONTH_2_L}'")
    INFO_3 =  run_query_fetchone(f"SELECT IFNULL(SUM(Price), 0) FROM Orders WHERE DocDate >= '{MONTH_3_F}' AND DocDate <= '{MONTH_3_L}'")
    INFO_4 =  run_query_fetchone(f"SELECT IFNULL(SUM(Price), 0) FROM Orders WHERE DocDate >= '{MONTH_4_F}' AND DocDate <= '{MONTH_4_L}'")
    INFO_5 =  run_query_fetchone(f"SELECT IFNULL(SUM(Price), 0) FROM Orders WHERE DocDate >= '{MONTH_5_F}' AND DocDate <= '{MONTH_5_L}'")
    INFO_6 =  run_query_fetchone(f"SELECT IFNULL(SUM(Price), 0) FROM Orders WHERE DocDate >= '{MONTH_6_F}' AND DocDate <= '{MONTH_6_L}'")
    INFO_7 =  run_query_fetchone(f"SELECT IFNULL(SUM(Price), 0) FROM Orders WHERE DocDate >= '{MONTH_7_F}' AND DocDate <= '{MONTH_7_L}'")
    INFO_8 =  run_query_fetchone(f"SELECT IFNULL(SUM(Price), 0) FROM Orders WHERE DocDate >= '{MONTH_8_F}' AND DocDate <= '{MONTH_8_L}'")
    INFO_9 =  run_query_fetchone(f"SELECT IFNULL(SUM(Price), 0) FROM Orders WHERE DocDate >= '{MONTH_9_F}' AND DocDate <= '{MONTH_9_L}'")
    INFO_10 =  run_query_fetchone(f"SELECT IFNULL(SUM(Price), 0) FROM Orders WHERE DocDate >= '{MONTH_10_F}' AND DocDate <= '{MONTH_10_L}'")
    INFO_11 =  run_query_fetchone(f"SELECT IFNULL(SUM(Price), 0) FROM Orders WHERE DocDate >= '{MONTH_11_F}' AND DocDate <= '{MONTH_11_L}'")
    INFO_12 =  run_query_fetchone(f"SELECT IFNULL(SUM(Price), 0) FROM Orders WHERE DocDate >= '{MONTH_12_F}' AND DocDate <= '{MONTH_12_L}'")
    DATA = [float(INFO_1[0]), float(INFO_2[0]), float(INFO_3[0]), float(INFO_4[0]), float(INFO_5[0]), float(INFO_6[0]), float(INFO_7[0]), float(INFO_8[0]), float(INFO_9[0]), float(INFO_10[0]), float(INFO_11[0]), float(INFO_12[0])]

    return jsonify(DATA)