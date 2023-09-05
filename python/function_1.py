#import snowboydetect
#from aip import AipSpeech
# import tuling
import sys
import pyaudio
import wave
import requests
import json
import os, re
import time
import base64
import numpy as np
import random
import pygame
from importlib import reload
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
    timer = time.perf_counter
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode
    timer = time.time

# musicPath = '/home/toybrick/aip-python-sdk/music'
musicPath = 'music'
reload(sys)

# print(sys.getdefaultencoding())


def playMusic(fileName):
    os.system('sudo aplay -D hw:0,0 ' + musicPath+'/'+ fileName + ' > /dev/null 2>&1 &')
    time.sleep(1)
def closeMusic():
    os.system("ps aux | grep aplay | grep -v grep | awk '{print $2}' | xargs sudo kill -9")
#播放音乐
def mplayerMusic(fileName):
    os.system('sudo aplay -D plughw:CARD=Device,DEV=0 ' + musicPath+'/'+ fileName + ' > /dev/null 2>&1 &')
    time.sleep(1)
def closeMplayer():
    os.system("ps aux | grep aplay | grep -v grep | awk '{print $2}' | xargs sudo kill -9")
    # pygame.mixer.music.pause()

    '''
    isRunStr = str(os.popen("ps -ef | grep mplayer | grep -v grep | awk '{print $1}' |sed -n '1p'").readline().strip())
    if isRunStr=='pi':
        print ('isRun')
        os.system("ps -ef | grep mplayer | grep -v grep | awk '{print $2}' | xargs kill -9")
        musicLoopStr = str(os.popen("ps -ef | grep musicLoop | grep -v grep | awk '{print $1}' |sed -n '1p'").readline().strip())
        if musicLoopStr=='pi':
            print ('isRun')
            os.system("ps -ef | grep musicLoop | grep -v grep | awk '{print $2}' | xargs kill -9")
    '''


def continueMplayer():
    pygame.mixer.music.unpause()


def getWeatherTemp():
    url = 'http://weatherapi.market.xiaomi.com/wtr-v2/weather?cityId=101210101'
    response = requests.get(url)
    wearher_json = json.loads(response.text)
    weather_dict = wearher_json['realtime']
    str = '%s%s%s%s%s%s%s%s%s%s%s%s%s%s' % (
    '当前天气', weather_dict['weather'], '，', '\n',
    '当前温度', weather_dict['temp'], '℃', '，', '\n'
    '当前风向', weather_dict['WD'], '，', '\n',
    '风速', weather_dict['WS'])
    return str


#今日天气预报
def getWeather():
    url = 'http://weatherapi.market.xiaomi.com/wtr-v2/weather?cityId=101210101'
    # url = 'http://www.weather.com.cn/data/sk/101210101.html'
    # url = 'http://www.weather.com.cn/data/cityinfo/101210101.html'
    response = requests.get(url)
    wearher_json = json.loads(response.text)
    print(wearher_json)
    weather_dict = wearher_json["forecast"]
    '''
    str = '%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s' % (
    '今天是', weather_dict['forecast'][0]['date'], '，', '\n',
    '天气', weather_dict["forecast"][0]['type'], '，', '\n',
    weather_dict['city'], '最', weather_dict['forecast'][0]['low'], '，', '\n',
    '最', weather_dict['forecast'][0]['high'], '，', '\n',
    '当前温度', weather_dict['wendu'], '℃', '，', '\n',
    weather_dict["forecast"][0]['fengxiang'],
    weather_dict["forecast"][0]['fengli'].split("[CDATA[")[1].split("]")[0])
    '''
    str = '%s%s%s%s%s%s%s%s%s' % (
    '杭州', '，', '\n',
    '今天天气', weather_dict["weather1"], '，', '\n',
    '温度', weather_dict["temp1"])
    return str
 
#明日天气预报
def getTWeather():
    # url = 'http://wthrcdn.etouch.cn/weather_mini?city=杭州'
    url = 'http://weatherapi.market.xiaomi.com/wtr-v2/weather?cityId=101210101'
    response = requests.get(url)
    wearher_json = json.loads(response.text)
    weather_dict = wearher_json['forecast']
    '''
    str = '%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s' % (
    '明天是', weather_dict['forecast'][1]['date'], '，', '\n',
    '天气', weather_dict["forecast"][1]['type'], '，', '\n',
    weather_dict['city'], '最', weather_dict['forecast'][1]['low'], '，', '\n',
    '最', weather_dict['forecast'][1]['high'], '，', '\n',
    weather_dict["forecast"][1]['fengxiang'],
    weather_dict["forecast"][1]['fengli'].split("[CDATA[")[1].split("]")[0],
    '。', '\n')
    '''
    str = '%s%s%s%s%s%s%s%s%s' % (
    '杭州', '，', '\n',
    '明天天气', weather_dict["weather2"], '，', '\n',
    '温度', weather_dict["temp2"])
    return str