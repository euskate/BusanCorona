import os 
import pandas as pd
import numpy as np 
import folium 
from folium import plugins
from folium.plugins import MarkerCluster
import re
import json
import random

# 부산지하철 이름 및 위도 경도 불러오기
sub=pd.read_csv('./Busan_subway.csv')

# 행정구 나누는 데이터 불러오기
with open('./Busan_gu.json',mode='rt',encoding='utf-8') as k:
  busan_gu=json.loads(k.read())

# 구청 데이터 불러오기(확진자 비율, 명수 포함되어 있음)
gu_info=pd.read_csv('./Gucheong_info(20_03_06).csv')

# 확진자 데이터 불러오기
definite=pd.read_csv('./patient_info(20_03_06).csv')

#----------------------------------------------------------------------------------------------

# 맵 생성
busan_div = folium.Map(location=[35.137922,129.055628], zoom_start=13, max_zoom=17, min_zoom=10)

# 구청자료에 있는 확진자 데이터 가지고 오기
# for i in range(len(gu_info)):
#   if gu_info['count'][i]==0:
#     gu_info['count'][i]= None
gu_info['count'] = gu_info['count'].astype('float')

# busan_gu와 gu_info 의 구 이름 맞춰주기
# for i in range(len(gu_info)):
#   gu_info['Name'][i]=gu_info['Name'][i][:-1]

gu_info['Name'] = gu_info.Name.str.slice(0,-1)

# 음영생성
folium.Choropleth(
  geo_data=busan_gu,
    name='구별 확진자 수(음영)',
    data=gu_info,
    columns=['Name', 'count'],
    key_on='feature.properties.name',
    fill_color='Reds',
    fill_opacity=0.4,

    line_opacity=1,
    line_weight=2,
    nan_fill_opacity=0,
    legend_name='구별 확진자 수'
).add_to(busan_div)

#----------------------------------------------------------------------------------------------


# 지하철 layer 생성
subway = folium.FeatureGroup(name="지하철")
# 지하철 간 라인 생성
# 1호선
for i in range(0,39):
  p1=[sub[sub['호선']=='1호선']['위도'][i],sub[sub['호선']=='1호선']['경도'][i]]
  p2=[sub[sub['호선']=='1호선']['위도'][i+1],sub[sub['호선']=='1호선']['경도'][i+1]]
  subway.add_child(folium.PolyLine([p1,p2], color="#F6531B", weight=5, opacity=0.8))
  busan_div.add_child(subway)
# 2호선
for i in range(40,82):
  p1=[sub[sub['호선']=='2호선']['위도'][i],sub[sub['호선']=='2호선']['경도'][i]]
  p2=[sub[sub['호선']=='2호선']['위도'][i+1],sub[sub['호선']=='2호선']['경도'][i+1]]
  subway.add_child(folium.PolyLine([p1,p2], color="#47DD77", weight=5, opacity=0.8))
  busan_div.add_child(subway)
# 3호선
for i in range(83,99):
  p1=[sub[sub['호선']=='3호선']['위도'][i],sub[sub['호선']=='3호선']['경도'][i]]
  p2=[sub[sub['호선']=='3호선']['위도'][i+1],sub[sub['호선']=='3호선']['경도'][i+1]]
  subway.add_child(folium.PolyLine([p1,p2], color="#ECBC26", weight=5, opacity=0.8))
  busan_div.add_child(subway)
# 4호선
for i in range(100,113):
  p1=[sub[sub['호선']=='4호선']['위도'][i],sub[sub['호선']=='4호선']['경도'][i]]
  p2=[sub[sub['호선']=='4호선']['위도'][i+1],sub[sub['호선']=='4호선']['경도'][i+1]]
  subway.add_child(folium.PolyLine([p1,p2], color="#2683EC", weight=5, opacity=0.8))
  busan_div.add_child(subway)
# 김해경전철
for i in range(114,134):
  p1=[sub[sub['호선']=='김해경전철']['위도'][i],sub[sub['호선']=='김해경전철']['경도'][i]]
  p2=[sub[sub['호선']=='김해경전철']['위도'][i+1],sub[sub['호선']=='김해경전철']['경도'][i+1]]
  subway.add_child(folium.PolyLine([p1,p2], color="#3B1ACC", weight=5, opacity=0.8))
  busan_div.add_child(subway)
# 동해선
for i in range(135,148):
  p1=[sub[sub['호선']=='동해선']['위도'][i],sub[sub['호선']=='동해선']['경도'][i]]
  p2=[sub[sub['호선']=='동해선']['위도'][i+1],sub[sub['호선']=='동해선']['경도'][i+1]]
  subway.add_child(folium.PolyLine([p1,p2], color="#B42BA7", weight=5, opacity=0.8))
  busan_div.add_child(subway)


# 라인 간 화살표 및 마커 생성
# 1호선
for i in range(0,40):
    # 지하철 마커생성
  subway.add_child(folium.CircleMarker(
  location=[sub[sub['호선']=='1호선']['위도'][i], sub[sub['호선']=='1호선']['경도'][i]],radius=3, color="#F6471B", 
  fill_color='#FFFFFF', fill=True,opacity=1,))
  busan_div.add_child(subway)
# 2호선
for i in range(41,83):
    # 지하철 마커생성
  subway.add_child(folium.CircleMarker(
  location=[sub[sub['호선']=='2호선']['위도'][i],sub[sub['호선']=='2호선']['경도'][i]], radius=3, color='#2CBF5A', 
  fill_color='white', fill=True,opacity=1))
  busan_div.add_child(subway)
# 3호선
for i in range(83,100):
    # 지하철 마커생성
  subway.add_child(folium.CircleMarker(
  location=[sub[sub['호선']=='3호선']['위도'][i],sub[sub['호선']=='3호선']['경도'][i]], radius=3, color='#E1A411', 
  fill_color='white', fill=True,opacity=1))
  busan_div.add_child(subway)
# 4호선
for i in range(100,114):
  #지하철 마커생성
  subway.add_child(folium.CircleMarker(
  location=[sub[sub['호선']=='4호선']['위도'][i],sub[sub['호선']=='4호선']['경도'][i]], radius=3,color='#2683EC', 
  fill_color='white', fill=True,opacity=1))
  busan_div.add_child(subway)
# 김해경전철
for i in range(114,135):
  #지하철 마커생성
  subway.add_child(folium.CircleMarker(
  location=[sub[sub['호선']=='김해경전철']['위도'][i],sub[sub['호선']=='김해경전철']['경도'][i]], radius=3,color='#3B1ACC', 
  fill_color='white', fill=True,opacity=1))
  busan_div.add_child(subway)
# 동해선
for i in range(135,149):
  #지하철 마커생성
  subway.add_child(folium.CircleMarker(
  location=[sub[sub['호선']=='동해선']['위도'][i], sub[sub['호선']=='동해선']['경도'][i]], radius=3,color='#B42BA7', 
  fill_color='white', fill=True,opacity=1))
  busan_div.add_child(subway)

Gu=folium.FeatureGroup(name="구청(구별 확진자 수)")
# 구청에 마커생성
for i in range(len(gu_info)):
  popup = folium.Popup(html=f"{gu_info.Address[i].split()[1]} 확진자 {gu_info['count'].fillna(0).astype(int)[i]} 명", max_width=200)
  Gu.add_child(folium.Marker( location=[gu_info['Longitude'][i], gu_info['Latitude'][i]],\
                icon=folium.Icon(color='green',icon='simplybuilt',prefix='fa'),popup=popup))
  busan_div.add_child(Gu)
#----------------------------------------------------------------------------------------------

from functions import get_arrows, get_bearing, bfs
from collections import deque

# 1- station 클래스를 만듭시다.
class Station:
    # 초기값 설정 생성자를 통해 인스턴스 변수들을 생성, 설정해 줍니다.
    def __init__(self, name):
        self.name = name
        # 이웃 역들을 담고 있는 리스트
        self.neighbor = []

    def add_connection(self, another_station):
        self.neighbor.append(another_station)
        another_station.neighbor.append(self)

# 2- 파일 읽기

# station 사전 만들기 - station 사전을 만드는 이유는 각각의 역 이름과 각 역에 담긴 정보들(Station 클래스의 인스턴스)을 key - value 값으로 입력하기 위함입니다.
stations = {}

# station 파일을 읽어봅시다.
in_file = open("./busan_jiha.txt",encoding="utf-8")

# add_connection 메소드를 활용하기 위해 이전 역과 현재 역으로 구분 시켜줄 필요가 있습니다.
# 물론, 현재 이전역은 없는 상태이므로 None으로 지정해줍니다.
previous_station = None

for line in in_file:
    temporary_line = line.strip().split("-")

    # 리스트를 각각의 역으로 변환시키고, 공백을 없애주기 위해 이중 반복문을 활용합시다.
    for line in temporary_line:
        station_line = line.strip()

        # current_station을 현재역의 정보를 담고있는 인스턴스 값으로 지정해줍니다.
        current_station = Station(station_line)

        # 각각의 역의 이름을 stations 사전의 key값으로 입력하는게 목적이었으므로
        # 아래와 같이 코드를 작성합니다.
        if station_line not in stations.keys():
        
            # 현재 역의 이름을 key값으로, 그 역의 정보(인스턴스)를 value로 저장합니다.
            stations[station_line] = current_station

        # 각 호선당 중복되는 역(환승 역)일 경우 에러가 발생하므로 경우를 나눠줘야 합니다.
        # 현재역은 이전에 정해줬던 역의 value값임을 선언해줘야
        # 자동 환승을 합니다. station[station_line] = current_station 으로 지정 할 경우
        # 환승하지 않습니다!
        elif station_line in stations.keys():
            current_station = stations[station_line]


        # 이전 역과 현재 역을 이웃역으로 엮어줘야 하나, 현재 이전 역은 None 이므로, 아래와 같이 조건문을 활용합니다.
        if previous_station != None:
            current_station.add_connection(previous_station)

        # 반복문을 돌면서 모든 역을 사전에입력시켜줘야 하므로 아래와 같이 코드를 작성합니다.
        previous_station = current_station

in_file.close()

#----------------------------------------------------------------------------------------------

# 확진자 지도
marker_cluster = MarkerCluster(popups='확진자 방문 장소',name='확진자 방문 횟수', overlay=True,control=True).add_to(busan_div)
Total=folium.FeatureGroup(name="전체 확진자 동선")
Week2=folium.FeatureGroup(name="최근 이주일 확진자 동선")
want_date=['21','22','23','24','25','26','27','28','29','1','2','3','4','5','6']
tooltip='정보 보기'

for Number in range(1,len(definite['No'].unique())+1):
  r = lambda: random.randint(0,255)
  color_r='#%02X%02X%02X' % (r(),r(),r())
  one=definite[definite['No']=='부산-{0}'.format(Number)]  
  one_num='부산-'+str(Number)
  one_month=list(one['SMonth'].unique())
  one_day=list(one['SDate'].unique())
  day_len=len(one['SDate'].unique())

  for i in range(day_len):
    tmp=one[one['SDate']==one_day[i]]
    check=tmp['SDate'].unique()[0]
    date1 = one_day[i]
    
    if check in want_date: # 최근 일주일 이내에 발생한 경우
    
      one_coordis=[]
      place1=[]
      address1=[]
      a=0
      for index in tmp['latitude'].index:
        place2= tmp['Place'][index]
        if tmp['latitude'][index]==0:
          if tmp['Place'][index] =='도시철도':#철도 탄거 어펜드해야함
            
            start_name = tmp['D_sub'][index]
            goal_name = tmp['S_sub'][index]

            if start_name=='없음':

              sub_index=sub[sub['역명']==goal_name].index
              sub_lat=sub[sub['역명']==goal_name]['경도'][sub_index[0]]
              sub_lon=sub[sub['역명']==goal_name]['위도'][sub_index[0]]
              sub_coordi=[sub_lon,sub_lat]
              one_coordis.append(sub_coordi)
              a+=1
            elif goal_name=='없음':

              sub_index=sub[sub['역명']==start_name].index
              sub_lat=sub[sub['역명']==start_name]['경도'][sub_index[0]]
              sub_lon=sub[sub['역명']==start_name]['위도'][sub_index[0]]
              sub_coordi=[sub_lon,sub_lat]
              one_coordis.append(sub_coordi)
              a+=1

            elif start_name!='없음' and goal_name!='없음':

              start = stations[start_name]
              goal = stations[goal_name]

              path = bfs(start, goal)
              for station in path:
                sub_index=sub[sub['역명']==station.name].index
                sub_lat=sub[sub['역명']==station.name]['경도'][sub_index[0]]
                sub_lon=sub[sub['역명']==station.name]['위도'][sub_index[0]]
                sub_coordi=[sub_lon,sub_lat]
                # print(sub_coordi)
                one_coordis.append(sub_coordi)
                a+=1



        elif tmp['latitude'][index]!=0:
          coordi=[tmp['longitude'][index],tmp['latitude'][index]]
          one_coordis.append(coordi)
          place1.append(tmp['Place'][index])
          address1.append(tmp['Address'][index])
      
      try:
          Week2.add_child(folium.PolyLine(one_coordis, color=color_r, weight=1.5, opacity=1))
      except:
          pass
      busan_div.add_child(Week2)

      for seq in range(0,len(tmp[tmp['latitude']!=0].index)):
        Week2.add_child(folium.CircleMarker(one_coordis[seq],radius=2,color='red',tooltip=tooltip,popup=folium.Popup(
        '확진자:{0},날짜:{1}일, 장소:{2},주소:{3}'.format(one_num,date1,place1[seq],address1[seq]),
        parse_html=True,max_width=450)))
        busan_div.add_child(Week2)
        for length in range(len(one_coordis)-1):
          p1=[one_coordis[length][0], one_coordis[length][1]]
          p2=[one_coordis[length+1][0], one_coordis[length+1][1]]
          defi_arrows = get_arrows(color='black', size=1.5,locations=[p1,p2], n_arrows=2)
          for defi_arrow in defi_arrows:
            Week2.add_child(defi_arrow)
            busan_div.add_child(Week2)
        
    else: # 최근 일주일이 아닌 경우(전체)
      a=0
      one_coordis=[]
      place1=[]
      address1=[]
      for index in tmp['latitude'].index:
        place2= tmp['Place'][index]
        if tmp['latitude'][index]==0:
          if tmp['Place'][index] =='도시철도':#철도 탄거 어펜드해야함
            
            start_name = tmp['D_sub'][index]
            goal_name = tmp['S_sub'][index]

            if start_name=='없음':

              sub_index=sub[sub['역명']==goal_name].index
              sub_lat=sub[sub['역명']==goal_name]['경도'][sub_index[0]]
              sub_lon=sub[sub['역명']==goal_name]['위도'][sub_index[0]]
              sub_coordi=[sub_lon,sub_lat]
              one_coordis.append(sub_coordi)
              a+=1
            elif goal_name=='없음':

              sub_index=sub[sub['역명']==start_name].index
              sub_lat=sub[sub['역명']==start_name]['경도'][sub_index[0]]
              sub_lon=sub[sub['역명']==start_name]['위도'][sub_index[0]]
              sub_coordi=[sub_lon,sub_lat]
              one_coordis.append(sub_coordi)
              a+=1
            elif start_name!='없음' and goal_name!='없음':

              start = stations[start_name]
              goal = stations[goal_name]

              path = bfs(start, goal)
              for station in path:
                sub_index=sub[sub['역명']==station.name].index
                sub_lat=sub[sub['역명']==station.name]['경도'][sub_index[0]]
                sub_lon=sub[sub['역명']==station.name]['위도'][sub_index[0]]
                sub_coordi=[sub_lon,sub_lat]
                # print(sub_coordi)
                one_coordis.append(sub_coordi)
                # print("지하철 추가했을때")
                a+=1


        elif tmp['latitude'][index]!=0:
          coordi=[tmp['longitude'][index],tmp['latitude'][index]]
          one_coordis.append(coordi)
          place1.append(tmp['Place'][index])
          address1.append(tmp['Address'][index])
    #   print('지하철 때',one_coordis,len(one_coordis))
      try:
          Total.add_child(folium.PolyLine(one_coordis, color=color_r, weight=1.5, opacity=1))
      except: 
          pass
      busan_div.add_child(Total)
      for length in range(len(one_coordis)-1):
        p1=[one_coordis[length][0], one_coordis[length][1]]
        p2=[one_coordis[length+1][0], one_coordis[length+1][1]]
        defi_arrows = get_arrows(color='black', size=1.5,locations=[p1,p2], n_arrows=2)
        for defi_arrow in defi_arrows:
          Total.add_child(defi_arrow)
          busan_div.add_child(Total)

      for seq in range(len(one_coordis)-a):
        # print('CircleMarker일때',one_coordis)
        # print("one_coordis:",len(one_coordis))
        # print("one_coordis:",len(one_coordis)-a)
        # print("tmp 어쩌고:",len(tmp[tmp['latitude']!=0].index))
        # print('*'*30)
        Total.add_child(folium.CircleMarker(one_coordis[seq],color='red',radius=2,tooltip=tooltip,popup=folium.Popup(
        '확진자:{0},날짜:{1}일, 장소:{2},주소:{3}'.format(one_num,date1,place1[seq],address1[seq]),
        parse_html=True,max_width=450)))
        busan_div.add_child(Total)


      for index in tmp['latitude'].index:
        if tmp['latitude'][index]==0:
          pass
        elif tmp['latitude'][index]!=0:
          coordi=[tmp['longitude'][index],tmp['latitude'][index]]
          one_coordis.append(coordi)
      for one_coordi in one_coordis:
        folium.CircleMarker(location=one_coordi,radius=2,color='red', popups='확진자 방문 장소').add_to(marker_cluster)
        folium.CircleMarker(one_coordi,radius=2,color='red',fill=True,opacity=1)
        


folium.LayerControl().add_to(busan_div)



busan_div.save('busan.html')