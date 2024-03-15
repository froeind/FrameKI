
import tkinter as tk
#import universalframe_tkinter as uftk
from tkinter import ttk

import random

class password:

    bigdata = None

    subframe = tk.Frame()
    intvar = []
    chkbt = []
    lbl = []
    stringvar = []
    inp = []
    btn = tk.Button()
    res = []

    default = ["5", "5", "5", "5"]

    ufpw_chkbtkeys = ("ufpw_chkbt1", "ufpw_chkbt2", "ufpw_chkbt3", "ufpw_chkbt4")
    ufpw_chkbt = []
    ufpw_entrykeys = ("ufpw_entry1", "ufpw_entry2", "ufpw_entry3", "ufpw_entry4")
    ufpw_entry = []
    passwort = ["", "", "", ""]

    def __init__(self, subframe, bigdata):

        self.subframe = subframe
        self.bigdata = bigdata
        self.createFrame()
        self.createplaceformatWidgets()
        
    def readoutentrycheck(self, index):
         # Input
        try: count = int(self.inp[index].get())
        except: count = int(self.default[index])
        self.ufpw_entry[index] = count
        # Checkbox
        self.ufpw_chkbt[index] = self.intvar[index].get()
        # Output nur von der Anzahl
        return count
    
    def writeconf(self):
        # Auslesen der Werte auch ohne Knöpfchendrücken
        for index in range(0,4): self.readoutentrycheck(index)
        # Schreiben
        res = list(zip(list(self.ufpw_entrykeys), self.ufpw_entry))
        self.bigdata.setvalues("configuration", res, "tvalue")
        res = list(zip(list(self.ufpw_chkbtkeys), self.ufpw_chkbt))
        self.bigdata.setvalues("configuration", res, "ivalue")

    def createFrame(self):

        x0_range = tuple([x for x in range(0,4)])
        y0_range = tuple([y for y in range(0,10)])
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
        self.ufpw_chkbt = self.bigdata.getvalues("configuration", self.ufpw_chkbtkeys, "ivalue")
        if self.ufpw_chkbt == []: self.ufpw_chkbt = [1, 1, 1, 1]
        self.ufpw_entry = self.bigdata.getvalues("configuration", self.ufpw_entrykeys, "tvalue")
        if self.ufpw_entry == []: self.ufpw_entry = self.default
        # Checkboxen Upper Lower Number XChar
        col = 0
        for index in range(0,4):
            # wenn ich darauf zugreifen will, muss ich zuerst das Objekt in einer Liste sichern
            # und nicht die Methode sozusagen
            # und das gewöhne ich mir generell an
            # also nicht so:
            #self.chkbt.append(tk.Checkbutton(self.subframe, width=1).grid(column=col, row=index, sticky="e", padx=0))
            self.intvar.append(tk.IntVar(value=self.ufpw_chkbt[index]))
            self.chkbt.append(ttk.Checkbutton(self.subframe, variable=self.intvar[index], width=1))
            self.chkbt[index].grid(column=col, row=index, sticky="e", padx=0)
        # Label Upper Lower Number XChar
        col += 1
        lbl_text = ["Großbuchstaben A - Z", "Kleinbuchstaben a - z", "Zahlen 0 - 9", "Sonderzeichen"]
        for index in range(0,4):
            self.lbl.append(tk.Label(self.subframe, text=lbl_text[index], width=17))
            self.lbl[index].grid(column=col, row=index, sticky="w", padx=0)
        # Input Upper Lower Number XChar
        col += 1
        for index in range(0,4):
            self.stringvar.append(tk.StringVar(value=self.ufpw_entry[index]))
            self.inp.append(tk.Entry(self.subframe, width=4, textvariable=self.stringvar[index], justify="center"))
            self.inp[index].grid(column=col, row=index, sticky="w", padx=5)
        # Hinweistext
        col += 1
        tk_string = tk.StringVar(value="mal")
        for index in range(0,4):
            tk.Entry(self.subframe, state="disabled", textvariable=tk_string, width=6).grid(column=col, row=index, sticky="w", padx=1)
        # Aktion 1
        self.btn = tk.Button(self.subframe, text="Passworte generieren", command=self.action1).grid(column=0, row=4, columnspan=2, sticky="w", padx=5, pady=5)
        # Aktion 2
        self.btn = tk.Button(self.subframe, text="Passworte kopieren", command=self.action2).grid(column=2, row=4, columnspan=2, sticky="w", padx=0, pady=5)
        # Anzeigen
        lbl_text = ["Kombiniertes Passwort", "Geschütteltes Passwort", "Verschlüsseltes Passwort", "Kryptifiziertes Passwort"]
        for index in range(5,9):
            tk_string = tk.StringVar(value=lbl_text[index-5])
            self.res.append(tk.Entry(self.subframe, state="disabled", textvariable=tk_string, width=40))
            self.res[index-5].grid(column=0, row=index, columnspan=4, sticky="w", padx=5, pady=5)

    def action1(self):
        self.passwort[0] = ""
        # Auslesen der Eingabefelder und Zusammenstellung der ersten Zeichenkombinationen
        for index in range(0,4):
            anzahl = self.readoutentrycheck(index)
            if self.intvar[index].get() == 1:
                for zindex in range(0,anzahl):
                    if index == 0:
                        # A-Z
                        self.passwort[0] += chr(random.randint(65,90))
                    elif index == 1:
                        # a-z
                        self.passwort[0] += chr(random.randint(97,122))
                    elif index == 2:
                        # Ziffern 0-9
                        self.passwort[0] += chr(random.randint(48,57))
                    else:
                        # Interpunktion
                        zeichen = chr(random.randint(33,47)) + chr(random.randint(58,64)) + chr(random.randint(91,96)) + chr(random.randint(123,126))
                        self.passwort[0] += zeichen[random.randint(0,3)]

        if self.passwort[0] != "":

            #tk_string = tk.StringVar(value=self.res[0].get() + ": " + passwort)
            tk_string = tk.StringVar(value="Passwort: " + self.passwort[0])
            self.res[0].config(textvariable=tk_string)

            self.passwort[1] = list(self.passwort[0])
            # danke Internet für string.pop(), dachte (noch) nicht an Slicing
            # passwort = ''.join([passwort[i] for i in range(len(passwort)) if i != 2]) 
            for index in range(0,len(self.passwort[0])):
                # aber im Grunde mache ich das auch, nur etwas umständlicher
                char = self.passwort[1].pop(random.randint(1,len(self.passwort[0]))-1)
                self.passwort[1].append(char)
            self.passwort[1] = "".join(self.passwort[1])
            tk_string = tk.StringVar(value="Geschüttelt: " + self.passwort[1])
            self.res[1].config(textvariable=tk_string)

            from passwordlogic import string_verschluesseln
            self.passwort[2] = string_verschluesseln(self.passwort[0], [1,2,3,4,5,6])
            #tk_string = tk.StringVar(value=self.res[1].get() + ": " + self.passwort[2])
            tk_string = tk.StringVar(value="Verschlüsselt: " + self.passwort[2])
            self.res[2].config(textvariable=tk_string)

            from passwordlogic import EnDeCryptDyn
            self.passwort[3] = EnDeCryptDyn(True,self.passwort[0],"jgkbsxtwd")
            #tk_string = tk.StringVar(value=self.res[1].get() + ": " + self.passwort[3])
            tk_string = tk.StringVar(value="Kryptifiziert: " + self.passwort[3])
            self.res[3].config(textvariable=tk_string)

    def action2(self):

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

            
        #uftk.showdestroyMessage("Der Klick hat was getan!")