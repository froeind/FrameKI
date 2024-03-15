
import tkinter as tk
# muss explizit importiert werden, sonst geht es nicht
import tkinter.messagebox as tkm

def showdestroyMessage(message, type='info', timeout=2500):
    # https://stackoverflow.com/questions/34643309/is-there-a-way-to-destroy-the-tkinter-messagebox-without-clicking-ok
    # aber ich nutze es doch nicht, weil es nicht ganz richtig - im Moment - funktioniert
    # es macht nämlich ein kleines Extrafenster unaufgefordert auf
    root = tk.Tk()
    root.withdraw()
    try:
        root.after(timeout, root.destroy)
        if type == 'info':
            tkm.showinfo('Info', message, master=root)
        elif type == 'warning':
            tkm.showwarning('Warning', message, master=root)
        elif type == 'error':
            tkm.showerror('Error', message, master=root)
    except:
        pass