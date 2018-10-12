import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font as tkf
import sqlite3
import datetime

from libvin.decoding import Vin

## DB Connection

DB_file = 'GessnerDB.sqlite'
conn = sqlite3.connect(DB_file)
cur = conn.cursor()

sqlstr = 'SELECT * FROM VIN'

spreadsheet = cur.execute(sqlstr)

headers_db = []

for unit in spreadsheet.description:
    headers_db.append(unit[0])

combination = []

for row_tuple in spreadsheet:
    combination.append(list(row_tuple[:6]) + list(row_tuple[6]) + list(row_tuple[7:]))

## Table Related

def ExtractID(iden): 
    sqlstr = 'SELECT * FROM VIN WHERE VIN.id = ?'
    cur.execute(sqlstr, (iden,))
    rowSelected = cur.fetchone()
   
    item = {}    
    for i in range(len(rowSelected)):
        item[headers_db[i]] = rowSelected[i]
   
    display_in_text(item)

def OnDoubleClick(event):
    global idglb
    try:
        item = table.selection()[0]
        value = table.item(item, 'values')    
        iden = value[0]
        ExtractID(iden)     
        idglb = iden
        
    except:
        pass

def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))

def refreshDB():
    global conn, cur, desc, headers, combination
    conn.close()
    conn = sqlite3.connect(DB_file)
    cur = conn.cursor()

    cur.execute('SELECT * FROM VIN')
    
    sqlstr = 'SELECT * FROM VIN ORDER BY VIN.id'
    
    spreadsheet = cur.execute(sqlstr)

    combination = []
    
    for row_tuple in spreadsheet:
        combination.append(list(row_tuple[:6]) + list(row_tuple[6]) + list(row_tuple[7:]))

def display_in_text(item):
    
    text_id.delete('1.0', tk.END)
    text_id.insert('1.0', item['id'])
    
    text_brand.delete('1.0', tk.END)
    text_brand.insert('1.0', item['Brand'])
    
    text_make.delete('1.0', tk.END)
    text_make.insert('1.0', item['Make'])  
    
    text_color.delete('1.0', tk.END)
    text_color.insert('1.0', item['Color'])  
    
    text_bodyStyle.delete('1.0', tk.END)
    text_bodyStyle.insert('1.0', item['BodyStyle'])  
    
    text_engine.delete('1.0', tk.END)
    text_engine.insert('1.0', item['Engine'])
    
    text_VIN.delete('1.0', tk.END)
    text_VIN.insert('1.0', item['VIN']) 
    
    # ////////////////////////////
    
    text_WMI.delete('1.0', tk.END)
    text_WMI.insert('1.0', item['VIN'][:3]) 
    
    text_VDS.delete('1.0', tk.END)
    text_VDS.insert('1.0', item['VIN'][3:9]) 
    
    text_VIS.delete('1.0', tk.END)
    text_VIS.insert('1.0', item['VIN'][9:]) 

def display_in_table(combination):
    for row in combination:
        table.insert("", "end", "", values=row)
    num = str(len(combination))
    text_num.delete('1.0', tk.END)
    text_num.insert('1.0', num)

def clear():
    for i in table.get_children():
        table.delete(i)

## Button Functions

def browse():
    clear()
    #refreshDB()
    display_in_table(combination)

def new():
    root_new = tk.Tk()
    
    w = 980 # width for the Tk root
    h = 540 # height for the Tk root

    # get screen width and height
    ws = root_new.winfo_screenwidth() # width of the screen
    hs = root_new.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    root_new.geometry('%dx%d+%d+%d' % (w, h, x, y))   
    root_new.title('New Patient')
    
    time_text = str(datetime.datetime.now())[-5:]
    
    id = ''
    
    for t in time_text:
        if t!=' 'and t!= '-' and t != ':' and t != '.':
            id += t
    
    def create():
        #try:        
            id_gotten = int(text_id_new.get('1.0', tk.END).rstrip())
            brand_gotten = text_brand_new.get('1.0', tk.END).rstrip()
            make_gotten = text_make_new.get('1.0', tk.END).rstrip()
            color_gotten = text_color_new.get('1.0', tk.END).rstrip()
            bodyStyle_gotten = text_bodyStyle_new.get('1.0', tk.END).rstrip()
            engine_gotten = text_engine_new.get('1.0', tk.END).rstrip()        
            VIN_gotten = text_VIN_new.get('1.0', tk.END).rstrip()
            comments_gotten = text_comments_new.get('1.0', tk.END).rstrip()            
            
            
            Question_mark = '(' + '?, ' * 7 + '?)'

            Update_values = (
                             id_gotten, 
                             brand_gotten,
                             make_gotten,
                             color_gotten,
                             bodyStyle_gotten,
                             engine_gotten, 
                             VIN_gotten,
                             comments_gotten
                             )

            Update_Fields = "(id, Brand, Make, Color, BodyStyle, Engine, VIN, comments)"

            cur.execute('INSERT INTO VIN '+ Update_Fields + ' VALUES ' + Question_mark, 
                        Update_values)
            conn.commit()  

            messagebox.showinfo("Created", "Vehicle information successfully created!")
                        
            clear()
            refreshDB()
            display_in_table(combination)
            root_new.destroy()
                
        #except:
            #pass

    # ///////// Main Stream ////////////////////////
    
    y_origin = 80
    gain = 50
    i = 0
    
     # ///////////// Raised Label Block ////////////////////////////////////////////////

    label_new = tk.Label(root_new,width=135, height=23 , relief='raised', borderwidth=1)
    label_new.place(x=10,y=y_origin+i*gain-40)
    
    # ///////////// Routine Edits////////////////          

    text_brand_new = tk.Text(root_new, width=30, height=1, font=('tahoma', 8), wrap='none')
    text_brand_new.place(x= 90, y= y_origin + i * gain)
    label_brand_new = tk.Label(root_new, text='Brand:', font=('tahoma', 8))
    label_brand_new.place(x = 90, y = y_origin + i * gain - 25)

    text_make_new = tk.Text(root_new, width=35, height=1, font=('tahoma', 8), wrap='none')
    text_make_new.place(x= 320, y= y_origin + i * gain)
    label_make_new = tk.Label(root_new, text='Make:', font=('tahoma', 8))
    label_make_new.place(x = 320, y = y_origin + i * gain - 25)

    text_color_new = tk.Text(root_new, width=15, height=1, font=('tahoma', 8), wrap='none')
    text_color_new.place(x= 580, y= y_origin + i * gain)
    label_color_new = tk.Label(root_new, text='Color:', font=('tahoma', 8))
    label_color_new.place(x = 580, y = y_origin + i * gain - 25)
    
    i = 1

    text_bodyStyle_new = tk.Text(root_new, width=28, height=1, font=('tahoma', 8), wrap='none')
    text_bodyStyle_new.place(x= 90, y= y_origin + i * gain)
    label_bodyStyle_new = tk.Label(root_new, text='Body Style:', font=('tahoma', 8))
    label_bodyStyle_new.place(x = 90, y = y_origin + i * gain - 25)

    text_engine_new = tk.Text(root_new, width=35, height=1, font=('tahoma', 8), wrap='none')
    text_engine_new.place(x= 320, y= y_origin + i * gain)
    label_engine_new = tk.Label(root_new, text='Engine:', font=('tahoma', 8))
    label_engine_new.place(x = 320, y = y_origin + i * gain - 25)
    
    text_id_new = tk.Text(root_new, width=35, height=1, font=('tahoma', 8), wrap='none')
    text_id_new.place(x= 320, y= y_origin + i * gain)
    label_id_new = tk.Label(root_new, text='ID:', font=('tahoma', 8))
    label_id_new.place(x = 320, y = y_origin + i * gain - 25)
    
    text_id_new.delete('1.0', tk.END)
    text_id_new.insert('1.0', id)  
    
    i = 2

    text_VIN_new = tk.Text(root_new, width=45, height=1, font=('tahoma', 8), wrap='none')
    text_VIN_new.place(x=90, y= y_origin + i * gain)
    label_VIN_new = tk.Label(root_new, text='VIN:', font=('tahoma', 8))
    label_VIN_new.place(x=90,y= y_origin + i * gain - 25)
    
    i = 3
    
    text_comments_new = tk.Text(root_new, width=80, height=1, font=('tahoma', 8), wrap='none')
    text_comments_new.place(x= 90, y= y_origin + i * gain)
    label_comments_new = tk.Label(root_new, text='Comments', font=('tahoma', 8))
    label_comments_new.place(x = 90, y = y_origin + i * gain - 25)
    
    # ////// Buttons //////////////////////////
    
    i = 5 
    
    button_add=ttk.Button(root_new, text='Create', width=15, command=create)
    button_add.place(x=300, y=y_origin+i*gain)

    button_cancel=ttk.Button(root_new, text='Cancel', width=15, command=root_new.destroy)
    button_cancel.place(x=650, y=y_origin+i*gain)      
    
    root_new.mainloop()

def update():
    try:        
        id_gotten = text_id.get('1.0', tk.END).rstrip()        
        brand_gotten = text_brand.get('1.0', tk.END).rstrip()
        make_gotten = text_make.get('1.0', tk.END).rstrip()
        color_gotten = text_color.get('1.0', tk.END).rstrip()
        bodyStyle_gotten = text_bodyStyle.get('1.0', tk.END).rstrip()
        engine_gotten = text_engine.get('1.0', tk.END).rstrip()        
        VIN_gotten = text_VIN.get('1.0', tk.END).rstrip()
        comments_gotten = text_comments.get('1.0', tk.END).rstrip()
        
        if len(VIN_gotten) != 17:
            messagebox.showwarning("Invalid VIN length", 
                                   "Sorry, the length of the VIN you have input is wrong. Please check!")
        else:       
                
            Question_mark = '(' + '?, ' * 7 + '?)'

            cur.execute('DELETE FROM VIN WHERE id = ?', (id_gotten,))        
            conn.commit()

            Update_values = (
                             id_gotten, 
                             brand_gotten,
                             make_gotten,
                             color_gotten,
                             bodyStyle_gotten,
                             engine_gotten, 
                             VIN_gotten,
                             comments_gotten
                             )


            Update_Fields = "(id, Brand, Make, Color, BodyStyle, Engine, VIN, comments)"

            cur.execute('INSERT INTO VIN '+ Update_Fields + ' VALUES ' + Question_mark, 
                        Update_values)
            conn.commit()  

            messagebox.showinfo("Updated", "Vehicle information successfully updated!")
            clear()
            refreshDB()
            display_in_table(combination)
        
    except:
        pass

def delete():
    id_gotten = text_id.get('1.0', tk.END).rstrip()

    if id_gotten == '':
        messagebox.showinfo("Empty", "There's no vehicle information to delete. Please make sure.")

    else:           
        result = messagebox.askquestion('Delete', 'Are you sure to delete this vehicle information?', 
                                        icon='warning')

        if result == 'yes':
            cur.execute('DELETE FROM VIN WHERE id = ?', (id_gotten,))        
            conn.commit()            
            messagebox.showinfo("Deleted", "Vehicle information has been deleted!")

            # //////////////////// Refresh the Table ///////////////////////////////////////////////////
            # Clear the table
            for i in table.get_children():
                table.delete(i)

            # Refresh the whole database
            refreshDB()

            # Refresh variable combination

            sqlstr = 'SELECT * FROM VIN ORDER BY id'
            spreadsheet = cur.execute(sqlstr)
            
            combination = []
    
            for row_tuple in spreadsheet:
                combination.append(list(row_tuple[:6]) + list(row_tuple[6]) + list(row_tuple[7:]))

            # Display the table        
            display_in_table(combination)

def decode():    
    vin_input = text_VIN.get('1.0', tk.END)[:17]   
    
    if len(vin_input) != 17:
        messagebox.showwarning("Invalid VIN length", 
                               "Sorry, the length of the VIN you have input is wrong. Please check!")
    
    else:   

        # Capitalization:
        vin = vin_input.upper()
        
        try:
            # Parse VIN
            v = Vin(vin)            

            year = v.year    
            country = v.country
            region = v.region.capitalize()
            manufacturer = v.manufacturer
            make = v.make

            # Differentiate Year:    
            if year < 2000:
                year = year + 30

            # Parameters
            text_region.delete('1.0', tk.END)
            text_region.insert('1.0', region)  

            text_country.delete('1.0', tk.END)
            text_country.insert('1.0', country)  

            text_manufacturer.delete('1.0', tk.END)
            text_manufacturer.insert('1.0', manufacturer)  

            text_make_decode.delete('1.0', tk.END)
            text_make_decode.insert('1.0', make)  

            text_year.delete('1.0', tk.END)
            text_year.insert('1.0', year)     
            
        except:            
            messagebox.showwarning("Invalid VIN", "Sorry, the VIN you input is invalid. Please check!")  

def about():
    messagebox.showinfo("About", "Author: Chuan Yang")

## Main Stream

root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
#root.attributes('-fullscreen', True)
root.title('Gessner VIN')
#root.iconbitmap('CharlestonParkIcon.ico')

### Table Control

headers = ['id', 'Brand', 'Make', 'Color', 'Body Style', 'Engine',
           '1', '2', '3', '4', '5', 
           '6', '7', '8', '9', '10', 
           '11', '12', '13', '14', '15', 
           '16', '17', 'Comments']
header_widths = [10, 80, 100, 60, 60, 80,
                 30, 30, 60, 30, 30, 
                 30, 30, 30, 60, 30, 
                 60, 30, 30, 30, 30, 
                 30, 30, 40]

# Multicolumn Listbox/////////////////////////////////////////////////////////////////////////////
table = ttk.Treeview(root, height="20", columns=headers, selectmode="extended")
table.pack(padx=10, pady=20, ipadx=1200, ipady=200)

i = 1
for header in headers:
    table.heading('#'+str(i), text=header.title(), anchor=tk.W, command=lambda c=header: sortby(table, c, 0))
    table.column('#'+str(i), stretch=tk.NO, minwidth=0, width=tkf.Font().measure(header.title())+header_widths[i-1])
    i+=1    
table.column('#0', stretch=tk.NO, minwidth=0, width=0)

table.bind("<Double-1>", OnDoubleClick)
#///////////////////////////////////////////////////////////////////////////////////////////

# Scrollbar////////////////////////////////////////////////////////////////////////////////////////
vsb = ttk.Scrollbar(table, orient = "vertical",  command = table.yview)
hsb = ttk.Scrollbar(table, orient = "horizontal", command = table.xview)
## Link scrollbars activation to top-level object
table.configure(yscrollcommand = vsb.set, xscrollcommand = hsb.set)
## Link scrollbar also to every columns
map(lambda col: col.configure(yscrollcommand = vsb.set, xscrollcommand = hsb.set), table)
vsb.pack(side = tk.RIGHT, fill = tk.Y)
hsb.pack(side = tk.BOTTOM, fill = tk.X) 

### Other Controls

y_origin = 560
gain = 60
i = 0

text_id = tk.Text(root, width=3, height=1, font=('tahoma', 8), wrap='none')
text_id.place(x= 40, y= y_origin + i * gain)

text_brand = tk.Text(root, width=30, height=1, font=('tahoma', 8), wrap='none')
text_brand.place(x= 90, y= y_origin + i * gain)
label_brand = tk.Label(root, text='Brand:', font=('tahoma', 8))
label_brand.place(x = 90, y = y_origin + i * gain - 25)

text_make = tk.Text(root, width=35, height=1, font=('tahoma', 8), wrap='none')
text_make.place(x= 320, y= y_origin + i * gain)
label_make = tk.Label(root, text='Make:', font=('tahoma', 8))
label_make.place(x = 320, y = y_origin + i * gain - 25)

text_color = tk.Text(root, width=15, height=1, font=('tahoma', 8), wrap='none')
text_color.place(x= 580, y= y_origin + i * gain)
label_color = tk.Label(root, text='Color:', font=('tahoma', 8))
label_color.place(x = 580, y = y_origin + i * gain - 25)

text_bodyStyle = tk.Text(root, width=28, height=1, font=('tahoma', 8), wrap='none')
text_bodyStyle.place(x= 720, y= y_origin + i * gain)
label_bodyStyle = tk.Label(root, text='Body Style:', font=('tahoma', 8))
label_bodyStyle.place(x = 720, y = y_origin + i * gain - 25)

text_engine = tk.Text(root, width=35, height=1, font=('tahoma', 8), wrap='none')
text_engine.place(x= 950, y= y_origin + i * gain)
label_engine = tk.Label(root, text='Engine:', font=('tahoma', 8))
label_engine.place(x = 950, y = y_origin + i * gain - 25)

text_VIN = tk.Text(root, width=45, height=1, font=('tahoma', 8), wrap='none')
text_VIN.place(x=1220, y= y_origin + i * gain)
label_VIN = tk.Label(root, text='VIN:', font=('tahoma', 8))
label_VIN.place(x=1220,y= y_origin + i * gain - 25)

i = 1

text_WMI = tk.Text(root, width=20, height=1, font=('tahoma', 8), wrap='none')
text_WMI.place(x= 40, y= y_origin + i * gain)
label_WMI = tk.Label(root, text='World Manufacture Identifier', font=('tahoma', 8))
label_WMI.place(x = 40, y = y_origin + i * gain - 25)

text_VDS = tk.Text(root, width=25, height=1, font=('tahoma', 8), wrap='none')
text_VDS.place(x= 210, y= y_origin + i * gain)
label_VDS = tk.Label(root, text='Vehicle Descriptor Section', font=('tahoma', 8))
label_VDS.place(x = 210, y = y_origin + i * gain - 25)

text_VIS = tk.Text(root, width=25, height=1, font=('tahoma', 8), wrap='none')
text_VIS.place(x= 400, y= y_origin + i * gain)
label_VIS = tk.Label(root, text='Vehicle Identifier Section', font=('tahoma', 8))
label_VIS.place(x = 400, y = y_origin + i * gain - 25)


text_comments = tk.Text(root, width=80, height=1, font=('tahoma', 8), wrap='none')
text_comments.place(x= 850, y= y_origin + i * gain)
label_comments = tk.Label(root, text='Comments', font=('tahoma', 8))
label_comments.place(x = 850, y = y_origin + i * gain - 25)


# /////////// Decode Area /////////////////

i = 3

text_manufacturer=tk.Text(root, width=40,height=1, font=('tahoma', 9), bd=2)
text_manufacturer.place(x=40, y=y_origin + i * gain)
label_manufacturer=tk.Label(root, text='Manufacturer:', font=('tahoma', 9))
label_manufacturer.place(x=40,y=y_origin + i * gain-30)

text_year=tk.Text(root, width=8,height=1, font=('tahoma', 9), bd=2)
text_year.place(x=350, y=y_origin + i * gain)
label_year=tk.Label(root, text='Year:', font=('tahoma', 9))
label_year.place(x=350,y=y_origin + i * gain-30)

text_make_decode=tk.Text(root, width=30,height=1, font=('tahoma', 9), bd=2)
text_make_decode.place(x=470, y=y_origin + i * gain)
label_make=tk.Label(root, text='Make:', font=('tahoma', 9))
label_make.place(x=470,y=y_origin + i * gain-30)

#//////////////////////////////////////////////////////////////////////////////////

text_region=tk.Text(root, width=10,height=1, font=('tahoma', 9), bd=2)
text_region.place(x=720, y=y_origin + i * gain)
label_region=tk.Label(root, text='Region:', font=('tahoma', 9))
label_region.place(x=720,y=y_origin + i * gain-30)

text_country=tk.Text(root, width=14,height=1, font=('tahoma', 9), bd=2)
text_country.place(x=850, y=y_origin + i * gain)
label_country=tk.Label(root, text='Country:', font=('tahoma', 9))
label_country.place(x=850,y=y_origin + i * gain-30)

text_model=tk.Text(root, width=20,height=1, font=('tahoma', 9), bd=2)
text_model.place(x=990, y=y_origin + i * gain)
label_model=tk.Label(root, text='Model:', font=('tahoma', 9))
label_model.place(x=990,y=y_origin + i * gain-30)

# //////////// Buttons /////////////////////////////////////

# New

button_new = ttk.Button(root, text='New...', width=20, command=new)
button_new.place(x=30, y=485)

# Delete
button_delete = ttk.Button(root, text='Delete', width=20, command=delete)
button_delete.place(x=1100, y=485)

# Browse

text_num = tk.Text(root, width=8, height=1, font=('tahoma', 8), wrap='none')
text_num.place(x=1300, y=490)

button_browse=ttk.Button(root, text='Browse', width=15, command=browse)
button_browse.place(x=1380, y=485)

# Update

button_update = ttk.Button(root, text='Update', width=15, command=update)
button_update.place(x=1380, y = y_origin + 1 * gain - 10)

# Decode

button_decode = ttk.Button(root, text='Decode', width=15, command=decode)
button_decode.place(x=655, y = y_origin + 1 * gain - 10)

# About...

button_about = ttk.Button(root, text='About...', width=15, command=about)
button_about.place(x=1190, y=730)

# Exit

button_exit = ttk.Button(root, text='Exit', width=15, command=root.destroy)
button_exit.place(x=1380, y=730)

root.mainloop()

conn.close()