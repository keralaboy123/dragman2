import tkinter as tk
from tkinter import messagebox
import pynput
import io, sys,mouse

mouseControll = pynput.mouse.Controller()

class logger(io.StringIO):
    pass

#log = sys.stdout = sys.stderror= logger()

class STATE:
        def __init__(self):
            self.isRightholding = False
            self.mouseMoved = False


class logicalDragAnalyser():
    " if mouse moving while button pressed its dragging.. "
    def __init__(self):
        self.STATE = STATE()

    def is_mousemoved(self):
        if self.STATE.mouseMoved:
            self.STATE.mouseMoved = False
            return True

    def mousemove(self):
        self.STATE.mouseMoved = True
        # print("button move  of  logicanalyser")

    def button_down(self):
        self.STATE.isRightholding = True
        print("button down  of  logicanalyser")

    def button_up(self):
        self.STATE.isRightholding = False
        print("button up  of  logicanalyser")

    def is_draging(self):
        if self.is_mousemoved():
            if self.STATE.isRightholding:
                return True



class DragEventManager(object):
    def __init__(self):
        "handles drag events "
        self.logicalDragAnalyser = logicalDragAnalyser()

    def on_click(self, x, y, button, notreleased):
        print("onclick of drageveMgr")
        if button == pynput.mouse.Button.right:
           if notreleased:
               print("key pressing  drageveMgr")
               self.on_buttondown(x, y, button, notreleased)
           else:
               print("key release drageveMgr")
               self.on_buttonup(x, y, button, notreleased)

    def on_buttonup(self,x, y, button, notreleased):
        print(" on button up   of  DragEventManager ")
        self.logicalDragAnalyser.button_up()

    def on_buttondown(self,x, y, button, notreleased):
        print(" onButtonDown of DragEventManage  ")
        self.logicalDragAnalyser.button_down()

    def on_move(self, x, y):
        #print(" onMOve  of DragEventManage   ")
        self.logicalDragAnalyser.mousemove()
        if self.logicalDragAnalyser.is_draging():
            self.on_dragEvent(x,y)

    def stop(self):
        self.listener.stop()

    def run(self):
        self.listener = pynput.mouse.Listener(on_move=self.on_move, on_click=self.on_click)#,suppress=True)
        self.listener.start()

    def on_dragEvent(self,x,y):
        print ("on drag event ")


class maper(DragEventManager):
    def __init__(self,scrollstep=0.03):
        super().__init__()
        self.is_draged_beforeButtonDown =False
        self.scrollstep = scrollstep

    def is_draged_justbefore(self):
        if self.is_draged_beforeButtonDown:
            print ("drag happened just before buttin up")
            self.is_draged_beforeButtonDown =False
            return True

    def on_buttondown(self,x,y,button,released):
        super().on_buttondown(x,y,button,released)
        self.listener.suppress_event()

    def on_buttonup(self,x, y, button, notreleased):
        super().on_buttonup(x, y, button, notreleased)
        print(" checking is drag happened")

        if self.is_draged_justbefore():
            print ("# generating right button click")
            mouseControll.click(button,1)
            self.listener.suppress_event()
        else:
            print("drag not happened just before right buttin up")


    def on_dragEvent(self,x,y):
        self.is_draged_beforeButtonDown = True
        print ("drag happened ")
        mouseControll.scroll(0, self.scrollstep)
        self.listener.suppress_event()


class gui(maper):
    root = tk.Tk()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        super().run()
        self.root.mainloop()

    def stop(self):
        super().stop()
        self.root.destroy()


if __name__ == "__main__":
    gui().run()
