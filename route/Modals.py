from flask import Blueprint, render_template, request, jsonify
import db
import library

modals = Blueprint('modals', __name__)

# =================================================================================
# === ORDER MODAL
# =================================================================================

@modals.route('/modal/order', methods=['POST', 'GET'])
def order():
    if request.method == 'POST' :
        id = request.form["OrderId"]   
        sql = f"SELECT OrderId, Status, MemberName, Phone, Address, Transport, TransportName FROM Orders WHERE OrderId = '{id}'"
        data =  db.run_query_fetchone(sql)
        return jsonify({'htmlresponse': render_template('/Modals/M_Order.html', data = data)})

@modals.route('/modal/payment', methods=['POST', 'GET'])
def payment():
    if request.method == 'POST' :
        id = request.form["PaymentId"]   
        sql = f"SELECT DocNo, OrderId, Name, AccountBank, Price, DocDate, Hour, Minute, FileName, PayType FROM Payment WHERE DocNo = '{id}'"
        data =  db.run_query_fetchone(sql)
        return jsonify({'htmlresponse': render_template('/Modals/M_Payment.html', data = data)})