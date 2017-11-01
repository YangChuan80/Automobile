import obd
import tkinter as tk
import time
import threading

### OBD Connection

connection = obd.OBD()

### Helper Functions

indicator = 0

def startCount():
    global indicator
    indicator = 0
    while(1):
        indicator += 1
        time.sleep(0.01)

str_rpm = '0'
str_speed = '0'
str_coolant_temp = '0'
str_fuel_level = '0'

def parseAuto():
    global str_rpm, str_speed, str_coolant_temp, str_fuel_level
    
    for i in range(100):
        #connection = obd.OBD()
        cmd_rpm = obd.commands.RPM
        cmd_speed = obd.commands.SPEED
        cmd_coolant_temp = obd.commands.COOLANT_TEMP
        cmd_fuel_level = obd.commands.FUEL_LEVEL

        response_rpm = connection.query(cmd_rpm)
        response_speed = connection.query(cmd_speed)
        response_coolant_temp = connection.query(cmd_coolant_temp)
        response_fuel_level = connection.query(cmd_fuel_level)
        
        str_rpm = str(response_rpm.value)
        str_speed = str(response_speed.value)
        str_coolant_temp = str(response_coolant_temp.value)
        str_fuel_level = str(response_fuel_level.value)
        
        time.sleep(0.01)

def refreshParameters():
    
    connection = obd.OBD()
    cmd_rpm = obd.commands.RPM
    cmd_speed = obd.commands.SPEED
    cmd_coolant_temp = obd.commands.COOLANT_TEMP
    cmd_fuel_level = obd.commands.FUEL_LEVEL

    response_rpm = connection.query(cmd_rpm)
    response_speed = connection.query(cmd_speed)
    response_coolant_temp = connection.query(cmd_coolant_temp)
    response_fuel_level = connection.query(cmd_fuel_level)

    str_rpm = str(response_rpm.value)
    str_speed = str(response_speed.value)
    str_coolant_temp = str(response_coolant_temp.value)
    str_fuel_level = str(response_fuel_level.value)
    
    text_rpm.delete('1.0', tk.END)
    text_rpm.insert('1.0', str(str_rpm))
    text_speed.delete('1.0', tk.END)
    text_speed.insert('1.0', str(str_speed))
    text_coolant_temp.delete('1.0', tk.END)
    text_coolant_temp.insert('1.0', str(str_coolant_temp))
    text_fuel_level.delete('1.0', tk.END)
    text_fuel_level.insert('1.0', str(str_fuel_level))

### Thread Management

def start_thread(event):
    global thread
    thread = threading.Thread(target=parseAuto)
    thread.daemon = True
    
    text_rpm.delete('1.0', tk.END)
    text_rpm.insert('1.0', str(str_rpm))
    text_speed.delete('1.0', tk.END)
    text_speed.insert('1.0', str(str_speed))
    text_coolant_temp.delete('1.0', tk.END)
    text_coolant_temp.insert('1.0', str(str_coolant_temp))
    text_fuel_level.delete('1.0', tk.END)
    text_fuel_level.insert('1.0', str(str_fuel_level))
    
    thread.start()
    root.after(20, check_thread)

def check_thread():
    if thread.is_alive():
        text_rpm.delete('1.0', tk.END)
        text_rpm.insert('1.0', str(str_rpm))
        text_speed.delete('1.0', tk.END)
        text_speed.insert('1.0', str(str_speed))
        text_coolant_temp.delete('1.0', tk.END)
        text_coolant_temp.insert('1.0', str(str_coolant_temp))
        text_fuel_level.delete('1.0', tk.END)
        text_fuel_level.insert('1.0', str(str_fuel_level))
        
        root.after(20, check_thread)    

### TKinter Mainflow

root = tk.Tk()

root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
#root.attributes('-fullscreen', True)
root.title('On Board Diagnostics Parser')
#root.iconbitmap('dna.ico')

y0 = 150
y1 = 400

text_rpm=tk.Text(root, width=10, height=1, font=('tahoma', 80), bd=2, wrap='none')
text_rpm.place(x=100, y=y0)
label_rpm=tk.Label(root, text='RPM', font=('tahoma', 40))
label_rpm.place(x=100,y=y0-100)

text_speed=tk.Text(root, width=10, height=1, font=('tahoma', 80), bd=2, wrap='none')
text_speed.place(x=800, y=y0)
label_speed=tk.Label(root, text='Speed', font=('tahoma', 40))
label_speed.place(x=800,y=y0-100)

text_coolant_temp=tk.Text(root, width=10, height=1, font=('tahoma', 30), bd=2, wrap='none')
text_coolant_temp.place(x=100, y=y1)
label_coolant_temp=tk.Label(root, text='Coolant Temperature', font=('tahoma', 30))
label_coolant_temp.place(x=100,y=y1-80)

text_fuel_level=tk.Text(root, width=10, height=1, font=('tahoma', 30), bd=2, wrap='none')
text_fuel_level.place(x=700, y=y1)
label_fuel_level=tk.Label(root, text='Fuel Level', font=('tahoma', 30))
label_fuel_level.place(x=700,y=y1-80)


button_start = tk.Button(root, text="Start", width=15, font=('tahoma', 20), command=lambda:start_thread(None))
button_start.place(x=100, y=y0+350)

button_refresh = tk.Button(root, text="Refresh", width=15, font=('tahoma', 20), command=refreshParameters)
button_refresh.place(x=700, y=y0+350)

root.bind('<Return>', start_thread)

root.mainloop()