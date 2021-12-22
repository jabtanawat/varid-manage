from flask import Blueprint, render_template, redirect, url_for, request,session, flash, jsonify
from db import run_query_fetchall, run_query_commit, run_query_fetchone
import library

banks = Blueprint('bank', __name__)

@banks.route('/bank')
def bank():
    Dt =  run_query_fetchall("SELECT Bankid,Bankaccount,Bankname  FROM bank where Status=true") 
    return render_template('bank.html',data=Dt) 


@banks.route('/bank/savebank',methods=["POST"])
def savebank():
    if request.method == 'POST':
        BankId = request.form["BankId"]
        Bankname = request.form["Bankname"]
        Bankaccount = request.form["Bankaccount"]
     
      
      
        
        sql = "INSERT INTO bank (Bankid, Bankname,Bankaccount,Status) VALUE (%s, %s, %s, %s)"
        executes = (BankId, Bankname,Bankaccount,True)
        run_query_commit(sql, executes)

        Dt =  run_query_fetchall("SELECT *  FROM bank where Status=true") 
        return render_template('bank.html',data=Dt) 


@banks.route('/editbank',methods=["POST"])
def editbank():
   if request.method == 'POST':
        BankId = request.form["BankId"]
        Bankname = request.form["Bankname"]
        Bankaccount = request.form["Bankaccount"]
        
            
        sql =f"update  bank  set Bankid={BankId},Bankname={Bankname},Bankaccount={Bankaccount}  where BankId={BankId} "
      
        run_query_commit(sql, "")
    
        Dt =  run_query_fetchall(f"SELECT *  FROM bank where Status=true") 
        return render_template('bank.html',data=Dt) 

@banks.route('/runing')
def runing():
  
    return render_template('runing.html')