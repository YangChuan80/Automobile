import obd
import tkinter as tk
import time
import threading

### OBD Connection

connection = obd.OBD()

### Helper Functions

str_rpm = '0'
str_speed = '0'
str_coolant_temp = '0'
str_fuel_level = '0'
str_engine_load = '0'
str_oil_temp = '0'

def parseAuto():
    global str_rpm, str_speed, str_coolant_temp, str_fuel_level
    
    for i in range(2000):
        # Parameter Adoptions
        cmd_rpm = obd.commands.RPM
        cmd_speed = obd.commands.SPEED
        cmd_coolant_temp = obd.commands.COOLANT_TEMP
        cmd_fuel_level = obd.commands.FUEL_LEVEL
        
        cmd_engine_load = obd.commands.ENGINE_LOAD
        cmd_oil_temp = obd.commands.OIL_TEMP
        cmd_fuel_type = obd.commands.FUEL_TYPE
        
        # Assignment of Values to Varible 'Response'
        response_rpm = connection.query(cmd_rpm)
        response_speed = connection.query(cmd_speed)
        response_coolant_temp = connection.query(cmd_coolant_temp)
        response_fuel_level = connection.query(cmd_fuel_level)
        
        response_engine_load = connection.query(cmd_engine_load)
        response_oil_temp = connection.query(cmd_oil_temp)
        response_fuel_type = connection.query(cmd_fuel_type)
        
        # Change Obj to String
        str_rpm = str(response_rpm.value)
        str_speed = str(response_speed.value)
        str_coolant_temp = str(response_coolant_temp.value)
        str_fuel_level = str(response_fuel_level.value)
        
        str_engine_load = str(response_engine_load.value)
        str_oil_temp = str(response_oil_temp.value)
        str_fuel_type = response_fuel_type.value
        
        
        # Delay Parsing Time
        time.sleep(0.01)

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
    
    text_fuel_type.delete('1.0', tk.END)
    text_fuel_type.insert('1.0', str(str_fuel_type))
    text_oil_temp.delete('1.0', tk.END)
    text_oil_temp.insert('1.0', str(str_oil_temp))
    text_engine_load.delete('1.0', tk.END)
    text_engine_load.insert('1.0', str(str_engine_load))
    
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
        
        text_fuel_type.delete('1.0', tk.END)
        text_fuel_type.insert('1.0', str(str_fuel_type))
        text_oil_temp.delete('1.0', tk.END)
        text_oil_temp.insert('1.0', str(str_oil_temp))
        text_engine_load.delete('1.0', tk.END)
        text_engine_load.insert('1.0', str(str_engine_load))
        
        root.after(20, check_thread)    

### TKinter Mainflow

root = tk.Tk()

root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
#root.attributes('-fullscreen', True)
root.title('KatyOBD -- On Board Diagnostics Parser')
#root.iconbitmap('dna.ico')

y0 = 150
y1 = 400
y2 = 580
y3 = 670

# Label & Edit Box

text_rpm=tk.Text(root, width=10, height=1, font=('tahoma', 80), bd=2, wrap='none')
text_rpm.place(x=50, y=y0)
label_rpm=tk.Label(root, text='RPM', font=('tahoma', 40))
label_rpm.place(x=50,y=y0-100)

text_speed=tk.Text(root, width=10, height=1, font=('tahoma', 80), bd=2, wrap='none')
text_speed.place(x=750, y=y0)
label_speed=tk.Label(root, text='Speed', font=('tahoma', 40))
label_speed.place(x=750,y=y0-100)

text_coolant_temp=tk.Text(root, width=10, height=1, font=('tahoma', 30), bd=2, wrap='none')
text_coolant_temp.place(x=50, y=y1)
label_coolant_temp=tk.Label(root, text='Coolant Temperature', font=('tahoma', 25))
label_coolant_temp.place(x=50,y=y1-80)

text_fuel_level=tk.Text(root, width=10, height=1, font=('tahoma', 30), bd=2, wrap='none')
text_fuel_level.place(x=600, y=y1)
label_fuel_level=tk.Label(root, text='Fuel Level', font=('tahoma', 30))
label_fuel_level.place(x=600,y=y1-80)

text_fuel_type=tk.Text(root, width=15, height=1, font=('tahoma', 30), bd=2, wrap='none')
text_fuel_type.place(x=1000, y=y1)
label_fuel_type=tk.Label(root, text='Fuel Type', font=('tahoma', 30))
label_fuel_type.place(x=1000,y=y1-80)

text_oil_temp=tk.Text(root, width=15, height=1, font=('tahoma', 30), bd=2, wrap='none')
text_oil_temp.place(x=50, y=y2)
label_oil_temp=tk.Label(root, text='Oil Temperature', font=('tahoma', 25))
label_oil_temp.place(x=50,y=y2-80)

text_engine_load=tk.Text(root, width=10, height=1, font=('tahoma', 30), bd=2, wrap='none')
text_engine_load.place(x=600, y=y2)
label_engine_load=tk.Label(root, text='Engine Load', font=('tahoma', 30))
label_engine_load.place(x=600,y=y2-80)

# Buttons

button_start = tk.Button(root, text="Start", width=15, font=('tahoma', 30), command=lambda:start_thread(None))
button_start.place(x=50, y=y3)

root.bind('<Return>', start_thread)

root.mainloop()