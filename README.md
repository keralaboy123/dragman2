 ### dragman 
this library provides drag detection .it uses pynput library as base library.

only windows is currenlty supported because limitations of pynput library

<pre>
  a software  built using this library is also called dragman.
  it is closed source currently .i will make it opensource if got financial support.
  you can downlaod free trial  from here <a href="http://dragman.great-site.net">http://dragman.great-site.net
</pre>

### how to use
<pre>

import dragman

class dragdetector ( dragman.DragEventManager ):
       def on_dragEvent ( self,x,y ):
               print ("right button of mouse is holding and mouse moved after that ")

if __name__ == "__main__":
      detector = dragdetector()
      detector.start()
</pre>
