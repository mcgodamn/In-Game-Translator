import Tkinter as tk
import os
from PIL import ImageGrab,ImageTk,Image

class MyCapture:
    def __init__(self, png):
        self.photo = ImageTk.PhotoImage(png)
        self.X = tk.IntVar(value=0)
        self.Y = tk.IntVar(value=0)
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        self.top = tk.Toplevel(root, width=screenWidth, height=screenHeight)
        self.top.overrideredirect(True)
        self.canvas = tk.Canvas(self.top,bg='white', width=screenWidth, height=screenHeight,highlightthickness=0)
        self.canvas.create_image(screenWidth//2, screenHeight//2, image = self.photo)
        def onLeftButtonDown(event):
            self.X.set(event.x)
            self.Y.set(event.y)
            self.sel = True
        self.canvas.bind('<Button-1>', onLeftButtonDown)
        def onLeftButtonMove(event):
            if not self.sel:
                return
            global lastDraw
            try:
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
            lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='black')
        self.canvas.bind('<B1-Motion>', onLeftButtonMove)
        def onLeftButtonUp(event):
            self.sel = False
            try:
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            pic = ImageGrab.grab((left+1, top+1, right, bottom))
            fileName = 'temp.png'
            pic.save(fileName)
            # self.result = pic
            self.top.destroy()
        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
def Capture():
    root.state('icon')
    im = ImageGrab.grab()
    w = MyCapture(im)
    root.wait_window(w.top)
    root.destroy()
    # return w.result
def ini():
    global root
    root = tk.Tk()
    root.geometry('100x40+400+300')
    root.resizable(False, False)
    root.after_idle(Capture)
    root.mainloop()