# piconator
An app, in mono-C#, for the RPi that presents images onto an RGB LED matrix

**This is still in the "gathering" phase.** <i class="icon-cog"></i> 

##30,000 foot goal
I want to display a series of fun images onto the 32x32 RGB matrix hooked up to the Pi.
I want a web interface to control it with options like:

 - turn on/off
 - speed
 - brightness
 - pause, play, next, and previous controls

Even though the app will land on a Pi 2, I am also developing it to run concurrently
on a Windows PC.  Where the Pi has a dedicated library compiled from C++ and linked/imported
by C#, that needs to happen only on the Pi and the Windows version needs to have a 
proper windows class.  One option I am leaning toward is having the default
state push to the screen, and that works on both Windows and the Pi.  Then,
there will be a command-line parameter to trigger it to push to the matrix.

Scratch that idea.  The windows command line window doesn't allow for enough
custom colors to display the 256 colors in a GIF, much less a PNG or JPG.
Because the original ideas was to give me the ability to develop on Windows
and remotely push to my Pi, I can achieve the same goal by allowing the 
console app to just create a windows form that displays it.  The Pi
should ignore that if the GUI isn't started or at least raise an exception,
which I can capture.  On the Pi, the command line option will route it
to the matrix anyway.


Some links to keep around:

https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi


Adafruit's Git repo for their hat:
https://github.com/adafruit/rpi-rgb-led-matrix

This guy knows what's going on.  Future larger scale projects to be based 
on his hardware and code:

https://github.com/hzeller/rpi-rgb-led-matrix

https://learn.adafruit.com/smartmatrix-animated-gif-player/gifs

http://ezgif.com/

> Written with [StackEdit](https://stackedit.io/).
