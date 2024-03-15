
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import math

import random

class ki1:

    bigdata = None

    subframe = tk.Frame()
    lbl = []
    lbl_text = ["", "Minderleistung in % für kritischen Zustand", "Minderleistung in % für Ausfall", "Mindestabstand zu K", "Mindestabstand zu A"]
    inp = []
    stringvar = []
    btn_analyse = tk.Button()
    btn_plot = tk.Button()
    btn_remove = tk.Button()
    btn_refill = tk.Button()
    liste = tk.Listbox()

    datenliste = []
    datentitel = ("Index", "Wa", "WM", "Wm", "Pa", "PM", "Pm", "K", "A")
    # W = wind_speed / P = active_power
    title_format = "{:<9}{sp}{:^9}{sp}{:^9}{sp}{:^9}{sp}{:^9}{sp}{:^9}{sp}{:^9}{sp}{:^9}{sp}{:^9}"
    data_format = "{:<9}{sp1}{:^9}{sp2}{:^9}{sp3}{:^9}{sp4}{:^9}{sp5}{:^9}{sp6}{:^9}{sp7}{:^9}{sp8}{:^9}"
    datenanalyse1 = []

    default_entry = ["80", "95", "300", "200"]
    ufknn_entrykeys = ("ufknn_entry1", "ufknn_entry2", "ufknn_entry3", "ufknn_entry4")
    ufknn_entry = []

    csv_readandwritten = False
    countdata = 0
    
    linear = lambda self, x: 0 if x<0 else (13-x)/2
    
    def __init__(self, subframe, bigdata):

        self.subframe = subframe
        self.bigdata = bigdata
        self.createFrame()
        self.createplaceformatWidgets()
        
        plt.figure(figsize = (4, 4), dpi = 200)
    
    def readcsvandwritedb(self):
        if not self.csv_readandwritten:
            # csv auslesen
            import csvlogic
            localdatentitel, self.datenliste = csvlogic.readcsv('10m 1.csv')    
            #("wind_speed_avg_", "wind_speed_max_", "wind_speed_min_", "active_power_avg_", "active_power_max_", "active_power_min_") 
            # csv in Datenbank speichern
            csvcount = 0
            for csvdata in self.datenliste:
                csvcount += 1
                setdata = [f"{csvcount:05d}"]
                # die Messdaten
                for index in range(0,6): setdata.append(float(csvdata[index]))
                # die Flags initialisiert
                setdata.append(0)
                setdata.append(0)
                # nicht vergessen, List of tuples ist das Eingabeformat
                setdata = [tuple(setdata)]
                self.bigdata.setvalues("dataki1", setdata)
            # Speicherumfang testen
            if csvcount == self.bigdata.getcount("dataki1"): self.csv_readandwritten = True
            self.countdata = csvcount

    '''
    def readcsvandwritedb_alteversion(self):
        if not self.csv_readandwritten:
            # csv auslesen
            import csvlogic
            turbinentitel, turbinendaten = csvlogic.readcsv('10m 1.csv')     
            # csv in Datenbank speichern
            csvtitle = ("wind_speed_avg_", "wind_speed_max_", "wind_speed_min_", "active_power_avg_", "active_power_max_", "active_power_min_")
            csvcount = 0
            for csvdata in turbinendaten:
                csvcount += 1
                # nicht vergessen, list of tupels ist das eingabeformat
                setdata = []
                for index in range(0,6):
                    setdata.append((csvtitle[index] + f"{csvcount:03d}", float(csvdata[index])))
                self.bigdata.setvalues("dataki1", setdata, "rvalue")
            # Speicherumfang testen
            csvtitle = tuple(element + "%" for element in csvtitle)
            if 6 * csvcount == self.bigdata.getcount("dataki1", csvtitle, True): self.csv_readandwritten = True
    '''

    def readlist(self):
        localliste = [self.datentitel]
        localliste.extend(self.bigdata.getvalues("dataki1"))
        #print(localliste)
        self.countdata = len(localliste) - 1
        return localliste

    def readoutentry(self, index):
        try: count = int(self.inp[index].get())
        except: count = int(self.default_entry[index])
        self.ufknn_entry[index] = count
        return count
    
    def writelist(self):
        # die Daten müssen natürlich auch gesichert werden
        self.bigdata.setvalues("dataki1", self.datenliste[1:])

    def writeconf(self):
        # Auslesen der Werte auch ohne Knöpfchendrücken
        for index in range(0,2): self.readoutentry(index)
        # Schreiben
        res = list(zip(list(self.ufknn_entrykeys), self.ufknn_entry))
        self.bigdata.setvalues("configuration", res, "tvalue")

    def showlist(self, dynlist, nocondition = True):
        self.liste.delete(0, tk.END)
        self.liste.insert(tk.END, self.title_format.format(*dynlist[0], sp=" "))
        count = 0
        for row in dynlist[1:]:
            if nocondition or (row[7] < 0) or (row[8] < 0):                
                count += 1
                self.liste.insert(tk.END, self.data_format.format(*row, sp1=" "*1, sp2=" "*3, sp3=" "*3, sp4=" "*3, sp5=" "*0, sp6=" "*0, sp7=" "*1, sp8=" "*1))
        self.lbl[0].config(text="# " + str(count))

    def createFrame(self):

        row_range = tuple([x for x in range(0,3)])
        col_range = tuple([y for y in range(0,5)])
        self.subframe.columnconfigure(row_range, weight=1)
        self.subframe.rowconfigure(col_range, weight=1)
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
        #self.ufknn_chkbt = self.bigdata.getvalues("configuration", self. ufknn_chkbtkeys, "ivalue")
        #if self. ufknn_chkbt == []: self. ufknn_chkbt = [1, 1, 1, 1]
        self.ufknn_entry = self.bigdata.getvalues("configuration", self.ufknn_entrykeys, "tvalue")
        if self.ufknn_entry == []: self.ufknn_entry = self.default_entry
        # wenn noch was dazukommt, muss ich hier manipulieren = nachladen
        # self.ufknn_entry.append(self.default_entry[4])
        columns = 7
        rows = 4
        # Label
        self.lbl.append(tk.Label(self.subframe, text=self.lbl_text[0], font=("", 20), width=6))
        self.lbl[0].grid(column=0, row=0, rowspan=4)
        for index in range(0,rows):
            self.lbl.append(tk.Label(self.subframe, text=self.lbl_text[index+1], width=35, justify="right"))
            self.lbl[index+1].grid(column=1, row=index, columnspan=columns-2, sticky="e", padx=0)
        # Input
        for index in range(0,rows):
            self.stringvar.append(tk.StringVar(value=self.ufknn_entry[index]))
            self.inp.append(tk.Entry(self.subframe, width=4, textvariable=self.stringvar[index], justify="center"))
            self.inp[index].grid(column=columns-1, row=index, sticky="w", padx=5)
        # Aktionen
        buttons = [("Analyse Data", self.action_analysedata), ("Analyse kNN", self.action_analyseknn), ("Reset", self.action_reset), ("SortReset", self.action_resetsort), ("Plot", self.action_plot), ("Hide", self.action_hide), ("Extend", self.action_extend)]
        rows += 1
        for index, (text, func) in enumerate(buttons):
            button = tk.Button(self.subframe, text=text, command=func)
            button.grid(column=index, row=rows, sticky="w", padx=5, pady=5)
        # Liste
        rows += 1
        self.liste = tk.Listbox(self.subframe, width=70, height=24)
        self.liste.grid(column=0, row=rows, columnspan=columns, sticky="w", padx=5, pady=5)
        # die Datenliste ist nur nach dem einmaligen csv-Import vorhanden
        # also muss sie geladen werden
        self.datenliste = self.readlist()
        self.showlist(self.datenliste)

    def sortlist(self):    
        datenlistesort = []
        datenlistesort.append(self.datenliste[0])
        datenlistesort.extend(sorted(self.datenliste[1:], key=lambda x: x[4], reverse=True))
        return datenlistesort

    def action_analysedata(self):
        # es wird der Mittelwert des Quotienten von durchschnittlicher Action Power und Windstärke genommen
        # wenn ein Windrad den Quotient um den kritischen prozentualen Schwellenwert unterschreitet
        # wird das Windrad als kritisch markiert
        # falls dies für den Ausfall-Schwellenwert gilt, gilt das Windrad als ausgefallen
        # negative Power wird ignoriert
        # und es muss berücksichtigt werden, dass bei schwachen Windstärken verhältnismäßig weniger Strom produziert wird
        # recht maximal ist bei Windstärke 10 ein Quotient von 200, bei Windstärke 5 nur noch 50
        # also baue ich eine lineare Ausgleichsfunktion ein, mehr Mathe stecke ich jetzt nicht rein
        # die die Power künstlich erhöht, y=(13-x)/2
        quotavgcompare = 0
        count = 0
        for row in self.datenliste[1:]:
            if row[4] > 0:
                quotavgcompare += self.linear(row[1])*row[4]/row[1]
                count += 1
        quotavgcompare = quotavgcompare / count
        #print(quotavgcompare)
        notsogood = False
        self.datenanalyse1 = []
        for index1 in range(0, 2):
            schwelle = self.readoutentry(index1)
            grenze = quotavgcompare * (1 - schwelle/100)
            for index2, row in enumerate(self.datenliste[1:]):
                changed = False
                listrow = list(row)
                if listrow[7 + index1] != 0:
                    listrow[7 + index1] = 0
                    changed = True
                if (self.linear(row[1])*row[4]/row[1]) < grenze:
                    listrow[7 + index1] = -1
                    changed = True
                    notsogood = True
                if changed: self.datenliste[index2 + 1] = tuple(listrow)
                if notsogood: self.datenanalyse1.append(tuple(listrow))
        self.showlist(self.sortlist(), False)

    '''
    Definition und Umsetzung stimmten sowieso nicht überein: statt überschreiten hatte ich auch unterschreiten genommen
    def action_analyse_alt(self):
        # es wird der Durchschnitt der minimalen und maximalen Windstärke und Action Power genommen
        # wenn ein Windrad den Durchschnitt für Min um den kritischen prozentualen Schwellenwert unterschreitet
        # oder den Durchschnitt für Max um den prozentualen Schwellenwert überschreitet
        # wird das Windrad als kritisch markiert
        # falls dies für den Ausfall-Schwellenwert gilt, gilt das Windrad als ausgefallen
        sumavgcompare = [0, 0, 0, 0, 0]
        # sumavgcompare[2] ist nur ein Dummy, weil sonst der Summierindex einen Sprung hätte
        for row in self.datenliste[1:]:
            # im ersten Index sind die Feldnamen
            for index in range(0, 5):
                sumavgcompare[index] += row[index + 2]
        for index in range(0, 5):
            sumavgcompare[index] = sumavgcompare[index] / (len(self.datenliste) - 1)
            #print(sumavgcompare[index])
        for index1 in range(0, 2):
            schwelle = self.readoutentry(index1)
            grenze = []
            for index2 in range(0, 5): grenze.append(sumavgcompare[index2] * (1 - schwelle/100))
            for index2, row in enumerate(self.datenliste[1:]):
                #if (index3==16) or (index3==52):
                #    print("Stop")
                #if (index3==17): break
                changed = False
                listrow = list(row)
                if listrow[7 + index1] != 0:
                    listrow[7 + index1] = 0
                    changed = True
                for index3 in range(0, 5):
                    if listrow[index3 + 2] < grenze[index3]:
                        if index3 != 2:
                            listrow[7 + index1] = -1
                            changed = True
                            #print(listrow[0])
                if changed: self.datenliste[index2 + 1] = tuple(listrow)
        self.showlist(self.datenliste, False)
    '''

    def action_analyseknn(self):
        # sofern die erste Analyse stattfand bzw. -1en existieren
        # werden alle 0en jetzt auch noch darauf untersucht, ob sie nicht in der Nähe einer -1 sind
        # wenn ja wird -2 gesetzt
        abstandK = self.readoutentry(2)
        abstandA = self.readoutentry(3)
        for indexo, rowo in enumerate(self.datenliste[1:]):
            for rowi in self.datenanalyse1[1:]:
                # es reicht den äußeren Datensatz nur mit den inneren Flags zu vergleichen
                # ich muss nicht auch den Index vergleichen, bei gleichem Index sind ja die Flags gleich,
                # also wird nichts gemacht
                # und wenn die Flags verschieden sind, dann ist das äußere immer 0 und das innere immer -1 (oder schon -2)
                # ein -2 muss ich auch nicht in der inneren Liste speichern, innere Werte sind immer nur die Basis-Flags -1
                # aber ein -2 darf -1 niucht überschreiben
                changed = False
                listrowo = list(rowo)
                if listrowo[7] != rowi[7]:
                    abstand = math.sqrt((listrowo[1] - rowi[1])**2 + (listrowo[4] - rowi[4])**2)
                    #print(abstand)
                    if (abstand < abstandK) and (listrowo[7] == 0):
                        listrowo[7] = -2
                        changed = True
                    if (abstand < abstandA) and (listrowo[8] == 0):
                        listrowo[8] = -2
                        changed = True
                if changed: self.datenliste[indexo + 1] = tuple(listrowo)
        self.showlist(self.sortlist(), False)

    def resetlist(self):
        for index, row in enumerate(self.datenliste[1:]):
            changed = False
            listrow = list(row)
            if listrow[7] != 0:
                listrow[7] = 0
                changed = True
            if listrow[8] != 0:
                listrow[8] = 0
                changed = True
            if changed: self.datenliste[index + 1] = tuple(listrow)

    def action_reset(self):
        self.resetlist()
        self.showlist(self.datenliste)

    def action_resetsort(self):
        self.resetlist()
        self.showlist(self.sortlist())

    def action_plot(self):
        windp = []
        powerp = []
        windm = []
        powerm = []
        windmm = []
        powermm = []
        for row in self.datenliste[1:]:
            if (row[7] == 0) and (row[8] == 0):
                windp.append(row[1])
                powerp.append(row[4])
            elif (row[7] == -2) or (row[8] == -2):
                windmm.append(row[1])
                powermm.append(row[4])
            else:
                windm.append(row[1])
                powerm.append(row[4])
        plt.scatter(windp, powerp, c="green", s=3)
        plt.scatter(windm, powerm, c="red", s=3)
        plt.scatter(windmm, powermm, c="orange", s=3)
        plt.show()

        '''
        Sie können die Funktion plt.clf() verwenden, um das aktuelle Diagramm zu löschen, ohne das Fenster zu schließen.
        Sie können die Funktion plt.subplot() verwenden, um mehrere Diagramme in einem Fenster anzuzeigen.
        Sie können die Funktion plt.savefig() verwenden, um das Diagramm als Bilddatei zu speichern.
        '''

    def action_hide(self):
        # doch, ich entferne jetzt die -1-Datensätze virtuell
        # wenn ich dann speichere lösche ich diese aber nicht in der Datenbank
        # d.h. die ersten 144 bleiben erhalten, es kommen nur neue dazu
        # dazu muss ich mir die Nummer des letzten Datensatzes merken, habe ich
        # und es kommen ja auch neue demnächst dazu
        for row in self.datenliste[1:]:
            if (row[7] < 0) or (row[8] < 0): self.datenliste.remove(row)
        self.action_reset()

    def action_extend(self):
        for n in range(10, random.randint(50, 300)):
            wind = []
            power = []
            for m in range(0, random.randint(1, 5)):
                wind.append(round(random.randint(10, 35) / 10, 1))
                # / muss es sein bei self.linear nicht *, muss nur hoffen, dass dies nie 0 wird, also Windstärke >= 13
                power.append(round(random.randint(180, 220) * wind[-1] / self.linear(wind[-1]), 1))
            for m in range(0, random.randint(1, 25)):
                wind.append(round(random.randint(30, 85) / 10, 1))
                power.append(round(random.randint(180, 220) * wind[-1] / self.linear(wind[-1]), 1))
            for m in range(0, random.randint(1, 125)):
                wind.append(round(random.randint(80, 119) / 10, 1))
                power.append(round(random.randint(180, 220) * wind[-1] / self.linear(wind[-1]), 1))
            self.countdata += 1
            # hier muss ich das Maxinmum halbieren (damit die Werte ähnlich der Basisdaten sind)
            # und das MIninmum verdoppeln (ausgleichende Gerechtigkeit)
            new = (f"{self.countdata:05d}", round(sum(wind)/len(wind), 1), max(wind), min(wind), round(sum(power)/len(power), 1), max(power)/2, min(power)*2, 0, 0)
            #print(new)
            self.datenliste.append(new)
        self.action_reset()

        #uftk.showdestroyMessage("Der Klick hat was getan!")