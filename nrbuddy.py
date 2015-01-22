#!/usr/bin/python

#  nrbuddy.py
# wrapper thing so we can wiggle our ibuddy from nodered
# cwhite
# Jan 2015

# Import libs - TODO: check usb and pybuddy is installed!
# TODO: make this handle indefinate colour sets on the head.

import sys
from pybuddylib import *






def badParams():
    print( "Bad parameters - {persist|demo|head|heart|flap|clear|close} {red|green|blue} {timeInSeconds}")


# process the command we got. Set True if we are persistant... this might help prevent unintentionally recursing
def dispatch(isCalledFromPersist, cmd):
    #print( 'Argument List:', str(sys.argv))
    
    if isCalledFromPersist==True:
        # tweak what we have so it 'matches' what things are like if we are called in a non-persistent way
        if len(cmd) < 1:
            cmd = "dummy"

        cmd = "dummy " + cmd
        args = cmd.split()        
        argsLen = len(args) + 1 # keep the dummy one
        cmd = args[1]
    else:
        argsLen = len(sys.argv)
        args = sys.argv


    if cmd == "clear":                 # clear the screen and reset cursor pos
        print( "clear")
        buddy.doReset()
    
    elif cmd == "head":                 # set the head to a colour for some time
        colour = args[2].lower()
        print( "head " + colour)
        if colour=="on" : 
            cad.lcd.blink_on()
        elif param=="off":
            cad.lcd.blink_off()
        else:
            badParams()

    elif cmd == "demo":
        if argsLen > 2 :
            time = args[2].lower()
        else :
            time = 0.5

        doDemo(time)

    elif cmd == "release":
        param = args[2].lower()
        print("release " + param)
        if param=="on" : 
            listenForButtonReleases()
        elif param=="off":
            ignoreButtonReleases()
        else:
            badParams()
      
    elif cmd == "persist":
        if isCalledFromPersist == True :
            print( "blocked persist call" )
        else:    
            print("PIFaceCAD py bridging staying 'resident' ") 
            doPersist()

    elif cmd == "close":
        buddy.doReset()
        if isCalledFromPersist==True:
            print("Thankyou and goodnight")
            sys.exit(0)
        else:
            print("close called outside persist mode")
    else:
        # TODO: Something else if we are persistant?
        badParams()


# rough n ready - while loop which will keep us in flight
# pass data via std io.
def doPersist():
    # hmmm thinking readline might be smarter here...

    while True:
        cmd = input()
        # TODO: validate this 
        print("input: " + cmd)
        dispatch(True, cmd)    


def doDemo(time=0.5):
    time = float(time)
    buddy.doColorName(iBuddyDevice.PURPLE, time)
    buddy.doColorName(iBuddyDevice.BLUE, time)
    buddy.doColorName(iBuddyDevice.LTBLUE, time)
    buddy.doColorName(iBuddyDevice.YELLOW, time)
    buddy.doColorName(iBuddyDevice.GREEN, time)
    buddy.doColorName(iBuddyDevice.RED, time)
    buddy.doColorName(iBuddyDevice.WHITE, time)
    buddy.doFlap()
    sleep(1)
    buddy.doWiggle()
    sleep(1)
    buddy.doHeartbeat()
    sleep(1)
    buddy.doReset()


# Let's do this thing!

if __name__ == '__main__':
    print "going for it"
    try:
      buddy = iBuddyDevice()
    except NoBuddyException, e:
      log.exception("No iBuddy device found!")
      exit(1)

if len(sys.argv) > 1:
    cmd = sys.argv[1].lower()
    
    if len(cmd) > 2:
        dispatch(cmd,cmd)
else:
    badParams()

