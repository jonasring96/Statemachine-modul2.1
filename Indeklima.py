from gpiozero import LED
from DesignSpark.Pmod.HAT import createPmod
import RPi.GPIO as GPIO
from time import *
import logging
import logging.handlers
import bme680
#opsætning af Knapperne tallene der står i GPIO.setup er GPIO portenes nr
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#Denne linie laver filen Indeklima.log inde i log mappen. og sætter logging level til debug
now = ctime(int(time()))
logging.basicConfig(filename='log/Indeklima.log',level=logging.DEBUG)



sensor = bme680.BME680()

# These oversampling settings can be tweaked to 
# change the balance between accuracy and noise in
# the data.
hum_baseline = 40.0
hum_weighting = 0.25

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

#start_time and curr_time ensure that the 
#burn_in_time (in seconds) is kept track of.

start_time = time()
curr_time = time()
burn_in_time = 50

burn_in_data = []

if __name__ == '__main__':

    #indstiller de forskellige variabler som der skal bruges i programmet nedenunder
    therm = createPmod('TC1','JBA')
    sleep(0.1)
    LEDroed = LED(12)       #simulerer Radiatorer
    LEDgroen = LED(23)      #simulerer vinduerne
    LEDgul = LED(25)        #simulerer overstyring af vinduerne
    state = 4               #Vinduernes State
    rstate = 0              #Radiatorenes State
    timer = 0               #Timer til tvangsstyring af vinduer
    logtimer = 0            #Timer som fortæller hvornår der skal skrives til loggen
    temp = 0                #Timer som fortæller hvornår den skal læse en ny temperatur
    cel = 24                #Variabel hvor temperaturen bliver skrevet til.
    loglock = 1
    baselinetimer =0
    try:
        while True:
            #indfanger dato og tid
            now = ctime(int(time()))
            #tager og slicer timetal ud fra tidligere variabel så den kan bruges andensteds
            hour = int(now[11:13])
            sleep(.5)
            
            temp+= 1
            print(temp)
            
#-----------------------------------------------------------------------------------------
#Funktion som opfanger alle data fra BME680
#-----------------------------------------------------------------------------------------

            if baselinetimer <= 600 and loglock == 1:
                
                if sensor.get_sensor_data() and sensor.data.heat_stable:
                    gas = sensor.data.gas_resistance
                    burn_in_data.append(gas)
                    #print("Gas: {0} Ohms".format(gas))
                    baselinetimer+=1
                                           
             
            if baselinetimer >=600:
                loglock = 0
                logtimer = logtimer + 1
                gas_baseline = sum(burn_in_data[-50:]) / 50.0                   
            
#----------------------------------------------------------
#Funktion til at opdatere temperaturen
#----------------------------------------------------------

            if temp == 20:
                cel = int(therm.readCelcius())
                temp = 0

#------------------------------------------------------------------------------------
#Funktion til at åbne og lukke vinduer.
#    ------------------------------------------------------------------------------------

            


            #vindue åbner Temp
            if cel > 24 and state == 4:
                print("Windows open")
                logging.info("\n"+ str(now)+ "\nWindows open\n")
                LEDgul.off()
                LEDroed.off()
                LEDgroen.on()
                state = 1
                
            #vindue lukker Temp
            elif cel < 23 and state == 1:
                print ("Radiator off and window locked")
                logging.info("\n"+ str(now)+ "\nRadiator off and window locked\n")
                LEDroed.off()
                LEDgroen.off()
                state = 4

            #knap åbner vindue hvis automatik har lukket dem    
            elif GPIO.input(16) ==1 and state == 4:
                print("Button pressed opening windows")
                logging.info("\n"+ str(now)+ "\nButton pressed opening windows\n")
                LEDgul.on()
                LEDgroen.off()
                state = 2
                
            #Vindue åbner efter tvangstyring
            elif GPIO.input(16) ==1 and state == 3:
                print ("Shutting off timer with button")
                logging.info("\n"+ str(now)+ "\nShutting off timer with button\n")
                LEDgul.off()
                state = 4

            #knap åbner vindue hvis automatik har åbnet dem    
            elif GPIO.input(14) == 1 and state == 1:
                print("Button press closes windows")
                logging.info("\n"+ str(now)+ "\nButton press closes windows\n")
                LEDgul.on()
                LEDgroen.off()
                timer = 0
                state = 3
                
            #vindue lukker efter tvangsstyring   
            elif GPIO.input(14) and state == 2:
                print ("shut off timer and closes window after open with button")
                logging.info("\n"+ str(now)+ "\nshuts down timer and closes window after open with button\n")
                LEDgul.off()
                LEDgroen.off()
                timer = 0
                state = 4
                                            
            #Vinduer Lukker og låser for resten af dagen
            elif hour >= 15 and state != 2 and state != 100:
                print("Locking windows")
                logging.info("\n"+ str(now)+ "\nLocking windows\n")
                LEDgroen.off()
                LEDgul.off()
                
                state = 100
                
            #Vinduer er låst op igen    
            elif hour == 7 and state == 100:
                print("Unlocking windows")
                logging.info("\n"+ str(now)+ "\nUnlocking windows\n")
                state = 4
#--------------------------------------------------------------------------
#Timer funktion til når man har trykket på knappen    
#--------------------------------------------------------------------------
                
            if state >= 2 and state <=3:
                timer+= 1
                #print ("timer er "+ str(timer))
                
                if timer == 600:
                    timer = 0
                    state = 4
                    LEDgul.off()

#--------------------------------------------------------
#funktion til at tænde og slukke Radiatorene
#--------------------------------------------------------
            
            #Radiator tænder
            if cel < 17 and state == 4 and rstate != 6 or cel <= 17 and state == 100 and rstate != 6 or cel <=17 and state == 3 and rstate != 6:
                print("Radiator is turning on")
                logging.info("\n"+ str(now)+ "\nRadiator is turning on\n")
                LEDroed.on()
                rstate = 6
                                
            #Radiator slukker    
            if cel > 18 and rstate == 6 or state == 2 and rstate == 6:
                print("Radiator turning off")
                logging.info("\n"+ str(now)+ "\nRadiator is turning off\n")
                LEDroed.off()
                rstate = 0
                
#----------------------------------------------------------
#Funktion til at logge Dataene som der bliver indsamlet
#----------------------------------------------------------
                
            if logtimer == 1200 and loglock == 0:
                              
                if sensor.get_sensor_data() and sensor.data.heat_stable:
                    gas = sensor.data.gas_resistance
                    gas_offset = gas_baseline - gas

                    hum = sensor.data.humidity
                    hum_offset = hum - hum_baseline

                    # Calculate hum_score as the distance from the hum_baseline.
                    
                if hum_offset > 0:
                    hum_score = (100 - hum_baseline - hum_offset) / (100 - hum_baseline) * (hum_weighting * 100)

                else:
                    hum_score = (hum_baseline + hum_offset) / hum_baseline * (hum_weighting * 100)

                # Calculate gas_score as the distance from the gas_baseline.
                
                if gas_offset > 0:
                    gas_score = (gas / gas_baseline) * (100 - (hum_weighting * 100))

                else:   
                    gas_score = 100 - (hum_weighting * 100)

                # Calculate air_quality_score.
                
                air_quality_score = hum_score + gas_score
                
                print(now+"\n")
                print("Grader "+ str(cel)+ u"\u2103")
                print("Gas: {0:.2f} Ohms,\nHumidity: {1:.2f} %RH,\nAir quality: {2:.2f} %\n".format(gas, hum, air_quality_score))
                print("State "+ str(state)+ "\n")
                logging.info("\n"+ str(now)+ "\nGrader : "+ str(cel) + u"\u2103\n"+ "Gas: {0:.2f} Ohms,\nHumidity: {1:.2f} %RH,\nAir quality: {2:.2f} %\n".format(gas, hum, air_quality_score)+ "State : "+ str(state)+ "\n")
                logtimer = 0
                
    except (KeyboardInterrupt, SystemExit):
        raise         
        #report error and proceed
    finally:
        therm.cleanup()
    

    
