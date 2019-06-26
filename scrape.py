#Import Statements
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.parse, ssl, os,sqlite3,time
#To make the code scrape 'https' page
ctx= ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode=ssl.CERT_NONE

url="https://www.xkcd.com/"
integ=1

exceptions=[404,1350,1416,1525,1608,1663,2067] #these are the interactive comic pages
#database connection and table creation 
con=sqlite3.connect('xkcd.db')
con.executescript('''
create table if not exists imageDescription(
id integer not null primary key autoincrement unique,
title text,
description text,
name text
);
''')

#parsing through all pages
while integ<2168:
    u=url+str(integ)+'/'
    if integ in exceptions:#interactive page error
        print("This is an interactive page, visit click on the below url to enjoy:")
        integ+=1
        print(u)
        fn="page"+str(integ)+".html"
        try:# to handle https://xkcd.com/404/ page
            urllib.request.urlretrieve(u,os.path.basename(fn))
        except:
            pass
        continue
    #Webscraping
    html=urllib.request.urlopen(u,context=ctx).read()
    soup=BeautifulSoup(html,'html.parser')
    tit=soup.find('div',id='comic').find('img')
    title=tit.get('alt')
    descript=tit.get('title')
    imageURL='https:'+tit.get('src')
    existance=con.execute('select id from imageDescription where title=?',(title,)).fetchone()#restartable condition
    if (existance!=None):
        print("Image",integ,"exists")
        integ+=1
        continue
    #Saving the image
    urllib.request.urlretrieve(imageURL,os.path.basename(imageURL))
    #Saving the data of stored image in the database
    con.execute('''insert into imageDescription (title, description, name) values(?,?,?)''',(title,descript,imageURL,))
    print("Scraped ",title," comic number ",integ)
    integ+=1
    con.commit()
    #Pause clause
    if(integ%100==0):
        print("Ondu chikka viraama!")
        time.sleep(5)
con.close()
