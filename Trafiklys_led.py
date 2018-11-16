from random import random
from gpiozero import LED
from time import sleep

led1=LED(12)
led2=LED(13)
led3=LED(23)

def state0():
    print ("Grøn! Kør")
    led1.on()
    sleep(5.5)
    led1.off()
    return state1

def state1():
    print ("Gul! stop")
    led2.on()
    sleep(1.5)
    led2.off()
    return state2

def state2():
    print ("Rød! stop")
    led3.on()
    sleep(5.5)
    led3.off()
    return state0


state=state0    # initial state
while state: state=state()  # launch state machine
print ("Done with states")
