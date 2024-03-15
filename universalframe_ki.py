
import tkinter as tk
from tkinter import ttk

import matplotlib
import matplotlib.pyplot as plt
import math

import random

# pip install scikit-learn
# PyCharm hat gemeckert über "pip install sklearn" und wollte "pip install scikit-learn", aber wie in VSCode wird mit der "falschen/alten" Syntax doch richtig importiert
from sklearn import svm

class ki:

    # 08.03.2024
    # jetzt werden aus Minus-Werten 2er-Potenzen
    #   weil ich dies für Decision Trees besser gebrauchen kann, ich möchte ermitteln, wo überall ein Windrad auffällig wird
    #   jeder Test ist eine Potenz höher und bestehende Informationen werden so nicht mehr überschrieben
    # und die Buttons werden jetzt auf gleiche Breite gebracht

    bigdata = None

    '''
    test0="test0"
    _test1="test1"
    __test2="test2"
    '''

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

    blnHasPoints = [False, False, False, False, False]
    
    linear = lambda self, x: 0 if x<0 else (13-x)/2
    
    K2 = [0, 0, 0]
    K4 = [0, 0, 0, 0, 0]
    xnv = 0
    ynv = 0
    bias = 0

    blnIstDrin = lambda self, x, y: x & y == y

    fig = None

    def __init__(self, subframe, bigdata):

        self.subframe = subframe
        self.bigdata = bigdata
        self.createFrame()
        self.createplaceformatWidgets()
        self.readconf()
        # das sollte initial passieren, damit ich ein Plotfenster habe
        #self.plotinwindow()
    
    def __str__(self):
        return f"xnv = {self.xnv}\nynv = {self.ynv}\nbias = {self.bias}\nK2 = {self.K2}\nK4 = {self.K4}\n"

    def plotinwindow(self):

        # geht so nicht, aber wie?
        rootplot = tk.Tk()
        tkBreite = 800; tkHoehe = 600; tkX = 2000; tkY = 100
        rootplot.geometry("%dx%d+%d+%d"%(tkBreite, tkHoehe, tkX, tkY))
        self.fig, ax = plt.subplots()
        canvas = tk.Canvas(rootplot, width=tkBreite, height=tkHoehe)
        canvas.pack(side="top", fill="both", expand=True)
        #canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.fig.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        #plt.figure(figsize = (4, 4), dpi = 200)   

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
        self.bigdata.setvalues("configuration", "ufsvm_xnv", "rvalue")
        self.bigdata.setvalues("configuration", "ufsvm_ynv", "rvalue")
        self.bigdata.setvalues("configuration", "ufsvm_bias", "rvalue")

    def readconf(self):
        self.xnv = self.bigdata.getvalues("configuration", "ufsvm_xnv", "rvalue")
        if self.xnv == []: self.xnv = 0
        self.ynv = self.bigdata.getvalues("configuration", "ufsvm_ynv", "rvalue")
        if self.ynv == []: self.ynv = 1
        self.bias = self.bigdata.getvalues("configuration", "ufsvm_bias", "rvalue")
        if self.bias == []: self.bias = 0
        
    def showlist(self, dynlist, typeof = 0):
        self.liste.delete(0, tk.END)
        self.liste.insert(tk.END, self.title_format.format(*dynlist[0], sp=" "))
        count = 0
        for row in dynlist[1:]:
            if (typeof == 0) or self.blnIstDrin(row[7], typeof) or self.blnIstDrin(row[8], typeof):
                count += 1
                self.liste.insert(tk.END, self.data_format.format(*row, sp1=" "*1, sp2=" "*3, sp3=" "*3, sp4=" "*3, sp5=" "*0, sp6=" "*0, sp7=" "*1, sp8=" "*1))
        self.lbl[0].config(text="# " + str(count))

    def createFrame(self):

        row_range = tuple([x for x in range(0,4)])
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
        self.lbl[0].grid(column=0, row=0, rowspan=4, columnspan=2, sticky="w", padx=5)
        for index in range(0,rows):
            self.lbl.append(tk.Label(self.subframe, text=self.lbl_text[index+1], width=35, justify="right"))
            self.lbl[index+1].grid(column=1, row=index, columnspan=columns-3, sticky="e", padx=0)
        # Input
        for index in range(0,rows):
            self.stringvar.append(tk.StringVar(value=self.ufknn_entry[index]))
            self.inp.append(tk.Entry(self.subframe, width=4, textvariable=self.stringvar[index], justify="center"))
            self.inp[index].grid(column=columns-1, row=index, sticky="w", padx=5)
        # Aktionen
        intWidthButton = 12
        buttons = [("Analyse Data", self.action_analysedata), ("Analyse kNN", self.action_analyseknn), ("Analyse SVM", self.action_analysesvm), ("Analyse Poly2", self.action_analysepoly2), ("Analyse Poly4", self.action_analysepoly4), ("Reset", self.action_reset), ("PowerSort", self.action_powersort), ("WindSort", self.action_windsort), ("Plot", self.action_plot_deactivated), ("Extend", self.action_extend)]
        #, ("Hide", self.action_hide)
        rows += 1
        indexstep = 0
        for index, (text, func) in enumerate(buttons):
            button = tk.Button(self.subframe, text=text, command=func, width=intWidthButton)
            button.grid(column=index+indexstep, row=rows, sticky="w", padx=2, pady=5)
            if index == 4:
                rows += 1
                indexstep = -(index+1)
        # Liste
        rows += 1
        self.liste = tk.Listbox(self.subframe, width=70, height=24)
        self.liste.grid(column=0, row=rows, columnspan=columns, sticky="w", padx=5, pady=5)
        # die Datenliste ist nur nach dem einmaligen csv-Import vorhanden
        # also muss sie geladen werden
        self.datenliste = self.readlist()
        self.showlist(self.datenliste)

    def sortlist(self, ascendingwind = False):    
        datenlistesort = []
        datenlistesort.append(self.datenliste[0])
        if ascendingwind: datenlistesort.extend(sorted(self.datenliste[1:], key=lambda x: x[1]))
        else: datenlistesort.extend(sorted(self.datenliste[1:], key=lambda x: x[4], reverse=True))
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
                if row[7 + index1] != 0:
                    listrow[7 + index1] = 0
                    changed = True
                if (self.linear(row[1])*row[4]/row[1]) < grenze:
                    listrow[7 + index1] = 1
                    changed = True
                    notsogood = True
                if changed: self.datenliste[index2 + 1] = tuple(listrow)
                if notsogood: self.datenanalyse1.append(tuple(listrow))
        self.blnHasPoints = [True, False, False, False, False]
        self.showlist(self.sortlist(), 1)
        self.action_plot()

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
        self.showlist(self.datenliste, 1)
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
                # aber ein -2 darf -1 nicht überschreiben
                changed = False
                listrowo = list(rowo)
                if listrowo[7] != rowi[7]:
                    abstand = math.sqrt((listrowo[1] - rowi[1])**2 + (listrowo[4] - rowi[4])**2)
                    #print(abstand)
                    if (abstand < abstandK):
                        if not self.blnIstDrin(rowo[7], 2):
                            listrowo[7] += 2
                            changed = True
                    if (abstand < abstandA):
                        if not self.blnIstDrin(rowo[8], 2):
                            listrowo[8] += 2
                            changed = True
                if changed: self.datenliste[indexo + 1] = tuple(listrowo)
        self.blnHasPoints[1] = True
        self.showlist(self.sortlist(), 2)
        self.action_plot()

    def action_analysesvm(self):
        # jetzt wird anhand der -1 und -2 eine neue Analyse nach der/einer "Support Vector Machine"-Methode oder ähnlichen durchgeführt
        # es wird eine Trenngerade ermittelt, und alle Punkte auf der einen Seite sind okay und auf der anderen -3 sozusagen
        # ist ja nur eine kleine Spielerei, um mich vertraut zu machen

        # Vorverarbeitung der Daten
        X = []
        y = []
        for row in self.datenliste[1:]:
            X.append((row[1], row[4]))
            y.append((row[7] > 0) or (row[8] > 0))
        #print(X)
        #print(y)

        # Auswahl des linearen Kernels
        kernel = 'linear'
        
        # Training des SVM-Modells
        clf = svm.SVC(kernel=kernel, C=1.0)
        clf.fit(X, y)

        # Bestimmen der Parameter der Hyperebene
        nv = clf.coef_ # Normalenvektor
        self.bias = float(clf.intercept_) # Bias, Abweichung von Nullpunkt, y-Achsenabschnitt = bias / y(nv)
        # jetzt endlich merke ich, dass die ganze Zeit das sowas <class 'numpy.ndarray'> war
        #print(nv)
        #print(bias)
        # Geradengleichung ist dann xnv * x1 + ynv * x2 + bias = 0
        #print(str(nv[0]))
        nvs = str(nv[0])[1:-2]
        #print(nvs)
        # nvs.split(" ") geht nicht sofort, weil beide Vorzeichen Blank oder - sein können
        # und damit muss ich alle Leerstring entfernen
        nvs = nvs.split(" ")
        #print(nvs)
        nvs = [elem for elem in nvs if elem != ""]
        #print(nvs)
        self.xnv = float(nvs[0])
        self.ynv = float(nvs[1])
        #print(self.xnv)
        #print(self.ynv)

        # Daten entsprechend anpassen
        for index, row in enumerate(self.datenliste[1:]):
            changed = False
            listrow = list(row)
            bereich = self.xnv * row[1] + self.ynv * row[4] + self.bias
            #print(bereich)
            if bereich > 0:
                if not self.blnIstDrin(row[7], 4):
                    listrow[7] += 4
                    changed = True
                if not self.blnIstDrin(row[8], 4):
                    listrow[8] += 4
                    changed = True
            if changed: self.datenliste[index + 1] = tuple(listrow)
        self.blnHasPoints[2] = True
        self.showlist(self.sortlist(), 4)
        self.action_plot()

    def action_analysepoly(self, intDim):
        # jetzt wird anhand der -1, -2 und -3 eine neue Analyse über Parabelgrenze
        # und alle Punkte auf der einen Seite sind okay und auf der anderen -4 sozusagen
        # aus einer kleinen Spielerei wird jetzt was komplexeres
        # mit SVM bin ich jetzt nicht glücklich geworden, ich mache einen eigenen Ansatz
        # (aber das hat sicher irgendjemand schon besser gemacht oder es steckt in irgendeiner Bibliothek
        # vielleicht sogar in SVM, aber ich habe auch "Dank" Gemini ehem. Bard nichts gefunden)

        # Vorverarbeitung der Daten
        # Suche für jedes x d.h. Wind-Wert das y-Pärchen (also Power) mit kleinstem Abstand von blau zu rot, d.h. 0 zu -n
        # da ich ohne Blick auf Plot nicht wissen kann, wie blau und rot im Bezug zur Kurve liegen
        # merke ich mir zwei Pärchen: rot über blau und blau über rot
        # Auswerten werde ich dann die Farbkombination, die am häufigsten ist, und wünsche mir Eindeutigkeit
        # und ich merke mir nicht die beiden y-Werte sondern den Mittelwert, weil der ja im Idealfall auf der Kurve liegt
        # ich muss aber berücksichtigen, dass es zu einem x nicht unbedingt verschiedene Punkte gibt
        # d.h. ich muss eigentlich ein x-Intervall berücksichtigen
        # und das mache ich so, das setzt aber voraus, das meine Daten in x "dicht genug" sind,
        # dass ich, wenn es zu einem x nur ein y gibt, weitermache mit dem nächsten x
        # wenn es einen Statuswechsel gibt für x (oder x und Nachfolger), dann setze ich den Mittelwert oder beide
        # wenn nicht, setze ich None
        # außerdem zähle ich hier auch gleich die Häufigkeiten
        # ich muss natürlich zuerst die p- bzw. n-y-Werte mir merken
        # weil ich kann ja nicht direkt paarweise Minima und Maxima und damit die Abstände bestimmen

        def FillNP(py, ny, row, initial = False):
            x = row[1]
            if initial:
                #print(id(py))
                # ich darf nicht mit set() das Set zurücksetzen, das erzeugt nur ein lokales Set
                py.clear()
                #print(id(py))
                ny.clear()
            if (row[7] > 0) or (row[8] > 0): ny.add(row[4])
            else: py.add(row[4])
            #return x, py, ny
            return x

        def AnalysePN(x, X, py, ny, pnM, npM, pnA, npA, countp, countn):
            # in py und ny sind die blauen und roten y-Koordinaten zu x (und eventuellen Vorwerten)
            # sofern welche gefunden wurden
            # in der Regel müssen beide Listen nichtleer sein, aber in der letzten Sammlung kann das schon sein
            # also muss ich daraufhin überprüfen
            # ist eine der Liste leer, dann steige ich aus
            # ansonsten merke ich mir x in X
            # und bestimme den minimalen Abstand von allen blauen y zu den roten y
            # wo einmal blau-y >= rot-y und umgekehrt blau-y <= rot-y gilt

            # ein Startabstand, der garantiert unterboten wird
            distp = 100000
            distn = 100000
            
            midp = 0
            midn = 0

            ofp = False
            ofn = False

            #print("py", py)
            #print("ny", ny)

            if (len(py) != 0) and (len(ny) != 0):
                for yp in py:
                    for yn in ny:
                        dist = abs(yp - yn)
                        if yp > yn:
                            if dist < distp:
                                distp = dist
                                ofp = True
                                midp = (yp + yn) / 2
                        else:
                            if dist < distn:
                                distn = dist
                                ofn = True
                                midn = (yp + yn) / 2
                X.append(x)
                if ofp:
                    pnM.append(midp)
                    pnA.append(distp)
                    countp += 1
                else:
                    pnM.append(None)
                    pnA.append(None)
                if ofn:
                    npM.append(midn)
                    npA.append(distn)
                    countn += 1
                else:
                    npM.append(None)
                    npA.append(None)

            #print("X", X)
            #print("pnM", pnM)
            #print("npM", npM)
            #return countp, countn, X, pnM, npM
            return countp, countn

        def SearchParabola(distM, intDim, lstKombi, intOptIndexe, lstOptIndexe, blnProduktiv = False):

            xvalue = []
            yvalue = []
            for index in lstKombi:
                xvalue.append(X[distM[index][1]])
                yvalue.append(valueM[distM[index][1]])

            from numpy import array
            from numpy import linalg

            A = []
            b = []
            for index in range(0,intDim+1):
                if intDim == 2:
                    A.append([xvalue[index]**2, xvalue[index], 1])
                else:
                    A.append([xvalue[index]**4, xvalue[index]**3, xvalue[index]**2, xvalue[index], 1])
                b.append(yvalue[index])
            if intDim == 2:
                self.K2 = linalg.solve(array(A), array(b))
                #print(self.K2)
                parabel = lambda x: self.K2[0] * x**2 + self.K2[1] * x + self.K2[2]
            else:
                self.K4 = linalg.solve(array(A), array(b))
                #print(self.K4)
                self.K4 = list(map(float, self.K4))
                parabel = lambda x: self.K4[0] * x**4 + self.K4[1] * x**3 + self.K4[2] * x**2 + self.K4[3] * x + self.K4[4]

            '''
            for index in range(0,3):
                print(parabel(xvalue[index]))
                print(parabel(xvalue[index]) - yvalue[index])
            '''

            # Daten entsprechend anpassen
            intCount = 0
            intSetValue = 8 if intDim == 2 else 16
            for index, row in enumerate(self.datenliste[1:]):
                changed = False
                listrow = list(row)
                if row[4] < parabel(row[1]):
                    if blnProduktiv:
                        if not self.blnIstDrin(row[7], intSetValue):
                            listrow[7] += intSetValue
                            changed = True
                        if not self.blnIstDrin(row[8], intSetValue):
                            listrow[8] += intSetValue
                            changed = True
                    else:
                        if row[7] > 0 or row[8] > 0: intCount += 1
                elif not blnProduktiv:
                    if row[7] == 0 and row[8] == 0: intCount += 1
                if blnProduktiv:
                    if changed: self.datenliste[index + 1] = tuple(listrow)

            if intCount > intOptIndexe: return intCount, lstKombi
            else: return intOptIndexe, lstOptIndexe

        # die x-Koordinate
        X = []
        # die Mittelwerte
        pnM = []
        npM = []
        # die Abstände, d.h. wie nahe sind die Mittelwerte an den Koordinaten
        pnA = []
        npA = []
        # welche Farben gibt es
        py = set()
        ny = set()
        # wie oft ist blau größer als rot oder umgekehrt
        countp = 0
        countn = 0
        
        x = -1
        for row in self.sortlist(True)[1:]:
            if (x == row[1]) or (len(py) == 0) or (len(ny) == 0):
                # entweder: wir sind beim ersten oder noch gleichen x
                # oder zuvor gab es noch keine zwei Farben bei einem Vorgänger-x
                # also das allererste x oder weiteres zum x oder nächstes x betrachten
                #print("Test if")
                # generell wird hier gesammelt
                #x, py, ny = FillNP(py, ny, row)
                x = FillNP(py, ny, row)
                #print(py)
                #print(ny)
            else:
                # oder: wir sind beim nächsten x
                # und wir haben schon etwas in beiden Farben bei allen dazu notwendigen vorigen x 
                # dann werden die vorhandenen Daten zuerst ausgewertet
                # und dann die neue Sammlung initiiert
                #print("Test else")
                # Auswertung
                #print("oha")
                #countp, countn, X, pnM, npM = AnalysePN(x, X, py, ny, pnM, npM, countp, countn)
                if x != -1: countp, countn = AnalysePN(x, X, py, ny, pnM, npM, pnA, npA, countp, countn)
                # nächste Sammlung
                #x, py, ny = FillNP(py, ny, row, True)
                x = FillNP(py, ny, row, True)
                if x > 0:
                    pass

        #countp, countn, X, pnM , npM = AnalysePN(x, X, py, ny, pnM, npM, countp, countn)
        countp, countn = AnalysePN(x, X, py, ny, pnM, npM, pnA, npA, countp, countn)

        #print(self.sortlist(True)[1:])

        if False:
            print("Länge X", len(X))
            print("X", X)
            print("Länge pnM", len(pnM))
            print("# p", countp)
            print("Mittelwert pn", pnM)
            print("Abstand pn", pnA)
            print("Länge npM", len(npM))
            print("# n", countn)
            print("Mittelwert np", npM)
            print("Abstand np", npA)

        # jetzt wähle ich die Liste von Grenzpunkten, für die es mehr Werte gibt
        # (hier ist es pnM (countp >= countn), aber ich muss dies abfragen, dann kann ich den Algorithmus weiterverwenden)
        # und nehme die 3, wo die Abstände am geringsten sind zur Interpolation einer Parabel
        if countp >= countn: distM = pnA; valueM = pnM
        else: distM = npA; valueM = npM
        # dann entferne ich noch die None, damit ich auch beliebige Werte wählen könnte
        # brauche ich nämlich wenn ich die "vorne und hinten" brauche
        # dann muss ich aber auch die entsprechenden Werte in X und valueM entfernen
        #print("X", X); print("distM", distM); print("valueM", valueM)
        X = [x for x, dist in zip(X, distM) if dist is not None]
        distM = [x for x in distM if x is not None]
        valueM = [x for x in valueM if x is not None]
        #print("X", X); print("distM", distM); print("valueM", valueM)
        # wenn es nicht drei bzw. fünf Punkte gibt, kann ich auch nichts weiteranalysieren
        if len(distM) >= intDim+1:
            distM = list(zip(distM, range(0, len(distM))))
            #print("distM zipped", distM)
            #print(type(distM))
            #print(len(distM))
            #print()
            #print(distM[0])
            #print(distM[0][0])
            distM = sorted(distM, key=lambda x: x[0])
            #print("distM sorted", distM)
            '''
            xvalue = []
            yvalue = []
            # das sind testweise die drei größten Abstände 
            #for index in range(-intDim-1, 0):
            # und das sind die drei kleinsten Abstände
            # bei denen bleibe ich auch
            # aber damit das Schaubild nicht zu sehr verzerrt wird, begrenze ich die Parabeln
            for index in range(0,intDim+1):
                #print(distM[index])
                #print(distM[index][1])
                xvalue.append(X[distM[index][1]])
                yvalue.append(valueM[distM[index][1]])
            #print(xvalue)
            #print(yvalue)
            '''
            # mein neuer Ansatz geht alle möglichen Indexkombinationen durch
            # und es wird die Kombination genommen, die die wenigsten neuen Minuswerte erzeugt
            # weil diese trennt gefühlt am besten
            # dazu bräuchte ich natürlich keine Sortierung, aber das lasse ich oben alles so
            # und nein, sie trennt nicht am besten
            # ich muss die Parabel wählen, die bestmöglich vorhandene Plus als Plus und Minus als Minus wiedererkennt

            from itertools import combinations

            #intCount = 0
            lstIndizes = [x for x in range(len(distM))]
            intOptIndexe = 0
            lstOptIndexe = []
            for lstKombi in combinations(lstIndizes, intDim+1):
                #print(lstKombi)
                intOptIndexe, lstOptIndexe = SearchParabola(distM, intDim, lstKombi, intOptIndexe, lstOptIndexe)
                #intCount += 1
            #print(len(lstIndizes))
            #print(intDim+1)
            #print(intCount)

            SearchParabola(distM, intDim, lstOptIndexe, intOptIndexe, lstOptIndexe, True)

            if intDim == 2: self.blnHasPoints[3] = True
            else: self.blnHasPoints[4] = True
            self.showlist(self.sortlist(), 8 if intDim == 2 else 16)
            self.action_plot()

    def action_analysepoly2(self):
        self.action_analysepoly(2)

    def action_analysepoly4(self):
        self.action_analysepoly(4)

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
        self.blnHasPoints = [False, False, False, False, False]

    def action_reset(self):
        self.resetlist()
        self.showlist(self.datenliste)

    def action_powersort(self):
        #self.resetlist()
        self.showlist(self.sortlist())

    def action_windsort(self):
        #self.resetlist()
        self.showlist(self.sortlist(True))

    def action_plot_deactivated(self):
        pass

    def action_plot(self):

        plt.clf()

        windp = []
        powerp = []
        windm = []
        powerm = []
        windknn = []
        powerknn = []
        windsvm = []
        powersvm = []
        windpbl2 = []
        powerpbl2 = []
        windpbl4 = []
        powerpbl4 = []
        xachse = []

        for row in self.datenliste[1:]:
            xachse.append(row[1])
            if (row[7] == 0) and (row[8] == 0):
                windp.append(row[1])
                powerp.append(row[4])
            elif self.blnIstDrin(row[7], 1) or self.blnIstDrin(row[8], 1):
                windm.append(row[1])
                powerm.append(row[4])
            elif self.blnIstDrin(row[7], 2) or self.blnIstDrin(row[8], 2):
                windknn.append(row[1])
                powerknn.append(row[4])
            elif self.blnIstDrin(row[7], 4) or self.blnIstDrin(row[8], 4):
                windsvm.append(row[1])
                powersvm.append(row[4])
            elif self.blnIstDrin(row[7], 8) or self.blnIstDrin(row[8], 8):
                windpbl2.append(row[1])
                powerpbl2.append(row[4])
            else:
                windpbl4.append(row[1])
                powerpbl4.append(row[4])

        plt.scatter(windp, powerp, c="green", s=1)
        plt.scatter(windm, powerm, c="red", s=1)
        plt.scatter(windknn, powerknn, c="orange", s=1)
        plt.scatter(windsvm, powersvm, c="blue", s=1)
        plt.scatter(windpbl2, powerpbl2, c="magenta", s=1)
        plt.scatter(windpbl4, powerpbl4, c="violet", s=1)

        fltMax = max(max(powerp), max(powerm)) * 1.1

        # ... und jetzt auch die Gerade
        gerade = lambda x: max(-50, min(fltMax, (-self.bias - self.xnv * x) / self.ynv))
        # damit das Schaubild nicht zu sehr verzerrt wird, begrenze ich die Parabeln ...
        # fltMin setze ich jetzt hier explizit mit -50 statt 0 wie zuvor
        parabel2 = lambda x: max(-50, min(fltMax, self.K2[0] * x**2 + self.K2[1] * x + self.K2[2]))
        parabel4 = lambda x: max(-50, min(fltMax, self.K4[0] * x**4 + self.K4[1] * x**3 + self.K4[2] * x**2 + self.K4[3] * x + self.K4[4]))
        #print(type(self.K4[0]))

        xachse.sort()
        if self.blnHasPoints[2]: plt.plot(xachse, [gerade(x) for x in xachse], color="blue", linewidth=0.2, linestyle="solid")
        if self.blnHasPoints[3]: plt.plot(xachse, [parabel2(x) for x in xachse], color="magenta", linewidth=0.2, linestyle="solid")
        if self.blnHasPoints[4]: plt.plot(xachse, [parabel4(x) for x in xachse], color="violet", linewidth=0.2, linestyle="solid")

        #plt.Line2D(xachse, [gerade(x) for x in xachse], color="blue", linewidth=4, linestyle="solid")
        plt.show()

        '''

        Sie können die Funktion plt.clf() verwenden, um das aktuelle Diagramm zu löschen, ohne das Fenster zu schließen.
        Sie können die Funktion plt.subplot() verwenden, um mehrere Diagramme in einem Fenster anzuzeigen.
        Sie können die Funktion plt.savefig() verwenden, um das Diagramm als Bilddatei zu speichern.

        Rot:
        Crimson
        Firebrick
        Maroon
        Red
        Ruby
        Tomato

        Rottöne mit Blauanteil:
        Magenta
        Pink
        Rose

        Rottöne mit Gelbanteil:
        Coral
        Salmon
        Rust

        Dunkle Rottöne:
        Brown
        Burgundy
        Chocolate

        Helle Rottöne:
        Peach
        Pink
        Strawberry
        
        color="#FF0000"

        '''

    def action_hide(self):
        # doch, ich entferne jetzt die -1-Datensätze virtuell
        # wenn ich dann speichere lösche ich diese aber nicht in der Datenbank
        # d.h. die ersten 144 bleiben erhalten, es kommen nur neue dazu
        # dazu muss ich mir die Nummer des letzten Datensatzes merken, habe ich
        # und es kommen ja auch neue demnächst dazu
        for row in self.datenliste[1:]:
            if (row[7] > 0) or (row[8] > 0): self.datenliste.remove(row)
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