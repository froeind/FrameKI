
boxS = [0] * 256
boxPW = [0] * 256

def InitCrypt(passwordKey): #,boxS,boxPW):

    # Ingo Werner 26.01.2024
    # zehn Jahre nach VBA nun in Python
    
    #print(boxS)
    #print(boxPW)

    # den passwort-Schlüssel im Byte-Array abspeichern
    # hat es weniger als 256 Zeichen, wird es wiederholt verwendet
    length = len(passwordKey)
    duplicate = False
    j = 0
    for i in range(0,256):
        j += 1
        if duplicate:
            # aus dem Array selbst kopieren
            boxPW[i] = boxPW[j]
        else:
            # aus dem passwort-Schlüssel kopieren
            boxPW[i] = ord(passwordKey[j-1])
            '''try:
                boxPW[i] = ord(passwordKey[j-1])
            except:
                print("boxPW[i] = ord(passwordKey[j-1])",i)'''
            duplicate = (j == length)
            # falls der passwort-Schlüssel "am Ende" ist, auf Array-Kopieren umschalten
            if duplicate: j = -1
    # S-Box initialisieren...
    for i in range(0,256):
        boxS[i] = i
        '''try:
            boxS[i] = i
        except:
            print("boxS[i] = i",i)'''
    # ...und füllen
    j = 0
    for i in range(0,256):
        j = (j + boxS[i] + boxPW[i]) % 256
        '''try:
            j = (j + boxS[i] + boxPW[i]) % 256
        except:
            print("j = (j + boxS[i] + boxPW[i]) % 256",i)'''
        # Swap der Elemente
        temp = boxS[i]
        '''try:
            temp = boxS[i]
        except:
            print("temp = boxS[i]",i)'''
        boxS[i] = boxS[j]
        boxS[j] = temp
    return

def EnDeCryptDyn(Encrypt,Text,passwordKey):

    # Ingo Werner 26.01.2024
    # zehn Jahre nach VBA nun in Python

    #boxS = [0] * 256
    #boxPW = [0] * 256
    #print(boxS)
    #print(boxPW)

    passwordKeyL = passwordKey
    EnDeCryptDynL = ""
    i = 0
    j = 0
    #print(Text)
    #print(range(1,len(Text)+1))
    for x in range(1,len(Text)+1):
        #print(len(Text))
        #print(x)
        #print(boxS)
        #print(boxPW)
        InitCrypt(passwordKeyL) #,boxS,boxPW)
        #print(boxS)
        #print(boxPW)
        i = (i + 1) % 256
        j = (j + boxS[i]) % 256
        # Swappen
        temp = boxS[i]
        boxS[i] = boxS[j]
        boxS[j] = temp
        # Keybyte erzeugen
        #print("boxS[i]",boxS[i])
        #print("boxS[j]",boxS[j])
        k = boxS[(boxS[i] + boxS[j])% 256]
        #print("k",k)
        # Plaintextbyte XOR Keybyte berechnen
        charS = Text[x-1]
        #print(charS)
        charX = int(ord(charS)) ^ k
        #print(charX)
        scharT = chr(charX)
        #print(scharT)
        EnDeCryptDynL = EnDeCryptDynL + scharT
        #print(EnDeCryptDynL)
        # jetzt wird für den nächsten Durchgang der passwort-Schlüssel geändert und damit auch die Verschlüsselung
        if Encrypt: scharT = charS
        ichar = ord(scharT)
        pos = int(ichar % len(passwordKeyL))
        #print(passwordKeyL)
        #print(pos)
        #print(passwordKeyL[0:pos])
        #print(passwordKeyL[pos+1:len(passwordKeyL)])
        passwordKeyL = passwordKeyL[0:pos] + scharT + passwordKeyL[pos+1:len(passwordKeyL)]
        #print(passwordKeyL)
    return EnDeCryptDynL

def passwordcheck(passwort):

    hatmindestlaenge = False
    hatziffer = False
    hatbuchstabe = False
    hatsonderzeichen = False

    hatmindestlaenge = len(passwort) >= 10

    if hatmindestlaenge:
        pos = 0
        while pos < len(passwort):
            # print(pos)
            char = passwort[pos]
            if char.isnumeric(): hatziffer = True
            elif char.isalpha(): hatbuchstabe = True
            else: hatsonderzeichen = True
            pos = pos + 1
            #if char.isnumeric(): print(char,"Hatziffer")
            #elif char.isalpha(): print(char,"Hatbuchstabe")
            #else: print(char,"Hatsonderzeichen")

    if hatmindestlaenge and hatziffer and hatbuchstabe and hatsonderzeichen: print("Passwort","'"+passwort+"'","ist okay.")
    else: print("Passwort","'"+passwort+"'","ist zu kurz oder nicht sicher genug.")

def verschluesseln(eingabe, schluessel):
    rueckgabe = eingabe[schluessel:][::-1]
    rueckgabe.extend(eingabe[:schluessel])
    return rueckgabe

def entschluesseln(eingabe, schluessel):
    rueckgabe = eingabe[len(eingabe)-schluessel:]
    rueckgabe.extend(eingabe[:len(eingabe)-schluessel:][::-1])
    return rueckgabe

def verschluesseln_mit_schluesselliste(eingabe, schluessel_liste):
  for s in schluessel_liste:
     eingabe = verschluesseln(eingabe, int(s))
  return eingabe

def entschluesseln_mit_schluesselliste(eingabe, schluessel_liste):
  for s in schluessel_liste[::-1]:
     eingabe = entschluesseln(eingabe, int(s))
  return eingabe

def string_verschluesseln(string, schluessel_liste):
    eingabe = list(string)
    return "".join(verschluesseln_mit_schluesselliste(eingabe, schluessel_liste))

def string_entschluesseln(string, schluessel_liste):
    eingabe = list(string)
    return "".join(entschluesseln_mit_schluesselliste(eingabe, schluessel_liste))
