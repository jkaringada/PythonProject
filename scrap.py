import requests
import bs4
import calendar
import datetime
from cdata import CVData
from dailystats import CVdailystat



def scrapWebsite(dd,mm,yyyy):
    ccaselist=[]
    base_url ='https://www.dhhs.vic.gov.au/coronavirus-update-victoria-{}-{}-{}'
    base_url1='https://www.dhhs.vic.gov.au/coronavirus-update-victoria-{}-{}{}'
    base_url2='https://www.dhhs.vic.gov.au/coronavirus-update-victoria-{}-{}'
    base_url3='https://www.dhhs.vic.gov.au/coronavirus-update-victoria-{}-{}-{}-{}'
    res= requests.get(base_url.format(str(dd),calendar.month_name[mm],str(yyyy)))
    if (res.status_code != 200):
        res= requests.get(base_url1.format(str(dd),calendar.month_name[mm],str(yyyy)))
        if (res.status_code != 200):
            res= requests.get(base_url2.format(str(dd),calendar.month_name[mm]))
            if (res.status_code !=200):
                pp=datetime.datetime.strptime(str(dd)+str(mm)+str(yyyy), "%d%m%Y").weekday()
                print(pp)
                weekd=calendar.day_name[pp]
                res= requests.get(base_url3.format(weekd,str(dd),calendar.month_name[mm],str(yyyy)))
                if (res.status_code!=200):
                    if (dd<10):
                        str1='0'+str(dd)
                    else:
                        return []    
                    res= requests.get(base_url.format(str1,calendar.month_name[mm],str(yyyy))) 
                    if (res.status_code != 200):
                        return []
    soup =bs4.BeautifulSoup(res.text,'lxml')       
    rows = soup.find("table").find("tbody").find_all("tr") 
    for row in rows:
        cells = row.find_all("td")
        if (len(cells)==0):
            continue
        lca = cells[0].get_text().strip()
        print(lca)
        print(len(cells))
        if (len(cells)==3):
            tc = cells[1].get_text().strip()
            ac = cells[2].get_text().strip()
        elif (len(cells)==2):
            tc = cells[1].get_text().strip()
            ac = ""
        else:
            tc = ""
            ac = ""    
        nwtc=tc.replace('*','')
        nwac=ac.replace('*','')
        if nwtc=="":
            nwtc=0
        if nwac=="":
            nwac=0    

        strdt=str(yyyy) + '-' + str(mm) + '-' + str(dd)
        if (lca!="LGA"):
            ccaselist.append(CVData(strdt,lca,nwtc,nwac,0))
    return  ccaselist   

def scrapkeypoints(soup):
    #lists = soup.find("div", class_="field field--name-field-dhhs-rich-text-text field--type-text-long field--label-hidden field--item").find_all("li")
    lists = soup.find("div", class_="field field--name-field-dhhs-rich-text-text field--type-text-long field--label-hidden field--item").find_all("li")
    points=[]
    for ls in lists:
        ls= ls.text.lower()
        if ('11.59pm' in ls) or ('residential address' in ls):
            break
        else:
            print(ls)
            points.append(ls)      
    return points

def scrapkeyinfor(soup,dte):
    rows = soup.find("div", class_="field field--name-field-dhhs-rich-text-text field--type-text-long field--label-hidden field--item").find_all("p")
    daillst=[]
    for k in rows:
        lst=[]
        j=k.text.lower().replace(".",'').replace(",","")
        lst=[int(s) for s in j.split() if s.isdigit()]
        j=j.lower()
        print(lst)
        if ('victoria' in j) and ('cases' in j) and('total number' in j):
            if lst[0] > lst[1]:
                tot=lst[0]
                nct=lst[1]
            else:
                tot=lst[1]
                nct=lst[0]
        elif ('outbreaks' in j) and ('investigation') in j   :
            if lst[0]> lst[1]:
                out=lst[1]
                invest=lst[0]
            else:
                out=lst[0]
                invest=lst[1]
        elif ('reclassified' in j):
            if lst[0] > lst[1]:
                net=lst[0]
                recls=lst[1]
            else:
                net=lst[1]
                recls=lst[0]
        elif ('deaths' in j) and ('died' in j):
            if 'no new deaths' in j:
                ndeath="Zero"
            else:
                r=j.split()
                ndeath = r[0]
            tdeath=lst[0]    
            break            
    daillst.append(CVdailystat(dte,tot,nct,net,recls,out,invest,ndeath,tdeath))    
    return daillst 




def scrapWebsitedaily(dd,mm,yyyy):
    ccaselist=[]
    dailylist=[]
    keylist=[]
    base_url ='https://www.dhhs.vic.gov.au/coronavirus-update-victoria-{}-{}-{}'
    res= requests.get(base_url.format(str(dd),calendar.month_name[mm],str(yyyy)))
    if (res.status_code != 200):
        if (dd<10):
            str1='0'+str(dd)
        else:
            return []    
        res= requests.get(base_url.format(str1,calendar.month_name[mm],str(yyyy))) 
        if (res.status_code != 200):
            return []
    soup =bs4.BeautifulSoup(res.text,'lxml')       
    rows = soup.find("table").find("tbody").find_all("tr") 
    for row in rows:
        cells = row.find_all("td")
        lca = cells[0].get_text().strip()
        tc = cells[1].get_text()
        ac = cells[2].get_text()
        strdt=str(yyyy) + '-' + str(mm) + '-' + str(dd)
        ccaselist.append(CVData(strdt,lca,tc,ac,0))
    dailylist=scrapkeyinfor(soup,strdt)
    keylist=scrapkeypoints(soup)    
    return  ccaselist, dailylist, keylist      