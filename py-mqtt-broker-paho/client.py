import paho.mqtt.client as mqtt
import time
import tclab

# mqttBroker = "mqtt.eclipseprojects.io"
mqttBroker = "127.0.0.1"
client = mqtt.Client()
client.connect(mqttBroker)

with tclab.TCLabModel() as lab:
    lab.Q1(70)
    for i in range(30):
        client.publish("T1", lab.T1)
        print("Published ", str(round(lab.T1, 2)))
        time.sleep(1)
