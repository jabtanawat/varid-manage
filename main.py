from threading import Timer
from flask import Flask, render_template, redirect
from route.back import back
from route.api import api
from datetime import time, timedelta

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.permanent_session_lifetime = timedelta(hours=1)
app.register_blueprint(back)
app.register_blueprint(api)

@back.errorhandler(404)
def not_found(error):
    return redirect("/notfound") 

@back.route("/notfound")
def notfound():
    return render_template('/error/notfound.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=int("5011"))
