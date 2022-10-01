'''
Author: Huaisheng Ye
Create time: 2022年8月24日12:21:18
Edit Time: 2022年10月1日23:08:39
Description: IIIoTD Visualization Tool.
GitHub Url: https://github.com/MJU-AIoT/IIIoTD
'''

import argparse

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import os

datasets_path = './datasets/'
visual_output_path = './visual/'
device_name = ['air-conditioner', 'illumination', 'curtain']

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

def draw_action_pie(room_name, days = 7*4):
    # read feature data
    room_data_path = '{}{}/'.format(datasets_path, room_name)
    feature_name_path = '{}feature_name.txt'.format(room_data_path)
    device_index = []
    device_opt_num = {

    }
    device_class_opt_num = {

    }
    file = open(feature_name_path, 'r')
    data = file.readlines()
    file.close()
    feature_name = data[0].split(',')
    for id, name in enumerate(feature_name):
        if name[:name.rfind('_')] in device_name:
            device_index.append(id)
            device_opt_num[name] = 0
    
    for d_n in device_name:
        device_class_opt_num[d_n] = 0
    
    # analyse data
    total_opt_num = 0
    for day in range(days):
        file_path = '{}day{}.txt'.format(room_data_path,day+1)
        file = open(file_path, 'r')
        data = file.readlines()
        pre_feature = data[0].split(' ')
        for feature in data:
            now_feature = feature.split(' ')
            for index in device_index:
                if now_feature[index] != pre_feature[index]:
                    total_opt_num += 1
                    d_n = feature_name[index]
                    device_opt_num[ d_n ] += 1
                    device_class_opt_num[ d_n[:d_n.rfind('_')] ] += 1
            pre_feature = now_feature
        file.close()
    print('[info]: {} total option num is {}, average option num is {:.2f}.'.format(room_name, total_opt_num, total_opt_num / days))
    print('[info]: The number of operations for each device entity is as follows.')
    for name in device_opt_num:
        print('\t{}={} ({:.2f}%)'.format(name, device_opt_num[name], (device_opt_num[name]/total_opt_num)*100))
    print('[info]: The number of operations for each device category is as follows.')
    device_num = []
    for name in device_class_opt_num:
        print('\t{}={} ({:.1f}%)'.format(name, device_class_opt_num[name], (device_class_opt_num[name]/total_opt_num)*100))
        device_num.append(device_class_opt_num[name])
    # draw the analysis result
    plt.figure()
    plt.pie(device_num, labels=device_name, autopct='%1.1f%%', counterclock=False, startangle=90, colors=['#1E90FF', '#FFA500', '#3CB371'])
    plt.title(room_name)
    plt.tight_layout()
    plt.savefig('{}action_pie_{}.png'.format(visual_output_path, room_name), dpi=640)
    plt.savefig('{}action_pie_{}.svg'.format(visual_output_path, room_name), dpi=640)

    # show the analysis result
    plt.show()

def draw_heat_map(room_name):
    # read data
    vegetables = ["23:00", "22:00", "21:00", "20:00", "19:00", "18:00", "17:00", "16:00", "15:00", "14:00", "13:00", "12:00", "11:00", "10:00", "09:00", "08:00"]
    farmers = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    room_data_path = '{}{}/'.format(datasets_path,room_name)
    feature_name_path = '{}feature_name.txt'.format(room_data_path)
    device_index = []
    file = open(feature_name_path, 'r')
    data = file.readlines()
    feature_name = data[0].split(',')
    for id, name in enumerate(feature_name):
        if name[:name.rfind('_')] in device_name:
            device_index.append(id)
    file.close()

    # analyse data
    heat_maps = {

    }
    for d_n in device_name:
        heat_maps[d_n] = np.zeros((16, 7))
    days = 7*4
    for day in range(days):
        file = open('{}day{}.txt'.format(room_data_path, day+1), 'r')
        data = file.readlines()
        pre_feature = data[0].split(' ')
        for minute, feature in enumerate(data):
            if feature == '':
                continue
            now_feature = feature.split(' ')
            for id, index in enumerate(device_index):
                if now_feature[index] != pre_feature[index]:
                    d_n = feature_name[index][:feature_name[index].rfind('_')]
                    hours = minute // 60 - 8
                    if hours < 0:
                        continue
                    week = day % 7
                    heat_maps[d_n][15 - hours][week] += 1
            pre_feature = now_feature

    # draw the analysis result
    fig = plt.figure()
    table_name = ['Air-conditioner', 'Illumination', 'Curtain']
    for id, name in enumerate(heat_maps):
        ax1 = fig.add_subplot(130 + id + 1)
        plt.xticks(np.arange(len(farmers)), labels=farmers, rotation=45, rotation_mode="anchor", ha="right", fontdict={'family' : 'Times New Roman', 'weight':'bold'})
        plt.yticks(np.arange(len(vegetables)), labels=vegetables, fontdict={'family' : 'Times New Roman', 'weight':'bold'})
        plt.title(table_name[id], fontdict={'family' : 'Times New Roman', 'weight':'bold'})
        for i in range(len(vegetables)):
            for j in range(len(farmers)):
                if int(heat_maps[name][i, j])!= 0:
                    text = plt.text(j, i, int(heat_maps[name][i, j]), ha="center", va="center", color="w", fontdict={'family' : 'Times New Roman', 'weight':'bold'})
        plt.imshow(heat_maps[name], cmap=cm.Blues)
        plt.sca(ax1)
    
    # show the analysis result
    plt.tight_layout()
    plt.savefig('{}heat_map_{}.png'.format(visual_output_path, room_name), dpi=640)
    plt.savefig('{}heat_map_{}.svg'.format(visual_output_path, room_name), dpi=640)

    plt.show()

def draw_env_change(room_name, days, legend = False):
    # read data
    room_data_path = '{}{}/'.format(datasets_path, room_name)
    feature_name_path = '{}feature_name.txt'.format(room_data_path)
    day_data_path = '{}day{}.txt'.format(room_data_path, days)
    file = open(day_data_path, 'r')
    data = file.readlines()
    file.close()
    file = open(feature_name_path, 'r')
    feature_name = file.readlines()[0].split(',')
    file.close()
    # analyse data
    filter_char = ['c', 'h', 'f', 'b']
    info_scale = [50, 45, 1, 1, 1, 1]
    for d_n in feature_name[6:]:
        if device_name[1] in d_n:
            info_scale.append(100)
        else:
            info_scale.append(1)
    draw_data = {

    }
    for name in feature_name:
        draw_data[name] = {
            'x': [],
            'y': []
        }
    device_start = 6
    pre_feature = data[0].split(' ')
    for minute, feature in enumerate(data):
        now_feature = feature.split(' ')
        for index, info in enumerate(now_feature):
            if index < device_start:
                msg_val = float(info) * info_scale[index]
                if index == 5:
                    msg_val /= 250
                    msg_val *= 100
                draw_data[feature_name[index]]['y'].append(msg_val)
                draw_data[feature_name[index]]['x'].append(minute)
            else:
                if now_feature[index] != pre_feature[index]:
                    real_info = info
                    for filter_c in filter_char:
                        real_info = real_info.replace(filter_c, '')
                    msg_val = float(real_info) * info_scale[index]

                    draw_data[feature_name[index]]['y'].append(msg_val)
                    draw_data[feature_name[index]]['x'].append(minute)
        pre_feature = now_feature
    
    # draw the analysis result
    fig, ax  = plt.subplots()
    ax.set_ylim(-10, 110)
    for index, name in enumerate(feature_name):
        if index < device_start:
            ax.plot(draw_data[name]['x'], draw_data[name]['y'], label=name, alpha=0.5)
        else:
            ax.scatter(draw_data[name]['x'], draw_data[name]['y'], label=name)
    if legend:
        labelss = plt.legend(loc='best').get_texts()
        [label.set_fontname('Times New Roman') for label in labelss]
    x1_label = ax.get_xticklabels() 
    [x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
    y1_label = ax.get_yticklabels() 
    [y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]

    # show the analysis result
    plt.savefig('{}env_change_{}_day{}.png'.format(visual_output_path, room_name, days), dpi=640)
    plt.savefig('{}env_change_{}_day{}.svg'.format(visual_output_path, room_name, days), dpi=640)
    plt.show()

if __name__ =='__main__':
    print('Hello Anne!')
    mkdir(visual_output_path)
    parser = argparse.ArgumentParser(description='IIIoTD Visualization Tool.')
    parser.add_argument('--room', default='R4', choices=['R0', 'R1', 'R2', 'R3', 'R4'], help='The name of the target room.')
    params = parser.parse_args()
    draw_action_pie(params.room)
    draw_heat_map(params.room)
    for day in range(28):
        draw_env_change(params.room, day+1, legend=False)
