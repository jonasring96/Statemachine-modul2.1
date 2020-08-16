import thingspeak
import time
import random


channel_id =1049013  # PUT CHANNEL ID HERE
key = 'B530FR63JBR4S3MN' # PUT YOUR WRITE KEY HERE
read_key = 'BQE5HYPZ0YTXJULT' # PUT YOUR READ KEY HERE


def measure(channel):
    try:

        humidity=random.randrange(30,100)
        temperature=random.randrange(-30,100)
        print("Fugt:",humidity)
        print("Temp:",temperature)
        response = channel.update({'field3': temperature, 'field2': humidity})
        #time.sleep(1)
        #response = channel.update({'field2': humidity})
        read = channel.get({})
        print(read)

    except:
        print("connection failed")


if __name__ == "__main__":
    channel = thingspeak.Channel(id=channel_id, api_key=key)
    while True:
        measure(channel)
        # free account has an api limit of 15sec
        time.sleep(15)

