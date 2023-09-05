# coding=utf-8
import sys
import json
import os
import random
import pygame
#from aip import AipSpeech
from stt import stt
from record_audio import shellRecord, shellRecord_old
# from function import *
from function_1 import *
from main_tic_tac_toe import tic_tac_toe_main
from server import socket_service
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
    # timer = time.perf_counter
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode
    # timer = time.time

API_KEY = 'sfsamNLCKhd5nnQoCdHQShYH'
SECRET_KEY = 'CEorysiIaXbQyAKVEovlyhl6FpeQGbkQ'

'''
audioPath = '/home/toybrick/aip-python-sdk/project/result.wav'
demoPath = '/home/toybrick/aip-python-sdk/project/demo.txt'
voicePath = '/home/toybrick/aip-python-sdk/project/voice.wav'
musicPath = '/home/toybrick/aip-python-sdk/project/music'
'''
audioPath = 'result.wav'
demoPath = 'demo.txt'
voicePath = 'voice.wav'
musicPath = 'music'

# TEXT = "欢迎使用百度语音合成。"

# 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
# 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美 
PER = 0
# 语速，取值0-15，默认为5中语速
SPD = 5
# 音调，取值0-15，默认为5中语调
PIT = 5
# 音量，取值0-9，默认为5中音量
VOL = 5
# 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
AUE = 6

FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
FORMAT = FORMATS[AUE]

CUID = "123456PYTHON"

TTS_URL = 'http://tsn.baidu.com/text2audio'


class DemoError(Exception):
    pass


"""  TOKEN start """

TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'
SCOPE = 'audio_tts_post'  # 有此scope表示有tts能力，没有请在网页里勾选


def changeVoiceMax(number):
    os.system("sudo amixer set Speaker " + str(number)  + "%")


def get_text(demo):
    f = open(demo, 'r', encoding='utf-8')
    command = f.read()
    if len(command) != 0:
        word = command
        f.close()
        return word
    else:
        return None


def fetch_token():
    print("fetch token begin")
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    if (IS_PY3):
        result_str = result_str.decode()

    print(result_str)
    result = json.loads(result_str)
    print(result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not SCOPE in result['scope'].split(' '):
            raise DemoError('scope is not correct')
        print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

def tts(TEXT):
    token = fetch_token()
    tex = quote_plus(TEXT)  # 此处TEXT需要两次urlencode
    print(tex)
    params = {'tok': token, 'tex': tex, 'per': PER, 'spd': SPD, 'pit': PIT, 'vol': VOL, 'aue': AUE, 'cuid': CUID,
              'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数

    data = urlencode(params)
    print('test on Web Browser' + TTS_URL + '?' + data)

    req = Request(TTS_URL, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()

        headers = dict((name.lower(), value) for name, value in f.headers.items())

        has_error = ('content-type' not in headers.keys() or headers['content-type'].find('audio/') < 0)
    except URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()
        has_error = True

    save_file = "error.txt" if has_error else 'result.' + FORMAT
    with open(save_file, 'wb') as of:
        of.write(result_str)

    if has_error:
        if (IS_PY3):
            result_str = str(result_str, 'utf-8')
        print("tts api  error:" + result_str)

    print("result saved as :" + save_file)
    os.system('sudo aplay -D plughw:CARD=Device,DEV=0 ' + audioPath)
    # os.system(audioPath)


def wakeup():
    while (1):
        print('Listening... please say wake-up word:蜡笔小新')
        socket_service()
        TEXT = get_text(demoPath)
        if TEXT is not None:
            if '蜡笔小新' in TEXT:
                tts('在的')
                loopRecord()

def loopRecord():
    count_1 = 0
    count_l = 1
    count_u = 1
    while (1):
        flag = False
        # shellRecord(voicePath)
        # shellRecord_old(voicePath)
        # time.sleep(5)
        socket_service()
        # stt(voicePath)
        TEXT = get_text(demoPath)
        time.sleep(1)
        print(TEXT)
        pygame.mixer.init()
        fileNameList = os.listdir(musicPath)
        print(fileNameList)
        if count_1 > 10:
            break
        if TEXT is not None:
            count_1 = 0
            if '明' in TEXT and '天' in TEXT and '气' in TEXT:
                tts(getTWeather())
                time.sleep(3)
            elif '音量' in TEXT or '声' in TEXT:
                if '低' in TEXT or '小' in TEXT:
                    voice = 50-count_l * 10
                    if voice >= 0:
                        changeVoiceMax(voice)
                        count_l = count_l + 1
                        count_u = 1
                elif '恢复' in TEXT or '正常' in TEXT:
                    changeVoiceMax(70)
                    count_l = 1
                    count_u = 1
                elif '最大' in TEXT:
                    changeVoiceMax(100)
                    count_l = 1
                    count_u = 1
                elif '大' in TEXT or '高' in TEXT:
                    voice = 50 + count_u * 10
                    if voice <= 100:
                        changeVoiceMax(voice)
                        count_u = count_u + 1
                        count_l = 1
                tts('音量已调到最悦耳的大小啦')
                time.sleep(4)
            elif '今' in TEXT and '天' in TEXT and '气' in TEXT:
                # changeVoiceMax(100)
                tts(getWeather())
                count_1 = 0
                time.sleep(3)
            elif ('当前' in TEXT or '现在' in TEXT) and '天' in TEXT and '气' in TEXT:
                # changeVoiceMax(100)
                tts(getWeatherTemp())
                count_1 = 0
                time.sleep(3)
            elif '随便' in TEXT or '随机' in TEXT or '放首歌' in TEXT or '播放音乐' in TEXT:
                fileNameList = os.listdir(musicPath)
                fileName = fileNameList.pop(random.randint(0, len(fileNameList) - 1))
                fileName_1 = ' '.join(fileNameList)
                fileName = fileName + ' ' + fileName_1
                mplayerMusic(fileName)
                # os.system('sudo aplay -D plughw:CARD=Device,DEV=0 ' + musicPath+'/'+fileName)
            elif '换一首' in TEXT or '下一首' in TEXT or '下一曲' in TEXT:
                closeMplayer()
                time.sleep(2)
                fileName = fileNameList.pop(random.randint(0, len(fileNameList) - 1))
                fileName_1 = ' '.join(fileNameList)
                fileName = fileName + ' ' + fileName_1
                mplayerMusic(fileName)
                count_1 = 0
            elif '停止' in TEXT or '暂停' in TEXT or '不要' in TEXT or '休息' in TEXT or '关闭音乐' in TEXT or '安静' in TEXT:
                closeMplayer()
                count_1 = 0
            elif '防守' in TEXT or '放手' in TEXT or '放首' in TEXT or '播放' in TEXT or '放一首' in TEXT or '唱一首' in TEXT or '听一下' in TEXT or '听一首' in TEXT:
                newStr = TEXT.replace('播放', '').replace('放一首', '').replace('唱一首', '').replace('听一下', '').replace('听一首', '').replace('放首', '').replace('放手', '').replace('防守', '').replace('。', '')
                closeMplayer()
                flag_1 = False
                for i in range(0, len(fileNameList)):
                    if newStr == fileNameList[i][:-4]:
                        mplayerMusic(fileNameList[i])
                        time.sleep(1)
                        flag_1 = True
                        break
                if flag_1 is False:
                    tts("没有找到你想要播放的歌曲")
                    time.sleep(3)
                count_1 = 0
            elif '继续' in TEXT:
                continueMplayer()
                count_1 = 0
            elif '关机' in TEXT or '退出' in TEXT:
                break
        else:
            count_1 = count_1 + 1
"""  TOKEN end """

if __name__ == '__main__':
    wakeup()