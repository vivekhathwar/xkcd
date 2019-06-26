from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.parse, ssl, os,sqlite3,time
ctx= ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode=ssl.CERT_NONE

url="https://www.xkcd.com/"
integ=1
exceptions=[404,1350,1416,1525,1608,1663,2067]
con=sqlite3.connect('xkcd.db')
con.executescript('''
create table if not exists imageDescription(
id integer not null primary key autoincrement unique,
title text,
description text,
name text
);
''')

while integ<2168:
    u=url+str(integ)+'/'
    if integ in exceptions:
        print("This is an interactive page, visit click on the below url to enjoy:")
        integ+=1
        print(u)
        fn="page"+str(integ)+".html"
        try:
            urllib.request.urlretrieve(u,os.path.basename(fn))
        except:
            pass
        continue
    html=urllib.request.urlopen(u,context=ctx).read()
    soup=BeautifulSoup(html,'html.parser')
    tit=soup.find('div',id='comic').find('img')
    title=tit.get('alt')
    descript=tit.get('title')
    imageURL='https:'+tit.get('src')
    existance=con.execute('select id from imageDescription where title=?',(title,)).fetchone()
    if (existance!=None):
        print("Image",integ,"exists")
        integ+=1
        continue
    urllib.request.urlretrieve(imageURL,os.path.basename(imageURL))
    con.execute('''insert into imageDescription (title, description, name) values(?,?,?)''',(title,descript,imageURL,))
    print("Scraped ",title," comic number ",integ)
    integ+=1
    con.commit()
    if(integ%100==0):
        print("Ondu chikka viraama!")
        time.sleep(5)
