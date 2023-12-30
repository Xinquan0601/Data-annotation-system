"""
    Please save the following code to the file "get_initmsg.py"
    This file will create the initialization window
    The initialization window will be automatically closed after the data path is correctly given.
    And return the data path to the system main program
"""
import os
import tkinter as tk

data_file_path = ''


def command_button():
    global data_file_path
    tmp_path = r'{}'.format(path_entry.get())
    if os.path.exists(tmp_path):
        if tmp_path[-4:] != '.npy':
            data_path.set("The input data must be a .npy file!")
            return
        data_file_path = tmp_path
        little_window.destroy()
    else:
        data_path.set("The target file does not exist!")


def get_datafilepath():
    global path_entry
    global little_window
    global data_path
    little_window = tk.Tk()
    little_window.geometry("400x100+300+100")
    little_window.title("Login interface")

    tips = tk.Label(text=r'Absolute path example: C:\Desktop\noise\data.npy')
    tips.place(relx=0.5, rely=0.1, anchor='center')

    data_path = tk.StringVar()
    data_path.set("Please enter the data file path")
    path_entry = tk.Entry(little_window, textvariable=data_path, justify='center')
    path_entry.place(relx=0.5, rely=0.35, anchor='center', relwidth=0.8)

    button = tk.Button(little_window, text="confirm", command=command_button)
    button.place(relx=0.5, rely=0.5, anchor='n')

    path_entry.bind("<Return>", lambda event: button.invoke())

    little_window.mainloop()
    return data_file_path
