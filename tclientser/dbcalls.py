import sqlite3
import time
import datetime
from tkinter import messagebox
import bcrypt
#this contains db calls
#checklist
# 1. create
# 2. get
# 3. update
# 4. 


def login(name,password):
    db=sqlite3.connect('db.db')
    query = f"SELECT password FROM Account WHERE Name='{name}'"
    try:
        values=db.execute(query).fetchall()
        #print(values[0][0])
        if bcrypt.checkpw(password.encode("utf-8"), values[0][0].encode("utf-8")):
            return True
    except Exception as e:
        print ("error login", e)
        db.close()
        return False
    
    return False

def register(name, password):
    db=sqlite3.connect('db.db')
    query = "INSERT INTO Account (Name, Password) VALUES ('{}', '{}')".format(name, bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt(10)).decode("utf-8"))
    #print(query)
    try:
        db.execute(query)
        db.commit()
        print("committ success")
        db.close()
        return True
    except Exception as e:
        #messagebox.showwarning(title="Input Exists", message="Name already taken")
        print ("error regis", e)
        db.rollback()
        db.close()
        return False


#table and list of items
def get(table, items, condition = ""):
    db=sqlite3.connect('db.db')
    shop_list = ""
    for item in items:
        shop_list += item + ", "
    shop_list = shop_list[:len(shop_list)-2]
    query = f"SELECT {shop_list} FROM {table} " + condition
    #print(query)
    values = None
    try:
        values=db.execute(query).fetchall()
    except Exception as e:
        print ("error", e)
        db.rollback()
    db.close()
    return values

def getdistinct(table, items, condition = ""):
    db=sqlite3.connect('db.db')
    shop_list = ""
    for item in items:
        shop_list += item + ", "
    shop_list = shop_list[:len(shop_list)-2]
    query = f"SELECT DISTINCT {shop_list} FROM {table} " + condition
    #print(query)
    values = None
    try:
        values=db.execute(query).fetchall()
    except Exception as e:
        print ("error", e)
        db.rollback()
    db.close()
    repack = []
    if values:
        for val in values:
            repack.append(val[0])
    return repack

def add_status(table, items):
    #items for student
    db=sqlite3.connect('db.db')
    #query to get teacher account id
    #time conversion
    query = "INSERT INTO History (Acct ID, Session, Time, Status, Student ID) VALUES ('{}','{}','{}','{}','{}')".format()
    values = None
    try:
        #cur=db.cursor()
        values=db.execute(query).fetchall()
        #db.commit()
        #cur.fetchall()
    except:
        print ("error")
        db.rollback()
    db.close()
    return values

def filltree(my_tree, user, check_var, searchlimiter=""):
    
    my_tree.delete(*my_tree.get_children())
    conn = sqlite3.connect("db.db")
    if check_var=="All":
        query="SELECT a.ID,a.AcctID,a.Session,a.Time,a.Status,a.StudentID FROM History a INNER JOIN Account b ON a.AcctID = b.ID WHERE b.Name='{}'".format(user)
    else:
        query="SELECT a.ID,a.AcctID,a.Session,a.Time,a.Status,a.StudentID FROM History a INNER JOIN Account b ON a.AcctID = b.ID WHERE b.Name='{}' AND a.session='{}'".format(user,check_var)
    data = conn.execute(query).fetchall()
    conn.close()
    #varlist = [var1.get(), var2.get(), var3.get(), var4.get(), var5.get()]
    iid = 1
    for line in data:
        if line[3]:
            date1 = datetime.datetime.fromtimestamp(line[3]/1000.0)
        if searchlimiter == "": #or varlist == [0, 0, 0, 0, 0]:
            my_tree.insert(parent='', index='end', iid=iid, text="", values=(line[1], line[2], date1, line[4],  line[5]))
        else:
            text=""
            a=0
            for item in line:
                if a==3:
                    text+= str(datetime.datetime.fromtimestamp(item/1000.0))
                else:
                    text += str(item)
                a+=1

            if searchlimiter.lower() in text.lower():
                
                my_tree.insert(parent='', index='end', iid=iid, text="", values=(line[1], line[2], date1, line[4],  line[5]))
        #else:
        #    c = 0
        #    text = ""
        #    for item in varlist:
        #        if item == 1:
        #            text += str(line[c])
        #        c+=1
        #    if searchlimiter.lower() in text.lower():
        #        my_tree.insert(parent='', index='end', iid=iid, text="", values=(line[0], line[1], line[2], line[3], line[4]))
        iid += 1