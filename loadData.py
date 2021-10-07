from cdata import CVData
from scrap import scrapWebsite, scrapWebsitedaily
from datetime import datetime, timedelta
from iData import get_CovDataByDate, get_CovActiveCaseByDate, insert_covidData, get_Covlgaacasebydate, delete_all,insert_statsdata,insertnotesdata


def buildBlock():

    cvlist=[]
    actcase={}
    dd=datetime.date(datetime.now()).day
    mm=datetime.date(datetime.now()).month
    yyyy=datetime.date(datetime.now()).year
    cvlist=scrapWebsite(dd,mm,yyyy)
    # dldate= datetime.date(datetime.today() - timedelta(days=1))
    # dtless= str(dldate.year)+ '-' + str(dldate.month) + '-' + str(dldate.day)
    actcase=get_Covlgaacasebydate()
    for cv in cvlist:
        if len(actcase)==0:
            insert_covidData(cv.cvdate,cv.lca,cv.acase,cv.tcase,0)
        else:
            if cv.lca in actcase.keys():
                num1=cv.acase - actcase[cv.lca]
                insert_covidData(cv.cvdate,cv.lca,cv.acase,cv.tcase,num1)
            else:
                insert_covidData(cv.cvdate,cv.lca,cv.acase,cv.tcase,0)

def buildBlockByDate(strdate):

    cvlist=[]
    actcase={}
    dtlist=strdate.split("-")
    dd=dtlist[0]
    mm=dtlist[1]
    yyyy=dtlist[2]
    cvlist=scrapWebsite(int(dd),int(mm),int(yyyy))
    # dldate= datetime.date(datetime.today() - timedelta(days=1))
    # dtless= str(dldate.year)+ '-' + str(dldate.month) + '-' + str(dldate.day)
    actcase=get_Covlgaacasebydate()
    for cv in cvlist:
        if len(actcase)==0:
            insert_covidData(cv.cvdate,cv.lca,cv.acase,cv.tcase,0)
        else:
            if cv.lca in actcase.keys():
                num1=int(cv.acase) - actcase[cv.lca]
                insert_covidData(cv.cvdate,cv.lca,cv.acase,cv.tcase,num1)
            else:
                insert_covidData(cv.cvdate,cv.lca,cv.acase,cv.tcase,0)               

def buildallByDate(strdate):

    cvlist=[]
    actcase={}
    statcase=[]
    notes=[]
    dtlist=strdate.split("-")
    dd=dtlist[0]
    mm=dtlist[1]
    yyyy=dtlist[2]
    cvlist, statcase, notes  =scrapWebsitedaily(int(dd),int(mm),int(yyyy))
    # dldate= datetime.date(datetime.today() - timedelta(days=1))
    # dtless= str(dldate.year)+ '-' + str(dldate.month) + '-' + str(dldate.day)
    actcase=get_Covlgaacasebydate()
    for cv in cvlist:
        if len(actcase)==0:
            insert_covidData(cv.cvdate,cv.lca,cv.acase,cv.tcase,0)
        else:
            if cv.lca in actcase.keys():
                num1=cv.acase - actcase[cv.lca]
                insert_covidData(cv.cvdate,cv.lca,cv.acase,cv.tcase,num1)
            else:
                insert_covidData(cv.cvdate,cv.lca,cv.acase,cv.tcase,0)
    for st in statcase:
        insert_statsdata(st)
    for nt in notes:
        print(nt)
        insertnotesdata(nt)    




def dateRangeBuild(startday,startmonth,endday,endmonth):
    yyyy=2020
    for mm in range(startmonth,endmonth+1):
        for dd in range(startday, endday+1):
            cvlist=scrapWebsite(dd,mm,yyyy)
            # dldate= datetime.date(datetime.today() - timedelta(days=1))
            # dtless= str(dldate.year)+ '-' + str(dldate.month) + '-' + str(dldate.day)
            actcase=get_Covlgaacasebydate()
            for cv in cvlist:
              #print(cv.lca)  
              if len(actcase)==0:
                 insert_covidData(cv.cvdate,cv.lca,cv.acase,cv.tcase,0)
              else:
                  if cv.lca in actcase.keys():
                     print(cv.cvdate) 
                     print(cv.lca)
                     print(cv.acase)
                     print(actcase[cv.lca])  
                     num1=int(cv.acase) - actcase[cv.lca]
                     insert_covidData(cv.cvdate,cv.lca,cv.acase,cv.tcase,num1)
                  else:
                     insert_covidData(cv.cvdate,cv.lca,cv.acase,cv.tcase,0)


if __name__ == '__main__':
    #insert_covidData('2020-07-01','Dabern',125,84,3)  
    #insert_covidData_list([('2020-07-01','Monash',84,33,5), ('2020-07-01','knox',65,24,3), ('2020-07-01','Glen Iris',15,3,1)])
    #print(InqcovidData())
    # print(get_CovDataByDate('2020-07-01'))
    #delete_all()
    #print(buildallByDate('09-5-2020'))
    #print(buildBlockByDate('31-5-2020'))
    print(dateRangeBuild(1,8,21,8))    


