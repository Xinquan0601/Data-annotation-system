# Introduction to one-dimensional data labeling system

This is a one-dimensional data labeling system written in Python language. Its main function is to add labels to data and display data waveforms (horizontal priority view and vertical priority view).

## author information:

- Email:1039953448@qq.com

## Development environment:

- PyCharm 2021.3.2 (Community Edition)
-Python 3.9.7
- matplotlib 3.7.1
- numpy 1.24.3
-os
-datatime

# Characteristics of one-dimensional data labeling system

- The default data file is 'data.npy' in the same directory as the script. You can modify the variable data_file_path in the global variable area in sys_framework to switch the data input file. The label file will be in the same directory as the data file, and will be based on the data file. name adjustment.
- The default label file is ‘data_labels.npy’, which is a one-dimensional int8 numpy data, used to correspond to the data and prevent label loss caused by accidents.
- The default labeled data files are 'data_label_one_datas.npy' and 'data_label_zero_datas.npy', which are written when the window is closed. Only the labeled data is written. If the save fails, you can run the program again, close the window and rebuild from 'data_labels.npy'.
- After running the program, it will check whether 'data_labels.npy' exists. If it does not exist, this file will be created and default labels will be written. Otherwise, check whether the labels of ‘data_labels.npy’ are consistent with the amount of input data. If data > label, the default label will be appended to the end; if data < label, the excess label will be cut off.
- The upper part of the window displays two image waveforms for user viewing
- There is a functional area and input area below the image, which are used for data viewing, annotation, and parameter modification. The input area has an error detection function.
- The main information bar of the window displays multiple commonly used data. Commonly used data can be displayed in real time after changes.
- Each time an operation is performed on a component of the window, feedback information will be returned to the bottom and the information bar can be scrolled to run.

#Use of one-dimensional data annotation system

**Note: After using the system, try to exit through the upper right corner of the program form, because there are subsequent operations after the form exit is triggered. If you close it directly in the integrated environment, the marked data will not be updated to the file. But the data
The tags will be saved and you can update the tagged data to the file by closing gracefully on the next run. **
After the data file is correctly given, it will be automatically initialized. Once the initialization is completed, the system can be run.
The main functions in this system are used together with buttons and input boxes. Let’s introduce them below.

## Button function:

- Mark '1': Mark the label of the current data as 1, and then automatically switch to the next data
- Mark '0': Mark the label of the current data as 0, and then automatically switch to the next data
- Previous: switch to the previous data
- Next: switch to the next data
- Find: Switch to the unlabeled data with the smallest index
- Jump: Switch to the data of the page number specified in the input box before the jump button
- Load into painting duration: Set the painting duration as the value in the input box in front of the button, the unit is seconds (s)
- Load to sampling rate: Set the sampling frequency to the value in the input box before the button, the unit is Hertz (Hz)

## Button triggering method:

- All buttons can be triggered by clicking (clicking triggers will not cause continuous operation of the keys)
- The following buttons can be triggered by keyboard shortcuts (key click only operates once; long press operates continuously):
   - Triggered by pressing ‘A’ or ‘a’------marked ‘1’
   - Press key ‘D’ or ‘d’ to trigger------marked with ‘0’
   - Press key 'J' or 'j' to trigger ------Previous
   - Press key 'K' or 'k' to trigger ------Next
   - Press 'L' or 'l' to trigger ------Search
   - Press the 'Enter' button to trigger ------jump
   - Press key 'T' or 't' to trigger ------View switching