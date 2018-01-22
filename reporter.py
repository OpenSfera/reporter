import paho.mqtt.client as mqtt
import time
from datetime import datetime, timedelta
import json
import configparser
import sferaconfig
from pymongo import MongoClient

sample_time = sferaconfig.getConfig("reporter_sample_time", 600)
technician_broadcast_time = sferaconfig.getConfig("technician_broadcast_time", 5)
next_sample = datetime.utcnow()

def getDb():
    client = MongoClient('mongodb://localhost:27017/')
    return client['sfera']

def on_message(client, userdata, msg):
    message = json.loads(msg.payload.decode('UTF-8'))
    now = datetime.utcnow()
    if msg.topic == "local/status" and message.get("event", None) == "sfera_status":
        global sample_time, next_sample
        if now > next_sample:
            d = message["data"]
            d["time"] = now
            db = getDb()
            samples = db.samples
            samples.insert_one(d)
            next_sample = now + timedelta(seconds=sample_time)
    elif msg.topic == "local/alert" and message.get("type", None) == "user_alert":
        d = message
        del d["expire_on"]
        del d["countdown"]
        d["time"] = now
        db = getDb()
        alerts = db.alerts
        alerts.insert_one(d)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("local/status")
    client.subscribe("local/alert")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

client = mqtt.Client(client_id="reporter")
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connect("localhost", 1883, 60)

client.loop_forever()
