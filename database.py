
import sqlite3  

def db_conn():
    try:
        conn = sqlite3.connect("hrm.db")
        return True
    except Exception:
        return False


if db_conn():

    conn = sqlite3.connect("hrm.db")
    cur = conn.cursor()

    # r = ('sai','sais@gmail.com','12356')

    # p = ('Ram','ram@gmail.com')

    # l = ('sai','12356')

    # r_sql = ''' INSERT INTO signup(username,email,password)
    #               VALUES(?,?,?) '''

    # l_sql = ''' INSERT INTO signin(username,password)
    #               VALUES(?,?) '''

    # p_sql = '''INSERT INTO profile(username,email)
                #    VALUES(?,?) '''

    # cursor.execute(r_sql, r)
    # cursor.execute(l_sql, l)
    # cur.execute(p_sql, p)

    # conn.commit()

    # uname='sai'
    # pwd = '123456'
    # auth = ''' select * from signin where username=? AND password=? '''
    # cur.execute(auth,(uname,pwd))
    # row = cur.fetchone()
    # print(row)

else:
    print('db connection error')