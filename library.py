from datetime import datetime
from ssh_db import run_query_fetchall, run_query_commit, run_query_fetchone

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

# ===== GET เลขรันนิ่ง
def Getrunning(name) :
  data =  run_query_fetchone(f"SELECT * FROM runing where Docid = '{name}'")
  r = str(data[2])
  F = str(data[1])
  A = "" 
  B = "" 
  C = "" 
  D = "" 
  running = ""
  for i  in range(int(len(r))):    
    if r[i:i+1] == "0":
      A +="0"
    else:
      B += str(r[i:i+1])      
    if  B == "" :        
      D = run1(r)
      running = F + D + "1"
    else:
      C = str(int(B)+ 1) 
      running = F + A + C
  return running

# ===== SET เลขรันนิ่ง
def SetRunning(name, running):
  data =  run_query_fetchone(f"SELECT * FROM runing where Docid = '{name}'")
  length = len(running) - len(data[2])
  number = running[length:]
  sql = "update runing set Idruning = %s where Docid = %s"
  executes = (number, name)
  run_query_commit(sql, executes)

def TableWhere(FROM, VALUE, WHERE):
  sql = f"select * from {FROM} where {VALUE} = '{WHERE}'"
  row = run_query_fetchall(sql)
  length = len(row)
  return length

def run1(r):
  D = ""
  for i in range (int(len(r))-1):
    D += "0"
  return D

#print(ConvertDate("14/09/2021"))
#print(FormatDate(datetime.now()))