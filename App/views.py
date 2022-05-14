from django.shortcuts import redirect, render
from bs4 import BeautifulSoup
import requests
from collections import Counter
from urllib.parse import urljoin
from .models import page, history

# Create your views here.
def GetContent(URL,url):
    webpage = requests.get(URL+url)
    parsed = BeautifulSoup(webpage.content, "html5lib")

    creator = parsed.find("div", class_ ='pw-author')
    name = parsed.find("h1", class_ ='pw-post-title')
    published_date = parsed.find("p", class_ ='pw-published-date')
    reading_time = parsed.find("div", class_ ='pw-reading-time')
    content = parsed.find("article")
    # urls = parsed.find_all("a")

    # for i in urls:
    #     print(i.get("href"))


    if creator==None:
        creator = " "
    else:
        creator = creator.text
    if name==None:
        name = " "
    else:
        name = name.string.strip()
    if published_date==None:
        published_date = " "
    else:
        published_date = published_date.string
    if reading_time==None:
        reading_time = " "
    else:
        reading_time = reading_time.string
    if content==None:
        content = " "
    else:
        content = content.text

    symbol = [".", ",", ":", ")", "(", "?", "’", "'", "!", "&", "_", "-", ";"]

    for i in symbol:
        content = " ".join(content.split(i))

    content = content.split(" ")
    content = list((map(lambda x: x.lower(), content)))
    # print(stop_words)
    # print(content)
    # unique_words=[]
    # unique_words = Counter(unique_words)
    # unique_words = sorted(unique_words.items(), key=lambda item: (-item[1], item[0]))

    # print(unique_words[0:10])
    # print(creator)
    # print(name)
    # print(published_date)
    # print(reading_time)

    return creator,name,published_date,reading_time

def index(request):
    print(request)
    records = page.objects.all()
    records.delete()
    if request.method=='POST':
        ta = request.POST.get('tag', "")
        URL = "https://medium.com/tag/"+ta
        webpage = requests.get(URL)
        parsed = BeautifulSoup(webpage.content, "html5lib")
        pages = []
        articles = parsed.find_all("article")
        

        if history.objects.filter(tag = ta).exists()==False:
            his = history.objects.create(tag=ta)
            his.save()

        for i in articles:
            url = i.findAll("a")[-1].get('href')
            print(url)
            
            if url[0]=="/":
                creator,name,published_date,reading_time=GetContent("https://medium.com",url)
                if  creator!=" " and name!=" " and published_date!=" " and reading_time!=" ":
                    print("https://medium.com"+url)
                    if creator.endswith("Follow"):
                            creator=creator[0:len(creator)-6]
                    # print(unique_words[0:10])
                    print(creator)
                    print(name)
                    print(published_date)
                    print(reading_time)

                    p = page()

                    p.num = len(pages)+1
                    p.link = "https://medium.com"+url
                    p.creator = creator
                    p.name = name
                    p.published_date = published_date
                    p.reading_time = reading_time

                    page.objects.create(num=p.num, link=p.link, creator=p.creator, name=p.name, published_date=p.published_date, reading_time=p.reading_time)
                    p.save()
                    pages.append(p)
                    # if len(pages)==2:
        return render(request,'index.html',{'pages':pages,"link":"https://medium.com"+url,"creator":creator,"name":name,"published_date":published_date,"reading_time":reading_time})
    else:
        return render(request,'index.html')

def getpage(request):
    data = page.objects.get()
    return render(request,"index.html",{{'data':data}})

def History(request):
    data = history.objects.all()
    return render(request,"history.html",{"data" : data})