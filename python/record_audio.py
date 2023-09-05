import os
import pyaudio
import wave
import numpy as np
import time
from client import sock_client
from stt import stt
# voicePath = '/home/toybrick/aip-python-sdk/project/voice.wav'
voicePath = 'voice.wav'
demoPath = 'demo.txt'
def shellRecord_old(voicePath):
    flag = False
    if flag is True:
        time.sleep(10)
    print('录音开始')
    os.system('sudo arecord -D plughw:3,0 -d 5 -r 16000  -t wav -f S16_LE ' + voicePath)
    print('录音结束')
    flag = True
# CARD=Device,DEV=0
 
# 根据你录音的长短决定，这里更新了录音时间，可长可短，最短2秒，最长7秒，用110/16约等于7秒
# 假如你不说话，2秒钟+1秒判断后识别，假如你说话，最多可以连续7秒钟再识别，很人性化

def shellRecord(voicePath):
    #最小说话音量
    MIN_VOICE = 4000
    #最大说话音量，防止干扰出现30000+的音量
    MAX_VOICE = 15000
    #录音判断开始时间，前面的时间可能是回复的语音音量过大导致误判断
    START_SEC = 5
    #录音判断间隔，约等于8/16=0.5秒
    INTERVAL = 5
    #最大录音时间,16*10=160,十秒钟
    MAX_RECORD_TIME = 160
    temp = 20					#temp为检测声音值
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    #录音文件输出路径
    WAVE_OUTPUT_FILENAME = voicePath
    p = pyaudio.PyAudio()
 
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    #snowboydecoder.play_audio_file()
    print("录音开始")
 
    frames = []
    flag = False			#一重判断,判断是否已经开始说话，这个判断从第5个数字开始，防止前面数字大于30000的情况
    stat2 = False			#二重判断,第一次判断声音变小
    stat3 = False			#三重判断,第二次判断声音变小
    tempnum = 0				#tempnum、tempnum2、tempnum3为时间
    tempnum2 = 0
    tempnum3 = 0
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
        audio_data = np.frombuffer(data, dtype=np.short)
        #获取录音的音量
        temp = np.max(audio_data)
        #如果时间大于其实判断时间并且音量在正常范围之内
        if tempnum > START_SEC and flag is False and temp > MIN_VOICE and temp < MAX_VOICE:
            #判断出开始说话
            flag = True
        #如果已经开始说话，那么开始判断
        if (flag):
            #如果声音小于正常范围
            if temp < MIN_VOICE:
                #如果是stat2还是False状态，证明还未开始判断
                if stat2 is False:
                    #时间点2和时间点3
                    tempnum2 = tempnum + INTERVAL
                    tempnum3 = tempnum + INTERVAL
                    #状态2开始变为True，说明第一次判断开始
                    stat2 = True
                #开始第二次判断，stat2为True表示已经第一次判断，超过第一次时间段开始第二次判断
                elif stat2 and stat3 is False and tempnum > tempnum2:
                    #已经超过了第一个时间段，那么stat3为True,这是第二次判断                   
                    stat3 = True
                #stat2和stat3都为True并且超过第二个时间段，这是最后一次判断
                if stat2 and stat3 and tempnum > tempnum3:
                    print("录音完毕")
                    #跳出循环
                    break
            else:
                #只要声音变大了，那么就重置状态
                stat2 = False
                stat3 = False
        #时间约1/16秒每次递增
        tempnum = tempnum + 1
        if tempnum > MAX_RECORD_TIME:				#超时直接退出
            print("录音结束")
             #跳出循环
            break
 
    stream.stop_stream()
    stream.close()
    p.terminate()
 
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    stt(voicePath)
    f = open('demo.txt', 'r', encoding='utf-8')
    command = f.read()
    if len(command) != 0:
        word = command
        f.close()

    time.sleep(2)
    sock_client()
    if '天' in word and '气' in word:
        time.sleep(10)


if __name__ == '__main__':
    count_1 = 0
    while 1:
        if count_1 > 5:
            break
        else:
            shellRecord(voicePath)

