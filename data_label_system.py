"""
    This system is run by Python 3.9.7
    Do not modify variables unless it is necessary
    You must ensure what consequences your operation will lead to
    Designer:ChenXinQuan
    Email:1039953448@qq.com
    Date:2023/5/26
"""
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

import numpy as np
from matplotlib import font_manager
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from base_functions import read_data_from_npy, check_label, write_label_to_npy, sent_init_msg, write_data_to_npy
from get_initmsg import get_datafilepath

# ------------------Initialization--------------------Initialization--------------------Initialization------------------- #
"""
    Initialization of required data before main system work
"""
data_file_path = get_datafilepath()
current_index = 1
data, data_num, data_dimension = read_data_from_npy(data_file_path)
label = check_label(data_num)
no_tagged_index = np.where(label == -1)[0]
info_msg = ''.join(sent_init_msg())
guide_msg = "INFO:" + " Use the following key shortcuts：\t   Q：Mark 1\t   E：Mark 0\t   J：Previous\t   K：Next\t   L：Find\t   T：Switch view   Enter：Confirm jump\n"
info_msg = guide_msg + info_msg
sample_freq = int(data_dimension / 2)
time_length = 0.5
show_mode = True
residue_num = len(no_tagged_index)
tagged_num = data_num - residue_num
font = font_manager.FontProperties(family='SimHei')


# ----------Command and function area----------Command and function area----------Command and function area---------- #


def command_last():
    """Command: Jump to the previous data"""
    run_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    global info_msg
    global current_index
    global data_num
    current_index -= 1
    if current_index < 1:  # Prevent index overflow
        current_index = data_num
    info_msg = "INFO:" + run_start_time + f' Success: Jumped to the previous data, currently NO.{current_index} data\n'
    page_var.set(str(current_index))
    current_tag_var.set(f"Current label:{label[current_index - 1]}")
    change_wave()  # change waveform
    output_info()  # Output running information


def command_next():
    """Command: jump to next data"""
    run_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    global info_msg
    global current_index
    global data_num
    current_index += 1
    if current_index > data_num:  # Prevent index overflow
        current_index = 1
    info_msg = "INFO:" + run_start_time + f' Success: Jumped to the next data, currently NO.{current_index} data\n'
    page_var.set(str(current_index))
    current_tag_var.set(f"Current label:{label[current_index - 1]}")
    change_wave()  # change waveform
    output_info()  # Output running information


def command_find():
    """Command: Find unlabeled data with the lowest index"""
    run_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    global info_msg
    global current_index
    global no_tagged_index
    no_tagged_index = np.where(label == -1)[0]  # Get only the lowest index
    if len(no_tagged_index) == 0:
        info_msg = "INFO:" + run_start_time + ' Tip: Unlabeled data not found\n'
        output_info()
        return
    current_index = no_tagged_index[0] + 1  # Index and order correspondence
    info_msg = "INFO:" + run_start_time + f' Success: Unlabeled data found, jump to NO.{current_index} data\n'
    page_var.set(str(current_index))
    current_tag_var.set(f"Current label:{label[current_index - 1]}")
    change_wave()
    output_info()


def command_goto():
    """Command: Jump to the specified page number"""
    run_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    global info_msg
    global current_index
    goto_index = page_entry.get()
    try:
        current_index = int(goto_index)  # Do integer conversion exception handling
    except ValueError:
        info_msg = "INFO:" + run_start_time + f" Error: Jump to NO.‘{goto_index}’ illegal\n"
        page_var.set(str(current_index))
        output_info()
        return
    info_msg = "INFO:" + run_start_time + f' Success: Jumped to N0.{current_index} data\n'
    page_var.set(str(current_index))
    current_tag_var.set(f"Current label:{label[current_index - 1]}")
    change_wave()
    output_info()


def command_one():
    """Mark the data as 1 while saving directly to the label file"""
    global info_msg
    global current_index, no_tagged_index
    global tagged_num, residue_num
    run_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label[current_index - 1] = 1
    info_msg = write_label_to_npy(label)  # Only write data corresponding to int8 tag 1, fast and efficient, and prevent loss
    info_msg = "INFO:" + run_start_time + f" Success: No.{current_index} data has been marked as 1\n"
    no_tagged_index = np.where(label == -1)[0]
    residue_num = len(no_tagged_index)
    tagged_num = data_num - residue_num
    residue_num_var.set(f"Total Number of Unmarked Instances:{residue_num}")
    tagged_num_var.set(f"Total Number of Marked Instances:{tagged_num}")
    output_info()
    command_next()


def command_zero():
    """Mark the data as 0 and save the data to the label"""
    global info_msg
    global current_index, no_tagged_index
    global tagged_num, residue_num
    run_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label[current_index - 1] = 0
    info_msg = write_label_to_npy(label)  # Only write data corresponding to int8 tag 0, fast and efficient, and prevent loss
    info_msg = "INFO:" + run_start_time + f" Success: No.{current_index} data has been marked as 0\n"
    no_tagged_index = np.where(label == -1)[0]
    residue_num = len(no_tagged_index)
    tagged_num = data_num - residue_num
    residue_num_var.set(f"Total Number of Unmarked Instances:{residue_num}")
    tagged_num_var.set(f"Total Number of Marked Instances:{tagged_num}")
    output_info()
    command_next()


def command_sample_freq():
    """Load the number in the input box to the sampling frequency to change the image"""
    run_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    global sample_freq
    global input_var
    global info_msg
    temp = input_entry.get()
    try:
        sample_freq = int(temp)  # Perform shaping exception handling on the sampling rate to prevent crashes
        input_var.set("Enter number here")
        sample_freq_var.set(f"Sampling Rate:{sample_freq}Hz")
        info_msg = "INFO:" + run_start_time + f" Success: The sampling rate has been set to{sample_freq}Hz\n"
    except ValueError:
        info_msg = "INFO:" + run_start_time + f" Failure: Sample rate set to‘{temp}’不合法\n"
        input_var.set("Enter number here")
    change_wave()
    output_info()


def command_time_length():
    """Load numbers into the paint duration to alter the image"""
    run_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    global time_length
    global input_var
    global info_msg
    temp = input_entry.get()
    try:
        time_length = float(temp)  # Perform floating-point exception handling on painting duration to prevent crashes
        input_var.set("Enter number here")
        # time_length_var.set(f"绘画时长:{time_length}s")  # No need to use it temporarily
        info_msg = "INFO:" + run_start_time + f" Success: The painting duration has been set to{time_length}s\n"

    except ValueError:
        info_msg = "INFO:" + run_start_time + f" Failure: Paint duration set to‘{temp}’illegal\n"
        input_var.set("Enter number here")
    change_wave()
    output_info()


def command_close():
    """Command: Close the window and classify the marked data"""
    print("Saving data, please wait...")
    write_data_to_npy(data=data, label=label)  # Write the labeled data to the corresponding labeled data file
    window.destroy()  # Destroy window
    print("Exited successfully！")


def change_frame(event=None):
    """Switch views, triggered only by key presses"""
    global show_mode
    if show_mode:  # show_mode持续取反对应两种视图
        master_wave_frame.place(relx=0, rely=0, anchor='nw', relwidth=0.5, relheight=0.65)
        magnify_wave_frame.place(relx=0.5, rely=0, anchor='nw', relwidth=0.5, relheight=0.65)
        master_fig.subplots_adjust(left=0.08, right=0.97, top=0.94, bottom=0.06)
        magnify_fig.subplots_adjust(left=0.08, right=0.97, top=0.94, bottom=0.06)
    else:
        master_wave_frame.place(relx=0, rely=0, anchor='nw', relwidth=1, relheight=0.325)
        magnify_wave_frame.place(relx=0, rely=0.325, anchor='nw', relwidth=1, relheight=0.325)
        master_fig.subplots_adjust(left=0.04, right=0.97, top=0.88, bottom=0.11)
        magnify_fig.subplots_adjust(left=0.04, right=0.97, top=0.88, bottom=0.11)
    show_mode = not show_mode


def change_wave():
    """Changing waveform data is called as a basic function, not a command"""
    global current_index
    global fig1, fig2
    global canvas, canvas1
    global time_length, sample_freq
    global show_mode
    fig1.cla()  # Clear the last drawing so that the data can be drawn again
    fig2.cla()
    fig1.plot(data[current_index - 1][-int(sample_freq * time_length):])
    fig2.plot(data[current_index - 1][-int(sample_freq * 0.25):])
    fig1.set_title(f"The Last {time_length} Seconds Image", fontproperties=font, fontsize=18, fontweight="bold")
    fig2.set_title("The Last 0.25 Seconds Image", fontproperties=font, fontsize=18, fontweight="bold")

    canvas.draw()  # Draw the image in memory for display
    canvas1.draw()
    canvas.get_tk_widget().place(relx=0, rely=0, anchor='nw', relwidth=1, relheight=1)
    canvas1.get_tk_widget().place(relx=0, rely=0, anchor='nw', relwidth=1, relheight=1)


def on_click_out(event):
    """Limit the components that the mouse can operate"""
    # When the left mouse button clicks outside the input box, move the cursor out of the input box
    if event.widget not in (page_entry, input_entry, info_text):
        window.focus()


def output_info():
    """Output information to the interface frontend"""
    info_text.configure(state='normal')
    info_text.insert(tk.END, info_msg)
    info_text.configure(state='disabled')
    info_text.see(tk.END)


# ---------------graphics frame area--------------graphics frame area--------------graphics frame area------------- #
"""Define a main window to receive subsequent components"""
window = tk.Tk()
window.geometry('1680x980+100+10')

window.minsize(1100, 680)  # Limit the minimum size to ensure the layout displays correctly
window.title("Data annotation system (recommended to use in full screen)")

# --------------------Picture 1 frame---------------------- #
"""Define a main picture frame and embed the picture canvas with the specified painting time"""
master_wave_frame = tk.Frame(window)
master_wave_frame.place(relx=0, rely=0, anchor='nw', relwidth=1, relheight=0.325)

master_fig = Figure()
fig1 = master_fig.add_subplot(111)  # Add sub-picture: 1 row 1 column 1
fig1.plot(data[current_index - 1][data_dimension - int(sample_freq * time_length):])
fig1.set_title(f"The Last {time_length} Seconds Image", fontproperties=font, fontsize=18, fontweight="bold")
master_fig.subplots_adjust(left=0.04, right=0.97)

canvas = FigureCanvasTkAgg(master_fig, master=master_wave_frame)
canvas.draw()
canvas.get_tk_widget().place(relx=0, rely=0, anchor='nw', relwidth=1, relheight=1)
# --------------------Picture 1 frame---------------------- #


# --------------------Picture 2 frame---------------------- #
"""Define a magnification frame and embed the picture canvas for the next 0.25 seconds"""
magnify_wave_frame = tk.Frame(window)
magnify_wave_frame.place(relx=0, rely=0.325, anchor='nw', relwidth=1, relheight=0.325)

magnify_fig = Figure()
fig2 = magnify_fig.add_subplot(111)  # Add sub-picture: 1 row 1 column 1
fig2.plot(data[current_index - 1][-int(sample_freq * 0.25):])
magnify_fig.subplots_adjust(left=0.04, right=0.97)

fig2.set_title("The Last 0.25 Seconds Image", fontproperties=font, fontsize=18, fontweight="bold")

canvas1 = FigureCanvasTkAgg(magnify_fig, master=magnify_wave_frame)
canvas1.draw()
canvas1.get_tk_widget().place(relx=0, rely=0, anchor='nw', relwidth=1, relheight=1)
# --------------------Picture 2 frame--------------------- #


# --------------------button frame------------------------- #
"""This framework corresponds to all components of the functional area and input area"""
my_style = ttk.Style()  # Create topic
my_style.configure('my.TFrame', borderwidth=10, relief='ridge', background='#FAFAFA', shadow=True)

button_frame = ttk.Frame(window, style='my.TFrame')  # Frame with themes to beautify the interface
button_frame.place(relx=0, rely=0.65, anchor='nw', relwidth=1, relheight=0.1)

function_area_label = tk.Label(button_frame, text="Function area:", height=1, font=('Arial', 16, 'bold',), bg='#FAFAFA')
function_area_label.place(relx=0.01, rely=0.25, anchor='w')

one_button = tk.Button(button_frame, text='Marked as 1', width=10, height=1, command=command_one)
one_button.place(relx=0.156, rely=0.0675, anchor='nw')

zero_button = tk.Button(button_frame, text='Marked as 0', width=10, height=1, command=command_zero)
zero_button.place(relx=0.234, rely=0.0675, anchor='nw')

last_button = tk.Button(button_frame, text='Previous data', width=10, height=1, command=command_last)
last_button.place(relx=0.117, rely=0.54, anchor='nw')

next_button = tk.Button(button_frame, text='Next data', width=10, height=1, command=command_next)
next_button.place(relx=0.195, rely=0.54, anchor='nw')

find_button = tk.Button(button_frame, text='Find data', width=10, height=1, command=command_find)
find_button.place(relx=0.273, rely=0.54, anchor='nw')

input_area_label = tk.Label(button_frame, text="Input area:", height=1, font=('Arial', 16, 'bold',), bg='#FAFAFA')
input_area_label.place(relx=0.48, rely=0.25, anchor='w')

input_var = tk.StringVar()
input_var.set("Please enter the number")
input_entry = tk.Entry(button_frame, width=20, textvariable=input_var)
input_entry.place(relx=0.653, rely=0.162, anchor='ne')

sample_freq_button = tk.Button(button_frame, text='Load to sample rate', width=22, height=1, command=command_sample_freq)
sample_freq_button.place(relx=0.656, rely=0.0675, anchor='nw')

time_length_button = tk.Button(button_frame, text='Load to painting time', width=22, height=1, command=command_time_length)
time_length_button.place(relx=0.78, rely=0.0675, anchor='nw')

page_var = tk.StringVar()
page_var.set(str(current_index))
page_entry = tk.Entry(button_frame, textvariable=page_var, width=5, justify='right')
page_entry.place(relx=0.684, rely=0.608, anchor='ne')

data_num_label = tk.Label(button_frame, text=f"of {data_num}", height=1, bg='#FAFAFA')
data_num_label.place(relx=0.731, rely=0.608, anchor='ne')

goto_button = tk.Button(button_frame, text='Goto', width=8, height=1, command=command_goto)
goto_button.place(relx=0.734, rely=0.54, anchor='nw')

# --------------------button frame------------------------ #


# --------------------component binding framework--------------------- #
"""Some components are mapped to the keyboard to increase efficiency"""
window.bind("Q", lambda event: one_button.invoke())
window.bind("q", lambda event: one_button.invoke())

window.bind("E", lambda event: zero_button.invoke())
window.bind("e", lambda event: zero_button.invoke())

window.bind("<J>", lambda event: last_button.invoke())
window.bind("<j>", lambda event: last_button.invoke())

window.bind("<K>", lambda event: next_button.invoke())
window.bind("<k>", lambda event: next_button.invoke())

window.bind("<L>", lambda event: find_button.invoke())
window.bind("<l>", lambda event: find_button.invoke())

page_entry.bind("<Return>", lambda event: goto_button.invoke())
window.bind("<T>", change_frame)
window.bind("<t>", change_frame)
window.bind('<Button-1>', on_click_out)
# --------------------component binding framework--------------------- #


# --------------------Always displayed data frame--------------------- #
"""Add a frame for data that needs to be viewed frequently to facilitate viewing"""
const_msg_frame = ttk.Frame(window, style='my.TFrame')
const_msg_frame.place(relx=0, rely=0.75, anchor='nw', relwidth=1, relheight=0.05)

main_msg_var = tk.StringVar()
main_msg_var.set(f"Key information:")
main_msg_label = tk.Label(const_msg_frame, textvariable=main_msg_var, height=1,
                          font=('Arial', 16, 'bold',), bg='#FAFAFA')
main_msg_label.place(relx=0.008, rely=0.5, anchor='w')

sample_freq_var = tk.StringVar()
sample_freq_var.set(f"Sampling Rate:{sample_freq}Hz")
sample_freq_label = tk.Label(const_msg_frame, textvariable=sample_freq_var, height=1,
                             font=('Arial', 12, 'bold'), bg='#FAFAFA')
sample_freq_label.place(relx=0.14, rely=0.5, anchor='w')

time_length_var = tk.StringVar()
time_length_var.set(f"Drawing time:{time_length}s")
time_length_label = tk.Label(const_msg_frame, textvariable=time_length_var, font=('Arial', 12, 'bold'), bg='#FAFAFA')
# time_length_label.place(relx=0.258, rely=0.5, anchor='w') # No need to place it temporarily

data_num_var = tk.StringVar()
data_num_var.set(f"Number of Data:{data_num}")
data_num_label = tk.Label(const_msg_frame, textvariable=data_num_var, font=('Arial', 12, 'bold'), bg='#FAFAFA')
data_num_label.place(relx=0.27, rely=0.5, anchor='w')

data_points_var = tk.StringVar()
data_points_var.set(f"number of data points:{data_dimension}")
data_points_label = tk.Label(const_msg_frame, textvariable=data_points_var, font=('Arial', 12, 'bold'), bg='#FAFAFA')
# data_points_label.place(relx=0.508, rely=0.5, anchor='w') # No need to place it temporarily

tagged_num_var = tk.StringVar()
tagged_num_var.set(f"Total Number of Marked Instances:{tagged_num}")
tagged_num_label = tk.Label(const_msg_frame, textvariable=tagged_num_var, font=('Arial', 12, 'bold'), bg='#FAFAFA')
tagged_num_label.place(relx=0.42, rely=0.5, anchor='w')

residue_num_var = tk.StringVar()
residue_num_var.set(f"Total Number of Unmarked Instances:{residue_num}")
residue_num_label = tk.Label(const_msg_frame, textvariable=residue_num_var, font=('Arial', 12, 'bold'), bg='#FAFAFA')
residue_num_label.place(relx=0.64, rely=0.5, anchor='w')

current_tag_var = tk.StringVar()
current_tag_var.set(f"Current Label:{label[current_index - 1]}")
current_tag_label = tk.Label(const_msg_frame, textvariable=current_tag_var, font=('Arial', 12, 'bold'), bg='#FAFAFA')
current_tag_label.place(relx=0.90, rely=0.5, anchor='w')
# --------------------Always displayed data frame--------------------- #


# --------------------Run the data frame--------------------- #
"""将运行中的反馈信息主要信息反馈到主窗口"""
run_msg_frame = tk.Frame(window)
run_msg_frame.place(x=0, rely=0.8, anchor='nw', relwidth=1, relheight=0.2)

info_text = ScrolledText(run_msg_frame, spacing1=4, foreground='blue', padx=10)
info_text.insert(tk.END, info_msg)
info_text.configure(state='disabled')
info_text.place(x=0, y=0, anchor='nw', relwidth=1, relheight=1)
# --------------------Run the data frame--------------------- #


window.protocol("WM_DELETE_WINDOW", command_close)
window.mainloop()
