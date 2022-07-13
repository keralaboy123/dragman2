import tkinter as tk
from tkinter import messagebox
import pynput
import io, sys

emu = pynput.mouse.Controller()
class logger(io.StringIO):
    pass


# out,err = sys.stdout  , sys.stderr
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
        print("button move  of  logicanalyser")

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
        self.__doc__ = "handles drag events "
        self.logicalDragAnalyser = logicalDragAnalyser()

    def on_click(self, x, y, button, notreleased):
        print("onclick of drageveMgr")
        if button == pynput.mouse.Button.right:
           if notreleased:
               print("key pressing  drageveMgr")
               self.on_buttondown()
           else:
               print("key released drageveMgr")
               self.on_buttonup()

    def on_buttonup(self):
        print(" on button up   of  DragEventManager ")
        self.logicalDragAnalyser.button_up()

    def on_buttondown(self):
        print(" onButtonDown of DragEventManage  ")
        self.logicalDragAnalyser.button_down()

    def on_move(self, x, y):
        print(" onMOve  of DragEventManage   ")
        self.logicalDragAnalyser.mousemove()
        if self.logicalDragAnalyser.is_draging():
            self.on_dragEvent()


    def stop(self):
        self.listener.stop()

    def run(self):

        self.listener = pynput.mouse.Listener(on_move=self.on_move, on_click=self.on_click)#,suppress=True)
        self.listener.start()

    def on_dragEvent(self):
        print ("on drag event ")



class gui(DragEventManager):
    root = tk.Tk()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        super().run()
        self.root.mainloop()

    def stop(self):
        super().stop()
        self.root.destroy()

    def on_dragEvent(self):
        emu.scroll(0, 0.03)
        self.listener.suppress_event()


if __name__ == "__main__":
    gui().run()
