from tkinter import *
import asyncio
import time


async def asyncTest():
    time.sleep(5)


def update():
    print(canvas.master.winfo_width())
    tk.after(10, update)


if __name__ == "__main__":
    tk = Tk()
    canvas = Canvas(tk, width=400, height=400)
    canvas.master.maxsize(1500, 1500)
    canvas.master.minsize(200, 200)
    canvas.pack()
    # canvas.create_rectangle(10, 10, 50, 50)  # （10,10）为正方形右上角坐标，（50,50）为正方形右下角坐标
    tk.after(0, update)
    tk.mainloop()
