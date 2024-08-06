import paho.mqtt.client as mqtt


def on_message(client, userdata, msg):
    print(f"Temperature: {round(float(msg.payload), 2)}")


# mqttBroker = "mqtt.eclipseprojects.io"
mqttBroker = "127.0.0.1"
client = mqtt.Client()
client.on_message = on_message
client.connect(mqttBroker)
client.subscribe("T1")
client.loop_forever()
