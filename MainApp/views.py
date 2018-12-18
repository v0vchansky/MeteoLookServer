from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import Http404, HttpResponse
from io import BytesIO
from PIL import Image
# import cStringIO #Inslall
import requests
import base64
import os
import json
import time


def index(request):
    lat = request.GET.get('lat', '')
    lon = request.GET.get('lon', '')
    sex = request.GET.get('sex', '')

    print(lat, lon)

    if sex == 'man':
        man = True
    else:
        man = False
    # print(lat)
    # Yandex Api
    # App_Id = "081fb88c-3764-41c5-a275-351b965120ab"
    # res = requests.get("https://api.weather.yandex.ru/v1/forecast",
    #                     params={'lat': 37, 'lon' : 55},
    #                     headers={'X-Yandex-API-Key': App_Id})



    # OWM Api
    # App_Id = "cd4ae38185273442f9a802c3b3a02665"
    # res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
    #                     params={'lat': lat, 'lon' : lon, 'units': 'metric', 'lang': 'ru', 'APPID': App_Id})
    # data = res.json()



    # with open('MainApp/localhost.json', 'r', encoding='utf-8') as fh: #открываем файл на чтение
    #     data = json.load(fh) #загружаем из файла данные в словарь data
    # print(data)



    # AccuWeather Api
    # apikey = "tsJfXOjfswhOrNCin439H64TYdc6IF6O"
    # # Получаем LocationKey для получения погоды
    # locationKeyRequest = requests.get("https://dataservice.accuweather.com/locations/v1/cities/geoposition/search",
    #                     params={'q': lat + ',' + lon, 'language': 'ru', 'apikey': apikey})
    # locationKey = locationKeyRequest.json()['Key']
    # print(locationKey)
    # # Получаем погоду на 5 дней
    # res = requests.get("https://dataservice.accuweather.com/forecasts/v1/daily/5day/" + locationKey, 
    #                     params={'details': True, 'language': 'ru', 'apikey': apikey}) 
    # data = res.json()['DailyForecasts']



    # DarkSky Api
    apikey = "b4a4e5b24b00252fe4d24d63870a7664"
    # Получаем LocationKey для получения погоды
    res = requests.get("https://api.darksky.net/forecast/" + apikey + "/" + lat + "," + lon,
                        params={'exclude': 'currently,minutely,hourly', 'lang': 'ru', 'units': 'si'})
    data = res.json()['daily']['data']

    dataList = []
    for index, a in enumerate(data):
        months = [' Января',' Февраля',' Марта',' Апреля',' Мая',' Июня',' Июля',' Августа',' Сентября',' Октября',' Ноября',' Декабря']
        if index == 0:
            continue

        ts = time.gmtime(a['time'])
        day = time.strftime("%d", ts)
        if day[0] == '0':
            day = day[:0] + day[(0+1):]
        month = months[int(time.strftime("%m", ts)) - 1]

        if index == 1:
            date = 'Сегодня'
        elif index == 2:
            date = 'Завтра'
        else:
            date = day + ' ' + month
        print(date + '\n')


        # DarkSky Api
        temp = round((int(a['temperatureMin']) + int(a['temperatureMax'])) / 2)
        humidity = int(a['humidity']) * 100
        wind = round(int(a['windGust']))
        icon = "DSIcons/" + str(a['icon']) + ".png"

        try:
            weatherType = a['precipType']
        except:
            weatherType = None

        dayWeather = {
            'date': date,
            'temp': temp,
            'humidity': humidity,
            'icon': icon,
            'image': Scotcher(man, temp, humidity, wind, weatherType)
        }

        # AccuWeather Api
        # temp = round((int(a['RealFeelTemperature']['Minimum']['Value']) + int(a['RealFeelTemperature']['Maximum']['Value'])) / 2)
        # humidity = 1
        # icon = "AWIcons/" + str(a['Day']['Icon']) + "-s.png"

        # dayWeather = {
        #     'date': date,
        #     'temp': temp,
        #     'humidity': humidity,
        #     'icon': icon,
        #     'image': Scotcher(man, temp, 1, 1)
        # }

        dataList.append(dayWeather)

    response = JsonResponse(dataList, safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    
    return response

def Scotcher(man, temp, humidity, wind, weatherType):
    # if man == true => man = man else man = woman

    path = os.getcwd() + "/MainApp/static/source/"

    hat = None         # Шапка
    shirt = None       # Кофта/футболка/рубашка/майка  
    scarf = None       # Шарф  
    vest = None        # Верхняя одежда
    socks = None       # Носки
    pants = None       # Штаны   
    gloves = None      # Перчатки
    boots = None       # Обувь
    umbrella = None    # Зонт

    if man:
        body = Image.open(path + 'm.png')

        if temp > 30:
            shirt = Image.open(path +   'm301.png')
            socks = Image.open(path +   'm601.png')
            pants = Image.open(path +   'm501.png')
            boots = Image.open(path +   'm701.png')
        
        elif temp > 20:
            shirt = Image.open(path +   'm302.png')
            socks = Image.open(path +   'm601.png')
            pants = Image.open(path +   'm501.png')
            boots = Image.open(path +   'm701.png')
        
        elif temp > 10:
            shirt = Image.open(path +   'm302.png')
            vest = Image.open(path +    'm305.png')
            socks = Image.open(path +   'm601.png')
            pants = Image.open(path +   'm502.png')
            boots = Image.open(path +   'm701.png')

        elif temp > 0:
            shirt = Image.open(path +   'm303.png')
            vest = Image.open(path +    'm305.png')
            socks = Image.open(path +   'm601.png')
            pants = Image.open(path +   'm502.png')
            boots = Image.open(path +   'm702.png')

        elif temp >= -9:
            hat = Image.open(path +     'm101.png')
            shirt = Image.open(path +   'm303.png')
            scarf = Image.open(path +   'm201.png')
            vest = Image.open(path +    'm306.png')
            socks = Image.open(path +   'm601.png')
            pants = Image.open(path +   'm502.png')
            gloves = Image.open(path +  'm401.png')
            boots = Image.open(path +   'm702.png')

        elif temp < -9:
            hat = Image.open(path +     'm102.png')
            shirt = Image.open(path +   'm304.png')
            scarf = Image.open(path +   'm201.png')
            vest = Image.open(path +    'm307.png')
            socks = Image.open(path +   'm601.png')
            pants = Image.open(path +   'm503.png')
            gloves = Image.open(path +  'm401.png')
            boots = Image.open(path +   'm703.png')

    else:
        body = Image.open(path + 'w.png')

        if temp > 25:
            shirt = Image.open(path +   'w301.png')
            socks = Image.open(path +   'w601.png')
            pants = Image.open(path +   'w501.png')
            boots = Image.open(path +   'w701.png')
        
        elif temp > 20:
            shirt = Image.open(path +   'w302.png')
            socks = Image.open(path +   'w601.png')
            boots = Image.open(path +   'w701.png')
        
        elif temp > 10:
            shirt = Image.open(path +   'w301.png')
            vest = Image.open(path +    'w305.png')
            socks = Image.open(path +   'w601.png')
            pants = Image.open(path +   'w502.png')
            boots = Image.open(path +   'w701.png')

        elif temp > 0:
            hat = Image.open(path +     'w102.png')
            shirt = Image.open(path +   'w304.png')
            vest = Image.open(path +    'w305.png')
            socks = Image.open(path +   'w601.png')
            pants = Image.open(path +   'w502.png')
            boots = Image.open(path +   'w702.png')

        elif temp >= -9:
            hat = Image.open(path +     'w101.png')
            shirt = Image.open(path +   'w304.png')
            scarf = Image.open(path +   'w201.png')
            vest = Image.open(path +    'w306.png')
            socks = Image.open(path +   'w601.png')
            pants = Image.open(path +   'w502.png')
            gloves = Image.open(path +  'w401.png')
            boots = Image.open(path +   'w702.png')

        elif temp < -9:
            hat = Image.open(path +     'w103.png')
            shirt = Image.open(path +   'w304.png')
            scarf = Image.open(path +   'w201.png')
            vest = Image.open(path +    'w306.png')
            socks = Image.open(path +   'w601.png')
            pants = Image.open(path +   'w503.png')
            gloves = Image.open(path +  'w401.png')
            boots = Image.open(path +   'w703.png')
    
    if weatherType == 'rain':
        umbrella = Image.open(path +   'зонт.png')
        if temp < 15:
            boots = Image.open(path +   '704.png')

    if not hat == None:
        body.paste(hat, (0, 0), hat)
    if not socks == None:
        body.paste(socks, (0, 0), socks)
    if not gloves == None:
        body.paste(gloves, (0, 0), gloves)
    if not shirt == None:
        body.paste(shirt, (0, 0), shirt)
    if not pants == None:
        body.paste(pants, (0, 0), pants)
    if not scarf == None:
        body.paste(scarf, (0, 0), scarf)
    if not vest == None:
        body.paste(vest, (0, 0), vest)
    if not boots == None:
        body.paste(boots, (0, 0), boots)
    if not umbrella == None:
        body.paste(umbrella, (0, 0), umbrella)
    

    buffered = BytesIO()
    body.save(buffered, format="PNG")
    imgStr = base64.b64encode(buffered.getvalue())
    imgBase64 = imgStr.decode('ascii')
    fullBase64Image = "data:image/png;base64," + imgBase64
    return fullBase64Image




# def getWeatherIconBase64(iconName):
#     #buffered = BytesIO(requests.get('http://openweathermap.org/img/w/' + iconName).content)
#     imgBase64 = base64.b64encode(requests.get('http://openweathermap.org/img/w/' + iconName + '.png').content)
#     imgBase64 = imgBase64.decode('ascii')

#     fullBase64Image = "data:image/png;base64," + imgBase64
#     return fullBase64Image
