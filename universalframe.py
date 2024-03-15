
import sqlite3

import universalframe_database as ufdb
bigdata = ufdb.confanddata()
bigdata.opendb()

import tkinter as tk
#from tkinter import ttk
# nur um zu testen, dass das jetzt richtig hochgeschoben wird
i = 5

# laut Bard=Gemini soll das das "Kein-Button-gedrückt"-Problem lösen - JA
def on_closing():
    # das muss natürlich hier rein, solange es tkinter noch gibt
    frame_password.writeconf()
    frame_plot.writeconf()
    frame_ki.resetlist()
    frame_ki.writelist()
    frame_ki.writeconf()
    #print(frame_ki)
    # und das ist 'natürlich' drin
    root.destroy()
    root.quit()
# laut Bard=Gemini soll das das "Kein-Button-gedrückt"-Problem lösen - JA

root = tk.Tk()
# laut Bard=Gemini soll das das "Kein-Button-gedrückt"-Problem lösen - JA
root.protocol("WM_DELETE_WINDOW", on_closing)
# laut Bard=Gemini soll das das "Kein-Button-gedrückt"-Problem lösen - JA

# Main window
root.title("Universal-Rahmen")
#tkBreite = 800; tkHoehe = 600; tkX = 3000; tkY = 100
tkBreite = 800; tkHoehe = 600; tkX = 1000; tkY = 100
root.geometry("%dx%d+%d+%d"%(tkBreite, tkHoehe, tkX, tkY))
root.minsize(450, 300)
root.maxsize(1000, 800)

x_range = tuple([x for x in range(0,3)])
#print(x_range)
y_range = tuple([y for y in range(0,2)])
#print(y_range)
root.columnconfigure(x_range, weight=1)
root.rowconfigure(y_range, weight=1)

framebox = []
for y in y_range:
    framerow = []
    for x in x_range:
        framerow.append(tk.Frame(root, borderwidth=3, relief=tk.GROOVE))
    framebox.append(framerow)

x, y = 0, 0
import universalframe_password as ufpw
frame_password = ufpw.password(framebox[x][y], bigdata)
framebox[x][y].grid(row=x, column=y, padx=20, pady=20, sticky="nw")

x, y = 1, 0
import universalframe_plot as ufpl
frame_plot = ufpl.plotter(framebox[x][y], bigdata)
framebox[x][y].grid(row=x, column=y, padx=20, pady=20, sticky="nw")

x, y = 0, 1
import universalframe_ki as ufki
frame_ki = ufki.ki(framebox[x][y], bigdata)
framebox[x][y].grid(row=x, column=y, padx=20, pady=20, sticky="nw", rowspan=2)

# Verwaltungssachen
# erfordern vielleicht mehrere Starts
# am Ende sollte aber wieder alles auf False gestellt sein
if False:
    tables = ["dataki1"]
    bigdata.droptables(tables)    
if False: frame_ki1.readcsvandwritedb()

# grid auch mit place kombinieren

'''
print(ufki.ki.test0)
print(ufki.ki._test1)
ufki.ki._test1 = "nix"
print(ufki.ki._test1)
#print(ufki.ki.__test2)
'''

root.mainloop()

bigdata.closedb()

# configuration auch über config.json
