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
        sql = f"SELECT OrderId, Status, MemberName, Phone, Address FROM Orders WHERE OrderId = '{id}'"
        data =  db.run_query_fetchone(sql)
        return jsonify({'htmlresponse': render_template('/Modals/M_Order.html', data = data)})