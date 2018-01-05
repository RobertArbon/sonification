import numpy as np
import time
import argparse
import multiprocessing as mp
import queue as q
import threading as th
import tkinter as tk
import tkinter.constants as tkConst

from pythonosc import udp_client

res_1 = np.load("/users/ajj/google drive/data/hmm_trajectories/traj-0.npy")
res_2 = np.load("/users/ajj/google drive/data/hmm_trajectories/entropy-0.npy")

class BackgroundThread(th.Thread):
  def __init__(self):
    th.Thread.__init__(self)
    self.queue = q.Queue()
    self.target = self.run_thread; self.start()
  def run_thread(self):
    while True:
        message = self.queue.get(block=True)
        print (message)

def some_other_process(background_thread):
  background_thread.queue.put("")

class gui_tk(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.initialise()

    def initialise(self):
        self.grid()
        self.geometry('500x555')

        self.entryVariable = tk.StringVar()

        self.entry = tk.Entry(self, textvariable=self.entryVariable)
        self.entry.grid(column=0, row=0, sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)

        self.labelVariable = tk.StringVar()
        self.entryVariable.set(u"Enter text here.")

        button = tk.Button(self, text="Exit", command=self.OnButtonClick)
        button.grid(column=1, row=0)

        label = tk.Label(self, textvariable=self.labelVariable, anchor="w", fg="white", bg="blue")
        label.grid(column=0, row=1, columnspan=2, sticky='EW')

        scale = tk.Scale(self ,from_=1.0, to=0.0, command=self.OnSliderChange, resolution=0.01)
        scale.grid(column = 0, columnspan=10, row = 3)
        scale.set(0.5)

        self.labelVariable.set(u"Hello !")
        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, False)

        self.update()
        self.geometry(self.geometry())

        self.entry.focus_set()
        self.entry.selection_range(0, tk.END)

    def OnButtonClick(self):
        self.labelVariable.set(self.entryVariable.get()+" (You clicked the button)")
        self.entry.focus_set()
        self.entry.selection_range(0, tk.END)


    def OnPressEnter(self, event):
        self.labelVariable.set(self.entryVariable.get()+" (You pressed enter)")
        self.entry.focus_set()
        self.entry.selection_range(0, tk.END)

    def OnSliderChange(self, event):
        print("You moved the sider")

def gui_loop():
    app = gui_tk(None)
    app.title('my application')
    gui_tk.mainloop(app)
    return

def oscar():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="")
    parser.add_argument("--port", type=int, default=5005, help="")
    args = parser.parse_args()
    client = udp_client.SimpleUDPClient(args.ip, args.port)
    for i, x in enumerate(res_1):
        #print(x)
        client.send_message("/state1", float(x[0]))
        client.send_message("/state2", float(x[1]))
        client.send_message("/state3", float(x[2]))
        client.send_message("/entropy", float(res_2[i]))
        time.sleep(.05)
    return

if __name__ == "__main__":
    #threads = []
    #t1 = th.Thread(target=oscar())
    #threads.append(t1)
    #th._start_new_thread(gui_loop())
    th._start_new_thread(oscar())
    #t1.start()
    #t0 = th.Thread(target=gui_loop())
    #threads.append(t0)
    #t0.start()