import tkinter as tk
from tkinter import messagebox
import pynput
import io, sys

class logger(io.StringIO):
    pass


mouseControll = pynput.mouse.Controller()
#log = sys.stdout = sys.stderror= logger()

class STATE:
        def __init__(self):
            self.is_RightButton_Still_holding = False
            self.is_mouseMoved_after_mouse_down = False

        def _is_RightButton_Still_holding(self):
            if self.is_RightButton_Still_holding:
                return True

        def _is_mouseMoved_after_mouse_down(self):
            if self.is_mouseMoved_after_mouse_down:
                return True

        def set_mouseMoved_after_mouse_down(self,value):
            self.is_mouseMoved_after_mouse_down = value

        def set_RightButton_Still_holding(self,value):
            self.is_RightButton_Still_holding=value

class logicalDragAnalyser():
    " if mouse moving while button pressed its dragging.. "
    def __init__(self):
        self.STATE = STATE()

    def is_mousemoved(self):
        if self.STATE._is_mouseMoved_after_mouse_down():
            self.STATE.set_mouseMoved_after_mouse_down(False)
            return True

    def on_mousemove(self):
        print(self.on_mousemove.__qualname__)
        self.STATE.set_mouseMoved_after_mouse_down(True)


    def on_button_down(self):
        print(self.on_button_down.__qualname__)
        self.STATE.set_RightButton_Still_holding(True)


    def on_button_up(self):
        print(self.on_button_up.__qualname__)
        self.STATE.set_RightButton_Still_holding( False )

    def is_draging(self):
        "this is the api should be used by other subclasses"
        if self.is_mousemoved():
            if self.STATE._is_RightButton_Still_holding():
                return True


class DragEventManager:
    def __init__(self):
        "creates drag detection and provideds callback for drag event"
        self.logicalDragAnalyser = logicalDragAnalyser()
        self.listener = pynput.mouse.Listener(on_move=self.on_move, on_click=self.on_click)  # ,suppress=True)

    def on_click(self, x, y, button, notreleased):
        print(self.on_click.__qualname__)
        if button == pynput.mouse.Button.right:
           if notreleased:
               print("      right button not released")
               self.on_buttondown(x, y, button, notreleased)
           else:
               print("      right button released")
               self.on_buttonup(x, y, button, notreleased)

    def on_buttonup(self,x, y, button, notreleased):
        print(self.on_buttonup.__qualname__)
        self.logicalDragAnalyser.on_button_up()

    def on_buttondown(self,x, y, button, notreleased):
        print(self.on_buttondown.__qualname__)
        self.logicalDragAnalyser.on_button_down()

    def on_move(self, x, y):
        print(self.on_move.__qualname__)
        self.logicalDragAnalyser.on_mousemove()
        print("moved from "+str(mouseControll.position) )
        print("moved " +str(x)+str(y))
        if self.logicalDragAnalyser.is_draging():
            self.on_dragEvent(x,y)

    def stop(self):
        self.listener.stop()

    def run(self):
        self.listener.start()

    def on_dragEvent(self,x,y):
        print(self.on_dragEvent.__qualname__)


class maper(DragEventManager):
    def __init__(self,scrollstep=0.03):
        super().__init__()
        self.is_draged_beforeButtonUp =False
        self.scrollstep = scrollstep

    def _is_draged_beforeButtonUp(self):
        print(self._is_draged_beforeButtonUp.__qualname__)
        if self.is_draged_beforeButtonUp:
            self.is_draged_beforeButtonUp =False
            return True

    def on_buttondown(self,x,y,button,released):
        print(self.on_buttondown.__qualname__)    
        super().on_buttondown(x,y,button,released)
        self.listener.suppress_event()

    def on_buttonup(self,x, y, button, notreleased):
        print(self.on_buttonup.__qualname__)
        super().on_buttonup(x, y, button, notreleased)
        if self._is_draged_beforeButtonUp():
            print("   draged before right button up")
            self.listener.suppress_event()
        else:
            print("   no drag just before right button up")
    def on_dragEvent(self,x,y):
        print(self.on_dragEvent.__qualname__)
        self.is_draged_beforeButtonUp = True

class manager(maper):
    def on_dragEvent(self,x,y):
        print(self.on_dragEvent.__qualname__)
        super().on_dragEvent(x,y)
        mouseControll.scroll(0, self.scrollstep)



class gui(manager):
    "running and stoping mape manger graphicaly"
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

