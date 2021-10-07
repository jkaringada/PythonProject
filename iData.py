import psycopg2
from config import config
from datetime import datetime



def insert_statsdata(obj1):
    sql = """INSERT INTO casestats(newcases,totalcases,netcase,reclasscases,outbreakcase,investcases,ndeath,tdeath,covdate)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING statsid;"""

    conn = None
    case_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        #print(council)
        # execute the INSERT statement
        cur.execute(sql, (obj1.ncase,obj1.tcase,obj1.netcase,obj1.rlccase,obj1.outcase,obj1.investcase,obj1.newd,obj1.totald,obj1.cvdate))
        # get the generated id back
        case_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return case_id  

def delete_statsdata():
    sql="""DELETE FROM casestats;"""     

    conn = None
    rows_deleted = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql)
        #cur.execute("DELETE FROM covcases WHERE part_id = %s", (part_id,))
        # get the number of updated rows
        rows_deleted = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted

def delete_statsdatabydate(dte):   

    conn = None
    rows_deleted = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute("DELETE FROM casestats WHERE covdate = %s", (dte))
        #cur.execute("DELETE FROM covcases WHERE part_id = %s", (part_id,))
        # get the number of updated rows
        rows_deleted = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted    

def insertnotesdata(str1):
     sql = """INSERT INTO covnotes(covdate,covnotes)
             VALUES(%s,%s) RETURNING covid;"""

     conn = None
     note_id= None
     try:
         params = config()
         conn = psycopg2.connect(**params)
         cur = conn.cursor()     
         dt=  datetime.now()
         cur.execute(sql,(dt,str1)) 
         note_id = cur.fetchone()[0]
         conn.commit()
         cur.close()
     except (Exception, psycopg2.DatabaseError) as error:
         print(error)
     finally:
         if conn is not None:
             conn.close()
     return note_id

def deletenotes():

    conn = None
    rows_deleted = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute("DELETE FROM covnotes")
        #cur.execute("DELETE FROM covcases WHERE part_id = %s", (part_id,))
        # get the number of updated rows
        rows_deleted = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted


def deletenotesbydate(dte):

    conn = None
    rows_deleted = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute("DELETE FROM covnotes WHERE covdate = %s", (dte))
        #cur.execute("DELETE FROM covcases WHERE part_id = %s", (part_id,))
        # get the number of updated rows
        rows_deleted = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted


def insert_covidData(dt,council,active,inactive,diff):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO covcases(case_date,lca,active_cases,total_cases,netcases)
             VALUES(%s,%s,%s,%s,%s) RETURNING Cvid;"""
    conn = None
    case_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        #print(council)
        # execute the INSERT statement
        cur.execute(sql, (dt,council,active,inactive,diff))
        # get the generated id back
        case_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return case_id

def insert_covidData_list(covid_list):
    """ insert multiple vendors into the vendors table  """
    sql = "INSERT INTO covcases(case_date,lca,active_cases,total_cases,netcases) VALUES(%s,%s,%s,%s,%s)"
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql,covid_list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def InqcovidData():
    """ query data from the vendors table """
    cov_dataList=[]
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT case_date,lca,active_cases,total_cases,netcases FROM covcases ORDER BY case_date")
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()

        while row is not None:
            cov_dataList.append(row)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()  
    return cov_dataList      

def get_CovActiveCaseByDate(dt):
    """ query parts from the parts table """
    conn = None
    dicti={}
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT case_date,lca,active_cases,total_cases,netcases FROM covcases where case_date=%(date)s",{'date':dt})
        rows = cur.fetchall()
       
        print("The number of parts: ", cur.rowcount)
        for row in rows:
            dicti[row[2]]=row[3]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()                
    return dicti

def get_Covlgaacasebydate():
    """ query parts from the parts table """
    conn = None
    dicti=dict()
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT case_date,lca,active_cases FROM covcases where case_date= (SELECT MAX (case_date) FROM covcases)")
        # cur.execute("SELECT case_date,lca,active_cases,total_cases,netcases FROM covcases where case_date=%(date)s",{'date':dt})
        rows = cur.fetchall()
       
        print("The number of parts: ", cur.rowcount)
        for row in rows:
            #print(row[1])
            dicti.update({row[1]:row[2]})
            # dicti[row[2]]=row[3]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()                
    return dicti    

def get_CovDataByDate(dt):
    """ query parts from the parts table """
    conn = None
    covidlistbydt=[]
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT case_date,lca,active_cases,total_cases,netcases FROM covcases where case_date=%(date)s",{'date':dt})
        rows = cur.fetchall()
        covidlistbydt.append(rows)
        print("The number of parts: ", cur.rowcount)
        for row in rows:
            print(row)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()                
    return covidlistbydt

def delete_all():
    """ delete all covid data """
    conn = None
    rows_deleted = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute("DELETE FROM covcases")
        #cur.execute("DELETE FROM covcases WHERE part_id = %s", (part_id,))
        # get the number of updated rows
        rows_deleted = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted

def delete_bydate(dt,lca):
    """ delete all covid data """
    conn = None
    rows_deleted = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        #cur.execute("DELETE FROM covcases")
        cur.execute("DELETE FROM covcases WHERE date = %s and councilName = %s", (dt,lca))
        # get the number of updated rows
        rows_deleted = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted

if __name__ == '__main__':
    #insert_covidData('2020-07-01','Dabern',125,84,3)  
    #insert_covidData_list([('2020-07-01','Monash',84,33,5), ('2020-07-01','knox',65,24,3), ('2020-07-01','Glen Iris',15,3,1)])
    #print(InqcovidData())
    # print(get_CovDataByDate('2020-07-01'))
    print(get_Covlgaacasebydate())

    