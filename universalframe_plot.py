
import tkinter as tk
#import universalframe_tkinter as uftk
from tkinter import ttk

import matplotlib.pyplot as plt
import math

class plotter:

    bigdata = None

    subframe = tk.Frame()
    
    default = ["x*math.sin(x)", "2*x", "math.sqrt(x)", "math.log(x)", "x*math.sin(x)*math.cos(x)"]

    stringvar = []
    inp = []
    btn = tk.Button()
    res = []

    #ufpw_chkbtkeys = ("ufpw_chkbt1", "ufpw_chkbt2", "ufpw_chkbt3", "ufpw_chkbt4")
    #ufpw_chkbt = []
    ufpl_entrykeys = ("ufpl_entry1", "ufpl_entry2", "ufpl_entry3", "ufpl_entry4", "ufpl_entry5")
    ufpl_entry = []
    
    def __init__(self, subframe, bigdata):

        self.subframe = subframe
        self.bigdata = bigdata
        self.createFrame()
        self.createplaceformatWidgets()
        
        plt.figure(figsize = (4, 4), dpi = 200)

    def readoutentryfunction(self, index):
        value = self.default[index]
        try: value = self.inp[index].get()
        except: pass
        if "x" not in value: value = self.default[index]
        self.ufpl_entry[index] = value
        return value
    
    def writeconf(self):
        # Auslesen der Werte auch ohne Knöpfchendrücken
        for index in range(0,5): self.readoutentryfunction(index)
        # Schreiben
        res = list(zip(list(self.ufpl_entrykeys), self.ufpl_entry))
        self.bigdata.setvalues("configuration", res, "tvalue")

    def createFrame(self):

        x0_range = tuple([x for x in range(0,1)])
        y0_range = tuple([y for y in range(0,7)])
        self.subframe.columnconfigure(x0_range, weight=1)
        self.subframe.rowconfigure(y0_range, weight=1)
        # das ist notwendig
        self.subframe.grid(column=0, row=0)
        # das macht nichts, zumindest merke ich nichts
        #self.subframe.update()

    def createplaceformatWidgets(self):        
        '''
        column: Spalte, in der das Widget platziert wird (beginnend bei 0)
        row: Zeile, in der das Widget platziert wird (beginnend bei 0)
        columnspan: Anzahl der Spalten, die das Widget überspannen soll
        rowspan: Anzahl der Zeilen, die das Widget überspannen soll
        sticky: Ausrichtung des Widgets in der Zelle (z. B. N, S, E, W, NE, SE, SW, NW)
        padx: Abstand zwischen dem Widget und den Rändern der Zelle (horizontal)
        pady: Abstand zwischen dem Widget und den Rändern der Zelle (vertikal)
        '''
        # Parameter auslesen
        #self.ufpl_chkbt = self.bigdata.getvalues(self.ufpw_chkbtkeys, "ivalue")
        #if self.ufpw_chkbt == []: self.ufpw_chkbt = [1, 1, 1, 1]
        self.ufpl_entry = self.bigdata.getvalues("configuration", self.ufpl_entrykeys, "tvalue")
        if self.ufpl_entry == []: self.ufpl_entry = self.default
        col = 0
        col = -1
        col += 1
        for index in range(0,5):
            self.stringvar.append(tk.StringVar(value=self.ufpl_entry[index]))
            self.inp.append(tk.Entry(self.subframe, width=40, textvariable=self.stringvar[index], justify="center"))
            self.inp[index].grid(column=col, row=index, sticky="w", padx=5)
        # Aktion 1
        self.btn = tk.Button(self.subframe, text="Plotten", command=self.action1).grid(column=0, row=6, sticky="w", padx=5, pady=5)

    def action1(self):

        xwerte = [x / 10.0 for x in range(5, 150)]
        for index in range(0,5):
            funzion = self.readoutentryfunction(index)
            plt.plot(xwerte, [eval(funzion) for x in xwerte], label=funzion.replace("math.",""))
        plt.legend()
        plt.show()

        '''
        Sie können die Funktion plt.clf() verwenden, um das aktuelle Diagramm zu löschen, ohne das Fenster zu schließen.
        Sie können die Funktion plt.subplot() verwenden, um mehrere Diagramme in einem Fenster anzuzeigen.
        Sie können die Funktion plt.savefig() verwenden, um das Diagramm als Bilddatei zu speichern.
        '''

    def action2(self):
        pass
        '''
        if self.passwort[0] != "":

            passwort = ""
            for index in range(0,4):
                # damit muss ich die Verpackung entfernen
                # aber das ist einfach, alles nach ': '
                # so bräuchte ich keine globalen Passwort-Variablen, wenn es strright von Haus aus gäbe
                # aber es gäbe instr
                # aber das wäre auch ein Gefummel, also doch globale Variable
                passwort += self.passwort[index] + "\n"

            # pip install pyperclip
            import pyperclip
            pyperclip.copy(passwort)
            #passwort = pyperclip.paste()
        '''

            
        #uftk.showdestroyMessage("Der Klick hat was getan!")