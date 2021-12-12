from flask import Blueprint, render_template, redirect, url_for, request,session, flash, jsonify
from ssh_db import run_query_fetchall, run_query_commit, run_query_fetchone
import library
from datetime import datetime

ordrerhistorys = Blueprint('ordrerhistory', __name__)

@ordrerhistorys.route('/ordrerhistory')
def ordrerhistory():
    Dt =  run_query_fetchall("SELECT  O_Id ,(select Name from member  where MemberId=O_MemberId) as Name,O_Date FROM orders where O_Status='2'") 
    return render_template('ordrerhistory.html',data= Dt)

@ordrerhistorys.route('/orderdetail/<id>')
def orderdetail(id):
    class order:
        def __init__(self,O_Id, O_MemberId, O_Date,O_Status,O_Phone,O_Address,O_Time,O_MemberName):
            self.O_Id = O_Id
            self.O_MemberId = O_MemberId
            self.O_Date = O_Date
            self.O_Status = O_Status
            self.O_Phone = O_Phone
            self.O_Address = O_Address
            self.O_Time = O_Time
            self.O_MemberName = O_MemberName
     
    data1 =  run_query_fetchone(f"SELECT O_Id,O_MemberId,O_Date,O_Status,O_Phone,O_Address,O_Time,(select Name from member where MemberId=O_MemberId ) as O_MemberName  FROM orders where O_Id='{id}' ")     
    info = order(str(data1[0]),str(data1[1]),library.FormatDate(data1[2]) ,str(data1[3]),str(data1[4]),str(data1[5]),str(data1[6]),str(data1[7])) 
    Dt =  run_query_fetchall(f"SELECT O_ProductId,(select P_Name from product where O_ProductId=P_Id  ) as O_Productname, O_Productcount FROM ordersdetail where O_Id='{id}' ") 
    return render_template('orderdetail.html',info=info,data=Dt)
