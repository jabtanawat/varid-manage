from datetime import datetime
from db import run_query_fetchall, run_query_commit, run_query_fetchone
from cryptography.fernet import Fernet

def ConvertDate(aDate):
  d1 = aDate.strftime("%d")
  d2 = aDate.strftime("%m")
  d3 = aDate.strftime("%Y")
  resultdate = f'{d3}-{d2}-{d1} 00:00:00'
  return resultdate

def ConvertDateSerach(aDate):
    format = "%Y/%m/%d"
    ResultDate = datetime.strptime(aDate, format)
    return ResultDate

def FormatDate(aDate):
    d1 = aDate.strftime("%d")
    d2 = aDate.strftime("%m")
    d3 = aDate.strftime("%Y")
    d4 = int(d3) + 543
    ResultDate = str(d1) + "/" + str(d2) + "/" + str(d4)
    return ResultDate
  
def FormatTime(aDate)  :
    d1 = aDate.strftime("%H:%M:%S")
    return d1

def CNUMBER(num) :
  result = f"{num:,.2f}"
  return result

# ===== GET RUNNING

def GETRUNNING(name) :
  DocRunning = ""
  RunLength = ""
  sql = f"SELECT Name, Front, Running, IF(AutoRun, 'true', 'false') AS AutoRun FROM Running WHERE Name = '{name}'"
  info =  run_query_fetchone(sql)
  Running = info[2]
  if info[3] == "true" :
    if Running != "NULL" :
      for i in range(int(len(Running))) :
        RunLength += "0"
      Number = int(Running) + 1
      Length = int(len(RunLength))      
      #DocRunning = info[1] + '{:0>5}'.format(Number)
      DocRunning = info[1] + str(Number).zfill(Length)
  return DocRunning  

# ===== SET RUNNING

def SETRUNNING(name, running):
  sql = f"SELECT Name, Front, Running, IF(AutoRun, 'true', 'false') AS AutoRun FROM Running WHERE Name = '{name}'"
  info =  run_query_fetchone(sql)
  if info[3] == "true" :
    Length = len(running) - len(info[2])
    Number = running[Length:]
    print(Number)
    sql = "UPDATE Running SET Running = %s WHERE Name = %s"
    executes = (Number, name)
    run_query_commit(sql, executes)

def TableWhere(FROM, VALUE, WHERE):
  sql = f"select * from {FROM} where {VALUE} = '{WHERE}'"
  row = run_query_fetchall(sql)
  length = len(row)
  return length

def TableWhereInfo(FROM, VALUE, WHERE):
  sql = f"select * from {FROM} where {VALUE} = '{WHERE}'"
  row = run_query_fetchall(sql)
  length = len(row)
  return length

def GET_USERNAME_COOKIE(INFO) :
  if DECRYPT(INFO) == "Developer" :
    return ["DEVE", "Developer"]
  SQL = f"SELECT EmpId, CONCAT(PreFix, ' ', F_Name, ' ', L_Name) AS FullName, User, Pass FROM Employee WHERE EmpId = '{DECRYPT(INFO)}'"
  RESULT = run_query_fetchone(SQL)
  return RESULT

def run1(r):
  D = ""
  for i in range (int(len(r))-1):
    D += "0"
  return D

key = b'AMzNNq1t876s27TtEziqbENXY0i5JYHd5ke_rRM0jOU='
f = Fernet(key)

def ENCRYPT(txt) :
  enc = txt.encode("utf-8")
  result = f.encrypt(enc).decode("utf-8") # ===== ????????????????????????????????????
  return result

def DECRYPT(txt) :
  enc = txt.encode("utf-8")
  result = f.decrypt(enc).decode("utf-8") # ===== ?????????????????????????????????
  return result