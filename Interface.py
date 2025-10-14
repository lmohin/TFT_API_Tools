from tkinter import ttk
import tkinter as tk
import tkinter.simpledialog as tkd
import asyncio
from Snapshot import *
from Scores_Loic import *
from Tacticianinit import *
import tk_async_execute as tae



def Snapshot_call():
    # Call async function
    tae.async_execute(Snapshot(), wait=True, visible=True, pop_up=True, callback=None, master=root)

    # Close application
def Score_call():
    tae.async_execute(Scores(), wait=True, visible=True, pop_up=True, callback=None, master=root)

def TacticianInit_call():
    page = tkd.askinteger("test","Quelle page?")
    if page == 1:
        plage = "D:F"
        page = "Liste Joueurs"
        case = "B"
    else:
        plage = "E:G"
        page = "Phase 1 : Rondes Suisse (Samedi)"
        case = "D"
    tae.async_execute(updateTactician(plage, page, case), wait=True, visible=True, pop_up=True, callback=None, master=root)


if __name__ == "__main__":
    root = tk.Tk()
    bnt = ttk.Button(root, text="Snapshot", command=Snapshot_call, width=20)
    bnt.pack()
    bnt = ttk.Button(root, text="Scores", command=Score_call, width=20)
    bnt.pack()
    bnt = ttk.Button(root, text="TacticianInit", command=TacticianInit_call, width=20)
    bnt.pack()

    tae.start()  # Starts the asyncio event loop in a different thread.
    root.mainloop()  # Main Tkinter loop
    tae.stop()  # Stops the event loop and closes it.