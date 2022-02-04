# Button(master, text='Get Value', command=show_values).pack()
# Power(W)= Current (I)* Voltage(V) (Displayed on graph)
# Electric Bill(Wh/kWh)=(W/T(hour))* Energy price per kWh (user input)

import tkinter as tk

import matplotlib
import pandas as pd
import numpy as np
import matplotlib.animation as animation

matplotlib.use("TkAgg")
from tkinter import *
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import *

fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)


def write(curr, volt, pow):
    data = pd.read_csv('data.csv')
    dt = get_datetime()
    lastlog = data['LOGID'].iloc[-1]
    lastlog = lastlog + 1
    datarow = {'LOGID': lastlog, 'DATETIME': dt, 'CURRENT': curr, 'VOLTAGE': volt, 'POWER': pow}
    data = data.append(datarow, ignore_index=True)
    data.to_csv('data.csv', index=False)


def get_datetime():
    dt = datetime.now()
    dtnow = dt.strftime("%m/%d/%Y %H:%M:%S")
    return dtnow


def get_values():
    currvalue = float(w1.get())
    voltvalue = float(w2.get())
    powvalue = currvalue * voltvalue

    write(currvalue, voltvalue, powvalue)

    print("")
    print("Current =", currvalue, "A")
    print("Voltage =", voltvalue, "V")
    print("Power =", powvalue, "W")
    print("")

    app.after(1000, get_values)


def animate(i):
    data = pd.read_csv('data.csv')

    sel = radiosel()

    x = []
    y = []
    xt = []
    yt = []

    if var.get() == 1:
        for index, row in data.iterrows():
            xt.append(row['LOGID'])
            yt.append(row['POWER'])
            if index in xt[-720::60]:
                x.append(row['LOGID'])
                y.append(row['POWER'])
    elif var.get() == 2:
        for index, row in data.iterrows():
            xt.append(row['LOGID'])
            yt.append(row['POWER'])
            if index in xt[-18000::300]:
                x.append(row['LOGID'])
                y.append(row['POWER'])
    elif var.get() == 3:
        for index, row in data.iterrows():
            xt.append(row['LOGID'])
            yt.append(row['POWER'])
            if index in xt[-2592000::3600]:
                x.append(row['LOGID'])
                y.append(row['POWER'])
    ax.clear()
    ax.plot(x, y, color="magenta")
    ax.plot(x, y, 'ro', markersize=2)
    ax.set_xlabel("Latest Log ID (" + str(sel[var.get()]) + ")")
    ax.set_ylabel("Power (Watts)")


def radiosel():
    sel = {1: '1 minute', 2: '5 minutes', 3: '1 hour'}
    selection = "You selected to display per " + str(sel[var.get()])
    label.config(text=selection)
    return sel


def electricbill():
    x = entry.get()
    data = pd.read_csv('data1.csv')
    lastlog = data['LOGID'].iloc[-1]
    hours = int(lastlog/3600)
    index = hours*3600
    rawpower = np.array(data['POWER'])
    totalpower = np.sum(rawpower[:index])
    if hours==0:
        billprint = "Data is less than an hour."
    else:
        elecbill = float(x) * (totalpower/hours)
        billprint = "Electric bill for 30 days is:" + str(elecbill)
    eleclabel = tk.Label(app, text=billprint)
    canvas2.create_window(50, 80, window=eleclabel)


app = Tk()
val = IntVar
var = IntVar()

canvas = FigureCanvasTkAgg(fig, master=app)
canvas.draw()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=0)

ani = animation.FuncAnimation(fig, animate, interval=1000)

w1 = Scale(app, variable=val, from_=0.001, to=1.000, resolution=0.000, tickinterval=0.099, orient=HORIZONTAL,
           length=700, width=20, borderwidth=10, background="light blue", foreground="black",
           troughcolor="light gray", label="Current (A)")

w2 = Scale(app, variable=val, from_=0, to=260, tickinterval=10, orient=HORIZONTAL,
           length=700, width=20, borderwidth=10, background="light blue", foreground="black",
           troughcolor="light gray", label="Voltage (V)")

canvas1 = tk.Canvas(app, width=550, height=70)
canvas1.pack()

label = Label(app)
canvas1.create_window(275, 20, window=label)

r1 = Radiobutton(app, text="Display per 1 Minute", variable=var, value=1, command=radiosel)
var.set(1)
canvas1.create_window(0, 50, window=r1)
r2 = Radiobutton(app, text="Display per 5 Minutes", variable=var, value=2, command=radiosel)
canvas1.create_window(150, 50, window=r2)
r3 = Radiobutton(app, text="Display per 1 Hours", variable=var, value=3, command=radiosel)
canvas1.create_window(300, 50, window=r3)

canvas2 = tk.Canvas(app, width=100, height=100)
canvas2.pack()

entry = tk.Entry(app)
canvas2.create_window(50, 20, window=entry)

button = tk.Button(text='Enter Energy Price per kWh (PHP)', command=electricbill)
canvas2.create_window(50, 50, window=button)

w1.set(0)
w1.pack()

w2.set(0)
w2.pack()

get_values()

app.mainloop()
