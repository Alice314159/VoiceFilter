from matplotlib import pyplot
import ThinkDSP.ThinkDSP.code.thinkdsp as DSP
import os
import pandas as pd
import numpy as np
import wave
import time


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


while True:
    excel_file_name = input("please input the xls file: ")
    if os.path.exists(excel_file_name):
        break
    else:
        print("can't find the file,please check and input the right wave file like 'E:\\aaa.wav': ")

dataTemp = pd.read_excel(excel_file_name, usecols=[0])
data_list = dataTemp.values.tolist()

# 将数据装换为list格式
y_list = []
for i in range(len(data_list)):
    y_list.append(data_list[i][0])

# 修改为音频文件后缀
wave_file = excel_file_name.rsplit('.xls')
wave_file_name = wave_file[0] + '.wav'

# 将数据存储为音频格式，方便滤波
wavdata = np.array(y_list)
f = wave.open(wave_file_name, "wb")  # 新建并打开wav文件
# 配置声道数、量化位数和采样频率
f.setnchannels(1)  # 配置声道数
f.setsampwidth(4)  # 配置量化位数
f.setframerate(500)  # 配置采样频率
f.writeframes(wavdata.tobytes())  # 将wav_data转换为二进制数据写入文件
f.close()

# 绘制原始的时域图像
pyplot.clf()
file_abs = os.path.abspath(wave_file_name)
file_path = os.path.dirname(file_abs)

wave = DSP.read_wave(wave_file_name)
wave.plot()
pyplot.savefig(file_path + "\\" + 'Original Time Domain Diagram')

# 绘制原始的频域图像
pyplot.clf()
spectrum = wave.make_spectrum()
spectrum.plot()
pyplot.savefig(file_path + "\\" + 'Original Frequency Domain Diagram')

# 绘制经过低通滤波器的频域图像
pyplot.clf()
while True:
    cutoff_str1 = input("Please input stop pass filter lower limit：")
    if cutoff_str1.isdigit():
        break
    else:
        print("lower limit parameter is wrong,the input parameter should be an integer！ ")

while True:
    cutoff_str2 = input("Please input stop pass filter higher limit：")
    if cutoff_str2.isdigit():
        break
    else:
        print("higher limit parameter is wrong,the input parameter should be an integer！ ")

while True:
    coefficient_str = input("Please input Attenuation coefficient：")
    if is_number(coefficient_str):
        break
    else:
        print("Attenuation coefficient is wrong,the input parameter should be an digit！ ")

low_cutoff = int(cutoff_str1)
high_cutoff = int(cutoff_str2)
coefficient = float(coefficient_str)

pyplot.clf()
spectrum.band_stop(low_cutoff, high_cutoff, coefficient)
spectrum.plot()
pyplot.title('Frequency Domain Diagram After Process')
pyplot.savefig(file_path + "\\" + 'Frequency Domain Diagram After Process')

# 绘制经过滤波器的时域图像
pyplot.clf()
wave1 = spectrum.make_wave()

file_name = wave_file_name.rsplit('.')
new_file_name = file_name[0] + '-after.' + file_name[1]
wave1.write(new_file_name)
wave1.plot()
pyplot.title('Time Domain Diagram After Process')
pyplot.savefig(file_path + "\\" + 'Time Domain Diagram After Process')

data = pd.DataFrame(wave1.ys)
after_excel = file_name[0] + '_after-filter.xls'
data.to_excel(after_excel)

print('data file:' + excel_file_name)
print('band pass param:{}-{}-{}'.format(low_cutoff, high_cutoff, coefficient))
print('save file to ' + after_excel)

time.sleep(10000)
