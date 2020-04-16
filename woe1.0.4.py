import os
os.system('mode con: cols=100 lines=25')
import conda
import warnings
import geopy.geocoders
from geopy import distance
from geopy.geocoders import Nominatim
import json
from urllib.request import urlopen
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import wikipedia as wk
import conda

conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib

class cityinforamtion_n_howfar:
    def __init__(self, key_city):
        self.key_city = key_city
    
    def myLocation(self):  #내 위치 
        response = urlopen("http://ip-api.com/json").read()
        responseJson = json.loads(response)
        rJ = responseJson
        
        return rJ.get("city"), rJ.get("regionName"), rJ.get("country"), rJ.get("lat"), rJ.get("lon")
    
    def Key_city_info(self): #입력한 도시 정보
        geopy.geocoders.options.default_timeout = 20
        geolocator = Nominatim(user_agent="hoon")
        try: 
            location = geolocator.geocode(self.key_city, language = 'en')
            address_key_city = location.address #(도착지) 주소
            latitude_key_city = location.latitude #위도
            longitude_key_city = location.longitude #경도
        except AttributeError:
            print('\nNO DATA\n')
            ph_1()
        else: return address_key_city, latitude_key_city, longitude_key_city

    def wikiRef(self, key_lat, key_lon):
        wk.set_lang('en')
        try: 
            summ = wk.summary(self.key_city, sentences = 3)
            print('◈Wiki summary of '+self.key_city+'◈')
            print(summ+'..')
        except wk.exceptions.DisambiguationError:
            print('.')
            beatAmbig = wk.search(self.key_city)
            summ_1 = wk.summary(beatAmbig[1], sentences = 3)
            print('◈Wiki summary of '+self.key_city+'◈')
            print(summ_1+'..')
        except wk.exceptions.PageError:print('CANNOT FIND ANY DATA ON WIKI')
        finally:
            related = wk.geosearch(key_lat, key_lon, results = 5, radius = 10000)
            print('\n◈Geographically related results (up to 5 results)◈\n')
            num = 1
            for re in related:
                print(str(num)+'. '+re)
                num += 1

    def CALdistance(self, departure, destination): #거리 계산, (직선거리를 걸어서 가면 걸릴 시간도 계산)
        temp_distance = distance.great_circle(departure, destination).km
        time = temp_distance//4
        
        return temp_distance, time
    
class theMap:
    def __init__(self, key_city, key_lat, key_lon):
        self.key_city = key_city
        self.key_lat = key_lat
        self.key_lon = key_lon

    def visualization_1(self): #세계 지도
        plt.figure(num = 'WORLD MAP', figsize = (10, 7.5), frameon = False) #윈도우 창 속성

        m = Basemap(projection='mill', llcrnrlat = -90, urcrnrlat=90,\
            llcrnrlon=-180, urcrnrlon=180, lat_0 = 0, lon_0 = 180, resolution='c')

        m.fillcontinents(color='white', lake_color='lightblue')
        #위선, 경선 관련
        parallels = np.arange(-90., 91., 30.)
        meridians = np.arange(-180., 181., 60.)
        m.drawparallels(parallels, labels=[True, False, False, False], linewidth = '0.6')
        m.drawmeridians(meridians, labels=[False, False, False, True], linewidth = '0.6')
        #점 찍기
        x, y = m(self.key_lon, self.key_lat)
        m.plot(x, y, 'r.', markersize = 4)
        label = self.key_city
        plt.text(x+30000, y+30000, label)
        #지도 꾸미기
        m.drawmapboundary(fill_color='lightblue')
        m.drawcountries(linewidth = 0.75)
        m.drawcoastlines(linewidth= 0.2)

        plt.title('Location of '+self.key_city+' on the map')
        plt.show()
    
    def visualization_2(self, mapSize): #지역 지도, 어느 범위까지 확대할 지는 사용자가 선택 가능
        plt.figure(num = 'REGIONAL MAP', figsize = (10, 7.5), frameon = False) #윈도우 창 속성

        for key in mapSize:
            mapSize[key] = float(mapSize[key])
            mapSize[key] = round(mapSize[key])

        m = Basemap(projection='mill',\
             llcrnrlat = mapSize['minimum latitude'],\
             urcrnrlat = mapSize['maximum latitude'],\
             llcrnrlon = mapSize['minimum longitude'],\
             urcrnrlon = mapSize['maximum longitude'],\
             resolution='i', lat_0 = self.key_lat, lon_0 = self.key_lon )

        #위선, 경선 관련
        inter_para = abs(mapSize['minimum latitude'] - mapSize['maximum latitude'])/4
        inter_mrid = abs(mapSize['minimum longitude'] - mapSize['maximum longitude'])/4
        parallels = np.arange(mapSize['minimum latitude']+inter_para//2, mapSize['maximum latitude']+inter_para//2, inter_para)
        meridians = np.arange(mapSize['minimum longitude']+inter_mrid//2, mapSize['maximum longitude']+inter_mrid//2, inter_mrid)
        m.drawparallels(parallels, labels=[True, False, False, False], linewidth = '0.6')
        m.drawmeridians(meridians, labels=[False, False, False, True], linewidth = '0.6')
        #점 찍기
        x, y = m(self.key_lon, self.key_lat)
        m.plot(x, y, 'r.', markersize = 8)
        label = self.key_city
        plt.text(x+30000, y+30000, label)
        #지도 꾸미기
        m.drawmapboundary(fill_color='lightblue')
        m.drawcountries(linewidth = 0.5)
        m.drawcoastlines(linewidth= 0.2)
        m.fillcontinents(color='white', lake_color='lightblue')

        plt.title('Location of '+self.key_city+' on the map')
        plt.show()
    
    def custom_mapSize(self): # vis2를 위한 지도 크기 정하기 단계
        min_lat = self.key_lat-10
        max_lat = self.key_lat+10
        min_lon = self.key_lon-15
        max_lon = self.key_lon+15
        pre_mapSize = {'minimum latitude' : min_lat,'maximum latitude' : max_lat,\
                        'minimum longitude' :  min_lon,'maximum longitude' :  max_lon}
        notice = '''
        NOTICE
        IF YOU CHANGE THE DEFUALT SETTING, IT MIGHT LEAD TO THE UNNATURAL MAP SHAPE.\n
        '''
        print(notice)
        whether_change = input("Do you want to change the map setting?\n('y' to change, '(enter)' to set as default)\n▶")
        if whether_change == 'y':

            for infoes in pre_mapSize:
                pre_mapSize[infoes] = input('input '+infoes+': ')

        return pre_mapSize
            
def ph_1(): #도시 이름 받고 도시 기본 정보 출력
    global city_name, city_info
    Key_city = input("Input a city name\nNOTICE: USE A GENERAL NAME\n▶")
    user_ph1 = cityinforamtion_n_howfar(Key_city)
    city_info = user_ph1.Key_city_info()
    #정확성을 위해 도시 정식 도시 이름 추출
    try:
        splited_address = city_info[0].split(',')
    except TypeError:
        print('\nSORRY: AN ERROR OCCURRED\nTRY AGAIN\n')
        ph_1()
        return
    city_name = splited_address[0]
    user_ph1 = cityinforamtion_n_howfar(city_name)
    #도시 정보 출력 후 위키 참조
    print(city_info, '\n')
    user_ph1.wikiRef(city_info[1], city_info[2])

    #재귀 호출 할 것인지 정하기
    ph_choice = input("\nDo you want to search for another city?('y' to change, '(enter)' to stay on)\n▶")
    if ph_choice == 'y': 
        print('★\n')
        ph_1()
        return

def ph_2(): #거리구하기 or 지도에 점 표시
    global city_name, city_info
    choice = input('''\n
    1: Calculating distance
    2: Show '''+city_name+''' on the world map
    3: Show '''+city_name+''' on the magnified map\n▶''')
    if int(choice) == 1: # 거리 구하기
        user_ph2 = cityinforamtion_n_howfar(city_name)
        # 출발지 설정
        departure = input("\nSet a departure ('m' to detect my location, 'k' to use "+city_name+")\n▶")
        if departure == 'm':
            departure = user_ph2.myLocation()
            print(departure)
        elif departure == 'k': departure = city_info
        else:
            custom_departure = cityinforamtion_n_howfar(departure)
            departure = custom_departure.Key_city_info()
            print(departure)
        # 도착지 설정
        destination = input("\nSet a destination ('m' to detect my location, 'k' to use "+city_name+")\n▶")
        if destination == 'm':
            destination = user_ph2.myLocation()
            print(destination)
        elif destination == 'k': destination = city_info
        else:
            custom_destination = cityinforamtion_n_howfar(destination)
            destination = custom_destination.Key_city_info()
            print(destination)
        # p_ 변수에 위도, 경도 정보만 저장
        p_departure = []
        p_departure.append(departure[-2])
        p_departure.append(departure[-1])
        
        p_destination = []
        p_destination.append(destination[-2])
        p_destination.append(destination[-1])
        
        distance = user_ph2.CALdistance(p_departure, p_destination) 
        print('\nFrom '+departure[0])
        print('To '+destination[0])
        print('\n'+str(distance[0])+'km\nApproximately '+str(distance[1])+' hours by walk\n')
        
    elif int(choice) == 2: #세계지도에서 보기
        user_ph2 = theMap(city_name, city_info[1], city_info[2])
        user_ph2.visualization_1()
    elif int(choice) == 3: #확대된 지도에서 보기
        user_ph2 = theMap(city_name, city_info[1], city_info[2])
        mapSize = user_ph2.custom_mapSize()
        user_ph2.visualization_2(mapSize)
    else: #이상한 숫자
        print('\nWRONG OPTION')
        ph_2()
    #재귀 호출 할 것인지 정하기
    ph_choice = input("\nDo you want to use the other tools?('y' to use, '(enter)' to search for another city)\n▶")
    if ph_choice == 'y': ph_2()
    else: return

#본격적인 실행
app_info = '''
-------------------------------------
WHAT ON EARTH! v. 1.0.4
This program is made by Yeonghun Lim.
March, 2020
-------------------------------------
'''
print(app_info)
while True:
    ph_1()
    ph_2()