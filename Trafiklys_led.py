from random import random
from gpiozero import LED
from time import sleep

greenwe=LED(26)
gulwe=LED(19)
redwe=LED(13)
redns=LED(6)
gulns=LED(5)
greenns=LED(0)
     
def state0():
    print ("Grøn! Kør")
    greenwe.on()
    redns.on()
    sleep(5.5)
    greenwe.off()
    redns.off()
    return state1

def state1():
    print ("Gul! stop")
    gulwe.on()
    gulns.on()
    sleep(6.5)
    gulwe.off()
    gulns.off()
    return state2

def state2():
    print ("Rød! stop")
    redwe.on()
    greenns.on()
    sleep(6.5)
    redwe.off()
    greenns.off()
    return state3

def state3():
    print("Gul! stop")
    gulwe.on()
    gulns.on()
    sleep(2)
    gulwe.off()
    gulns.off()
    return state0
    


state=state0    # initial state
while state: state=state()  # launch state machine
print ("Done with states")
