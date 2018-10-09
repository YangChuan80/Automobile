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
    for i in range(200):
        indicator += 1
        time.sleep(0.01)

### Thread Management

def start_thread(event):
    global thread
    thread = threading.Thread(target=startCount)
    thread.daemon = True
    
    text_RPM.delete('1.0', tk.END)
    text_RPM.insert('1.0', str(indicator))
    
    thread.start()
    root.after(20, check_thread)

def check_thread():
    if thread.is_alive():
        text_RPM.delete('1.0', tk.END)
        text_RPM.insert('1.0', str(indicator))
        
        root.after(20, check_thread)    

### TKinter Mainflow

root = tk.Tk()

root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
#root.attributes('-fullscreen', True)
root.title('On Board Diagnostics Parser')
#root.iconbitmap('dna.ico')

y0 = 100

text_RPM=tk.Text(root, width=18, height=1, font=('tahoma', 20), bd=2, wrap='none')
text_RPM.place(x=400, y=y0)
label_RPM=tk.Label(root, text='RPM', font=('tahoma', 20))
label_RPM.place(x=400,y=y0-50)

button_count = tk.Button(root, text="Count", width=15, font=('tahoma', 20), command=lambda:start_thread(None))
button_count.place(x=100, y=y0)

root.bind('<Return>', start_thread)

root.mainloop()