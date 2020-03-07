import urllib.request as req
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
from datetime import date
import pandas as pd
import csv
import re
#정규식
re_su=re.compile('\d+')
re_find=re.compile('~|-')
re_day=re.compile('\([월화수목금토일]\)')
re_Smonth=re.compile('\d+[월.]')
re_Fmonth=re.compile('\d+[월.]')
re_Sdate=re.compile('\d+')
re_Fdate=re.compile('\d+일+')
checks = re.compile('(\d+[월.]\d+일*\(*[월화수목금토일]*\)*[\~\-]\d*[월.]*\d+일*\(*[월화수목금토일]*\)*)|(\d+[월.]\d+[^도]일*\(*[월화수목금토일]*\)*)')
Time=re.compile('\d{2}:\d{2}')
re_Address=re.compile('[가-힣]{1,3}구+\(*[가-힣]+[로동]\d*[번지길]*[\-\d]*\,*[가-힣\d]*\)*')
re_Time_all=re.compile('\d+[:;]\d+[-~]\d+[:;]\d+|\d+[:;]\d+')
pattern = re.compile(r'\s+')#공백제거 정규식
#URL에 대한 고민은 전제하고, 하나의 사이트에서 처리 루틴을 정리
target_url = 'http://www.busan.go.kr/corona19/index'
res=req.urlopen(target_url)
# 파싱 > 구글에 bs4검색해서 컨트롤+f 해서 parser검색해서 종류 뭐뭐 있는지 본다
soup=BeautifulSoup(res,'html5lib')

# 장원 추가 코드, 현재 확진자 수릂 파악해서 변수에 담는다.
totalPatient = int(soup.select_one('#header div.main_banner span.item2').text[:-1])

#df생성
df = pd.DataFrame(columns=['No','Age','Sex','Gu','SMonth','SDate','Sday','FMonth','FDate','Fday','STime','FTime','Place','Address','Routing'])#15
# time.sleep(2)
#12,13
STime=list()
FTime=list()
Place=list()
Routing=list()
SMonth=list()
SDate=list()
Sday=list()
FMonth=list()
FDate=list()
Fday =list()


for i in range(1,totalPatient+1):     # 전체 환자수만큼 크롤링
    # time.sleep(1)
    # No부터 Gu까지 추출 및 가져오기 a
    #contents > div:nth-child(1) > div > div.list_body > ul:nth-child(1) > li:nth-child(1)
    #contents > div:nth-child(1) > div > div.list_body > ul:nth-child(1) > li:nth-child(1)
    #contents > div:nth-child(1) > div > div.list_body > ul:nth-child(2) > li:nth-child(1)
    #contents > div:nth-child(1) > div > div.list_body > ul:nth-child(2) > li:nth-child(1)
    info=soup.select('#contents > div:nth-child(1) > div > div.list_body > ul:nth-child('+str(i)+') > li:nth-child(1) > span')
    # print(info)
    # break
    d=info[0].text
    
    c=d.replace(' ','').replace('<span>','').replace('</span>','').replace(')','').replace('(','/').replace('\'','/')
    f=c.split('/')
    
    No=f[0]
    Age=f[1]
    Sex=f[2]
    Gu=f[3]
    #No부터 Gu까지 추출 및 가져오기 
    
    ps=soup.select('#contents > div:nth-child(1) > div > div.list_body > ul:nth-child('+str(i)+') > li.result')
    oh1=ps[0]
    ps_del=oh1.text
    ps_del = re.sub(pattern, '', ps_del).replace('\u200b','')
    # print(ps_del)
    if len(ps_del) <= 6:
        SMonth='확인중'
        SDate='확인중'
        Sday='확인중'
        FMonth='확인중'
        FDate='확인중'
        Fday='확인중'
        STime='확인중'
        FTime='확인중'
        Place='확인중'
        Address='없음'
        Routing='확인중'
        print(No,Age,Sex,Gu,SMonth,SDate,Sday,FMonth,FDate,Fday,STime,FTime,Place,Address,Routing)
        stat_S=[No,Age,Sex,Gu,SMonth,SDate,Sday,FMonth,FDate,Fday,STime,FTime,Place,Address,Routing]
        df.loc[len(df)] = stat_S
        # print(No,Age,Sex,Gu,Sm,Sd,Fm,Fd,Date,Stime,Ftime,Place)
        # stat_S=[No,Age,Sex,Gu,Date,Time,Place]
        # df.loc[len(df)] = stat_S
    else:
        b=re.split(checks, ps_del)
        # print(b)
        del b[0]
        all_=list()
        for i in b:
            if i != None :
                all_.append(i)
            else:   
                pass
        # print(len(all_),all_)
        STime='00:00'
        FTime='00:00'
        Routing=''
        tmp123=list()
        for i in range(0,len(all_),2):
            #########날짜 찾기 완성############
            tmp123=all_[i]
            a=re.split(re_find,tmp123)
            if len(a) == 1:#[2월3일(금)]
                b=re.findall(re_Smonth, a[0])#[2월] findall로 찾기
                oh=re.findall(re_su,b[0])#[2월]에서숫자만 가져오기 2 됨
                if len(oh) == 0:
                    oh=['nan']
                SMonth=oh[0]
                b=re.split(re_Smonth, a[0])#[2월] 스플릿 ['','3일(금)]
                chang=re.findall(re_Sdate,b[1])#남은 숫자는 일밖에 없으니깐 일은 그냥 바로 숫자로 가져오기
                if len(chang) == 0:
                    chang=['nan']
                SDate=chang[0]
                FMonth=SMonth
                FDate=SDate
                suk=re.findall(re_day,b[1]) #요일 #완료!!
                if len(suk) == 0:
                    suk=['nan']
                Sday=suk[0]
                Fday=Sday
                # print(No,Age,Sex,Gu,SMonth,SDate,Sday,FMonth,FDate,Fday'1')
                
            else: # [2월3일(금),2월4일(토)]
                b=re.findall(re_Smonth, a[0])#[2월] findall로 찾기
                oh=re.findall(re_su,b[0])#[2월]에서숫자만 가져오기 2 됨
                if len(oh) == 0:
                    oh=['nan']
                SMonth=oh[0]
                b=re.split(re_Smonth, a[0])#[2월] 스플릿 ['','3일(금)]
                chang=re.findall(re_Sdate,b[1])#남은 숫자는 일밖에 없으니깐 일은 그냥 바로 숫자로 가져오기
                if len(chang) == 0:
                    chang=['nan']
                SDate=chang[0]
                suk=re.findall(re_day,b[1]) #요일 #완료!!
                if len(suk) == 0:
                    suk=['nan']
                Sday=suk[0]
                chang=re.split(re_Smonth, a[1])

                if len(chang)==1:#끝난 날짜[2월4일(토)]인데 'x월'이 없거나 x'일'<이없는경우 1, 월을 기준으로 쪼개서 len확인
                    #앞에 월이 없는경우
                    FMonth=SMonth
                    oh=re.findall(re_Sdate,chang[0])
                    if len(oh) == 0:
                        oh=['nan']
                    FDate=oh[0]
                    chang=re.findall(re_day,chang[0])
                    if len(chang) == 0:
                        chang=['nan']
                    Fday=chang[0]
                    # print(No,Age,Sex,Gu,SMonth,SDate,Sday,FMonth,FDate,Fday,STime,FTime,Place,Address,Routing,'2')
                else:
                    #앞에 월이 있는경우
                    #a[1]=[2월4일(토)]
                    b=re.findall(re_Smonth, a[1])
                    oh=re.findall(re_su,b[0])
                    if len(oh) == 0:
                        oh=['nan']
                    FMonth=oh[0]
                    b=re.split(re_Smonth, a[1])
                    chang=re.findall(re_Sdate,b[1])
                    if len(chang) == 0:
                        chang=['nan']
                    FDate=chang[0]
                    suk=re.findall(re_day,b[1])
                    if len(suk) == 0:
                        suk=['nan']
                    Fday=suk[0]
                    # print(No,Age,Sex,Gu,SMonth,SDate,Sday,FMonth,FDate,Fday,STime,FTime,Place,Address,Routing,'3')
            #########날짜 찾기 완성############
            tmp=all_[i+1].split('⇒')#>방향으로 쪼개기
            for cut in tmp:
                # print(cut)
                chang=re.split(re_Time_all, cut)
                # print(chang,len(chang))
                # print(chang)
                if len(chang)==1:#['자택'],['버스']처럼 숫자가 없는 애들
                    STime=FTime
                    Place=chang[0]
                    Address='없음'
                    Routing=chang[0]
                    print(No,Age,Sex,Gu,SMonth,SDate,Sday,FMonth,FDate,Fday,STime,FTime,Place,Address,Routing,'1')
                    stat_S=[No,Age,Sex,Gu,SMonth,SDate,Sday,FMonth,FDate,Fday,STime,FTime,Place,Address,Routing]
                    df.loc[len(df)] = stat_S
                else: #앞에 숫자 (시간 00:00)가 있는애들
                    # print('cut',cut,len(cut))
                    TA=re.findall(re_Time_all, cut) 
                    # print('TA',TA,len(TA))      
                    Cck=re.split(re_find, TA[0])
                    # print('Cck',Cck,len(Cck))
                    if len(Cck)==1:
                        STime=Cck[0]
                        FTime=STime
                        seok=re.findall(re_Address,chang[1])
                        if len(seok) == 0:
                            seok=['없음']
                        Address=seok[0]
                        P1=re.split(re_Address, chang[1])
                        qw=''
                        for i in P1:
                            qw=qw+i
                        Place=qw
                        print(No,Age,Sex,Gu,SMonth,SDate,Sday,FMonth,FDate,Fday,STime,FTime,Place,Address,Routing,'2')
                        stat_S=[No,Age,Sex,Gu,SMonth,SDate,Sday,FMonth,FDate,Fday,STime,FTime,Place,Address,Routing]
                        df.loc[len(df)] = stat_S
                    else:#시간 2개인애들([00:00],[00:00])
                        STime=Cck[0]
                        FTime=Cck[1]
                        # print('chang[1]',chang[1],type(chang[1]),len(chang[1]))
                        seok=re.findall(re_Address,chang[1])
                        if len(seok) == 0:
                            seok=['없음']
                        Address=seok[0]
                        P1=re.split(re_Address, chang[1])
                        qw=''
                        for i in P1:
                            qw=qw+i
                        Place=qw
                        # print('qw',qw)
                        print(No,Age,Sex,Gu,SMonth,SDate,Sday,FMonth,FDate,Fday,STime,FTime,Place,Address,Routing,'3')
                        stat_S=[No,Age,Sex,Gu,SMonth,SDate,Sday,FMonth,FDate,Fday,STime,FTime,Place,Address,Routing]
                        df.loc[len(df)] = stat_S
print('저장하기')                      
df.to_csv('my_csv.csv', mode='w', header=True)
print('저장완료')                      