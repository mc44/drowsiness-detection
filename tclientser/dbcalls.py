import sqlite3

#this contains db calls
#checklist
# 1. create
# 2. get
# 3. update
# 4. 


def get(table, items):
    db=sqlite3.connect('db.db')
    query = ""
    values = None
    try:
        cur=db.cursor()
        cur.execute(query)
        #db.commit()
        values=cur.fetchall()
    except:
        print ("error")
        db.rollback()
    db.close()
    return values