import time
import requests
import json
import RPi.GPIO as io
io.setmode(io.BCM)

pir_pin = 18

slack_webhook = 'https://hooks.slack.com/services/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'

slack_occupied_payload = {
    "username" : 'Mens Bathroom', 
    "icon_emoji": ':poop:', 
    "channel" : '#mens_room',  
    "text" : 'Mens Bathroom is #occupied, try again later'
}

headers = { 'Content-type' : 'application/json' }

io.setup(pir_pin, io.IN, io.PUD_DOWN)

previous_state = False
current_state = False


while True:
    time.sleep(0.5)
    previous_state = current_state
    current_state = io.input(pir_pin)
    print(current_state)
    if current_state != previous_state:
        if current_state:
            new_state = 'HIGH'
	    r = requests.post(slack_webhook, data=json.dumps(slack_occupied_payload), headers=headers)            
            time.sleep(10)
        else:
	    slack_free_payload = slack_occupied_payload
            slack_free_payload['text'] = 'Bathroom is free again'
            r = requests.post(slack_webhook, data=json.dumps(slack_free_payload), headers=headers) 
            new_state = 'LOW'
        print('GPIO pin %s is %s' % (pir_pin, new_state))
