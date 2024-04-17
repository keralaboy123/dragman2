### dragman 
this library provides drag detection .it uses pynput library as base library.

only windows is currenlty supported because limitations of pynput library

<pre>
  a software is built using this library is also called dragman.
  it is closed source currently .you can downlaod it from here
  http://dragman.great-site.net
  
</pre>

### how to use

import dragman

class dragdetector(DragEventManager):
    def on_dragEvent(self,x,y):
       print ("rightmouse button of mouse is holding and mouse moved after that ")
