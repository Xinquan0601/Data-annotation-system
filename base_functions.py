"""
    This base_functions is designed to operate npy files
    Do not modify it unless it is necessary
    Designer:ChenXinQuan
    Email:1039953448@qq.com
    Date:2023/5/26
"""
import os
from datetime import datetime

import numpy as np

msg_table = []
data_file_name = ''


def read_data_from_npy(file_path):
    """
    Reading data from the npy file, if an IO exception occurs,
    the initialization will not be completed and the program will exit directly.
    """
    global data_file_name
    run_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_file_name = file_path[:-4]
    try:
        # Load npy file
        data = np.load(file_path)
        data_num, data_dimension = data.shape
        msg = run_start_time + f" Success: Loaded{file_path}document，Data quantity:{data_num}，number of data points:{data_dimension}\n"
        collect_init_msg(msg)
        return data, data_num, data_dimension
    except IOError:
        if file_path == '':
            print(run_start_time + f" Error: Unable to load empty file\n")
        else:
            print(run_start_time + f" Error: Unable to load {file_path} file\n")
        exit(0)


def read_label_from_npy():
    """
    If a tag is read from a given data path and an IO exception occurs,
    the initialization cannot be completed and the program will exit directly.
    """
    file_path = data_file_name + '_labels.npy'
    run_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Load npy file
        label = np.load(file_path)
        label_num, = label.shape
        return label, label_num
    except IOError:
        print(run_start_time + f" Error: Unable to load{file_path}label file\n")
        exit(0)


def check_label(data_num):
    """
    Check whether the label file exists. If it does not exist, it will initialize and generate a default label file.
    If the amount of excess data is exceeded, it will be trimmed;
    if it is higher than the amount of data, it will be automatically replenished.
    """
    file_path = data_file_name + '_labels.npy'
    run_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if os.path.exists(file_path):
        label, label_num = read_label_from_npy()
        if label_num == data_num:
            msg = run_start_time + f" Success: Loaded{file_path}file,Number of tags：{label_num}\n"
            collect_init_msg(msg)
            return label
        elif data_num > label_num:
            add_label = np.ones(data_num - label_num, dtype=np.int8) * -1
            label = np.append(label, add_label)
            msg = run_start_time + f" Warning: The number of data is greater than the number of tags, \
            it has been automatically added at the end{data_num - label_num}个默认值\n"
            collect_init_msg(msg)
            return label
        else:
            label = label[:data_num]
            msg = run_start_time + f" Warning: The number of data is less than the number of tags, \
            and the end of{label_num - data_num}labels cut off\n"
            collect_init_msg(msg)
            return label
    else:
        label = np.ones(data_num, dtype=np.int8) * -1
        msg = run_start_time + f" Tip: Tag file does not exist{file_path}, has been automatically created and assigned a default value\n"
        collect_init_msg(msg)
        write_label_to_npy(label)
        return label


def write_label_to_npy(label):
    """
    Write the label to the npy file,
    because the data type specified when generating is int8,
    so the writing occupation is relatively small
    """
    file_path = data_file_name + '_labels.npy'
    run_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Save two-dimensional array
        np.save(file_path, label)
        msg = run_start_time + f" Success: Label saved\n"
        collect_init_msg(msg)
    except IOError:
        msg = run_start_time + f" Error: cannot save array to file{data_file_name + file_path}，IOError occurred\n"
        collect_init_msg(msg)
    return msg


def write_data_to_npy(data, label):
    """Write the marked data to the file in the original order"""
    run_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label_one_indexs = np.where(label == 1)[0]
    label_zero_indexs = np.where(label == 0)[0]
    try:
        # Save two-dimensional array
        np.save(data_file_name + '_label_one_datas.npy', data[label_one_indexs])
        print(run_start_time + f" Success: Saved data labels to file{data_file_name + '_label_one_datas.npy'},Number of data items{len(label_one_indexs)}")
    except IOError:
        print(run_start_time + f" Error: cannot save array to file{data_file_name + '_label_one_datas.npy'},IOError occurred\n")
    try:
        # Save two-dimensional array
        np.save(data_file_name + '_label_zero_datas.npy', data[label_zero_indexs])
        print(run_start_time + f" Success: Saved data labels to file{data_file_name + '_label_zero_datas.npy'},Number of data items{len(label_zero_indexs)}")
    except IOError:
        print(run_start_time + f" Error: cannot save array to file{data_file_name + '_label_zero_datas.npy'},IOError occurred\n")


def collect_init_msg(operate_msg):
    """Collect initialization information"""
    msg_table.append("INFO:" + operate_msg)


def sent_init_msg():
    """Send initialization information to the main program"""
    global msg_table
    msg = msg_table.copy()
    msg_table.clear()
    return msg
