#!pip install PyMySQL
import pymysql
import datetime
user='visitor'

def createConn():
    return pymysql.connect(host='localhost', database='graduation_project', user='root', password='123456', port=3306)
def insertData(date,user,squat,glute_bridge,lunge):
    conn = createConn()
    cursor = conn.cursor()
    args = (date,user,squat,glute_bridge,lunge)
    query = "INSERT INTO exer_count (date, user, squat, glute_bridge, lunge) VALUES (%s, %s, %s, %s, %s);"
    cursor.execute(query,args)
    conn.commit()
    print("data inserted")
    conn.close()
def updateData(date,user,squat,glute_bridge,lunge):
    conn = createConn()
    cursor = conn.cursor()
    args = (squat,glute_bridge,lunge,date,user)
    query = "update exer_count set squat = %s, glute_bridge = %s, lunge = %s where `date`= %s and `user` = %s;"
    cursor.execute(query,args)
    conn.commit()
    #print("data updated")
    conn.close()
def showDataByDate(date,user):
    conn = createConn()
    cursor = conn.cursor()
    args = (date,user)
    if date=='all':
        query = "select * from exer_count where `user`=%s;"
    else:
        query = "select * from exer_count where `date`=%s and `user`=%s;"
    cursor.execute(query,args)
    result = cursor.fetchone()
    #print(result[3]) #glute-bridge
    print(result) #all
    conn.close()
    if result == None: return None
    else: return list(result)
def showDataBySearchDate(sdate,edate,user):
    conn = createConn()
    cursor = conn.cursor()
    args = (sdate,edate,user)
    query = "select * from exer_count where `date`>=%s and `date`<=%s and `user`=%s;"
    cursor.execute(query,args)
    result = cursor.fetchall()
    #print(result[3]) #glute-bridge
    #print(result) #all
    conn.close()
    if result == None: return None
    else: return list(result)
def deleteDataByDate(date,user):
    conn = createConn()
    cursor = conn.cursor()
    args = (date,user)
    query = "delete from exer_count where `date`=%s and `user`=%s;"
    cursor.execute(query,args)
    conn.commit()
    print('data deleted')
    conn.close()
def showDataBySearchYear(year,user):
    conn = createConn()
    cursor = conn.cursor()
    args = (user,year)
    query = "SELECT LEFT(`date`,7) AS `mon`, SUM(squat), SUM(glute_bridge), SUM(lunge) FROM exer_count WHERE `user`='%s' AND `date` LIKE '%s-%-%' GROUP BY RIGHT(`mon`,2);"
    cursor.execute(query,args)
    result = cursor.fetchall()
    #print(result[3]) #glute-bridge
    #print(result) #all
    conn.close()
    if result == None: return None
    else: return list(result)
def showDataBySearchYear(year,user):
    conn = createConn()
    cursor = conn.cursor()
    args = (user)
    query = "SELECT LEFT(`date`,7) AS `mon`, SUM(squat), SUM(glute_bridge), SUM(lunge) FROM exer_count WHERE `user`=%s AND `date` LIKE '"+year+"-%%-%%' GROUP BY RIGHT(`mon`,2);"
    cursor.execute(query,args)
    result = cursor.fetchall()
    conn.close()
    if len(result) == 0: return None
    else: return list(result)
def showDataBySearchMonth(year,month,user):
    conn = createConn()
    cursor = conn.cursor()
    args = (user)
    query = "SELECT RIGHT(`date`,2), squat, glute_bridge, lunge FROM exer_count WHERE `user`=%s AND `date` LIKE '"+year+"-"+month+"-%%';"
    cursor.execute(query,args)
    result = cursor.fetchall()
    #print(result)
    #print(result[3]) #glute-bridge
    #print(result) #all
    conn.close()
    if len(result) == 0: return None
    else: return list(result)
def showDataBySearchWeek(sdate,edate,user):
    conn = createConn()
    cursor = conn.cursor()
    args = (user,edate,sdate)
    query = "SELECT `date`, squat, glute_bridge, lunge FROM exer_count WHERE `user`=%s AND `date` <= %s AND `date` >= %s;"
    cursor.execute(query,args)
    result = cursor.fetchall()
    conn.close()
    if len(result) == 0: return None
    else: return list(result)
def dataExist(date,user):
    conn = createConn()
    cursor = conn.cursor()
    args = (date,user)
    query = "SELECT COUNT(*) FROM exer_count WHERE `date` = %s and `user` = %s;"
    cursor.execute(query,args)
    result = cursor.fetchone()
    conn.close()
    return result[0]
def setCounter(date,user,s,g,l):
    if dataExist(date,user) == 0:
        print('no')
        insertData(date, user, 0, 0, 0)
    else:
        print('yes')
        updateData(date, user, s, g, l)
        date, user, squat, bridge, lunge = showDataByDate(date,user)
        print(date, user, squat, bridge, lunge)
        return squat, bridge, lunge
def createAccount(account,password): #創建帳號
    conn = createConn()
    cursor = conn.cursor()
    args = (account)
    query = "SELECT account FROM user_account WHERE account = %s;"
    cursor.execute(query,args)
    result = cursor.fetchone()
    if result==None:
        args = (account,password)
        query = "INSERT INTO user_account VALUES (%s,%s);"
        cursor.execute(query,args)
        conn.commit()
        return True
    else:
        return False
def confirmAccount(account,password): #確認帳號密碼正確與否
    global user
    conn = createConn()
    cursor = conn.cursor()
    args = (account)
    query = "SELECT account, password FROM user_account WHERE account = %s;"
    cursor.execute(query,args)
    result = cursor.fetchone()
    #print(result)
    if result==None or result[0]==None:
        return False
    elif result[1]!=password:
        return False
    else:
        user=account
        return True
    

#today = datetime.datetime.now().strftime('%Y-%m-%d')
#insertData(today, 'user1', int(0), int(2), int(5))
#updateData(today,'user1',1,3,5)
#deleteDataByDate(today,user)
#showDataByDate(today)
#createAccount('user3','123')
#print(confirmAccount('user2','1234'))
#showDataBySearchMonth('2022','10','user1')