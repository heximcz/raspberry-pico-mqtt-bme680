"""
Hexim MQTT extend for Adafruit miniMqtt
"""
import gc
import json
import os
import ssl
import time
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import microcontroller
import socketpool
import wifi

class mqtt(MQTT.MQTT):

    def __init__(self, subscriber: bool = True, debug: bool = False) -> None:
        """
        :param bool subscriber: Enable subcriber functions etc. "restart".
            Listen on MQTT_SUB_TOPIC
        :param bool debug: Enable create debug callbacks
        """

        # Params
        self.subscriber = subscriber
        self.debug = debug

        # Create a socket pool
        self.socket = socketpool.SocketPool(wifi.radio)

        # Set up a MiniMQTT Client
        self.mqtt_client = MQTT.MQTT(
            broker=os.getenv('MQTT_BROKER'),
            port=os.getenv('MQTT_PORT'),
            username=os.getenv('MQTT_USER'),
            password=os.getenv('MQTT_PWD'),
            socket_pool=self.socket,
            ssl_context=ssl.create_default_context()
        )

        self.pub_topic = os.getenv('MQTT_PUB_TOPIC')

        # Connect callback handlers to client
        if self.subscriber:
            # enable sub message callback
            self.mqtt_client.on_message = self.message
        # Create callbacks only on debug
        if self.debug:
            self.mqtt_client.on_connect = self.connect
            self.mqtt_client.on_publish = self.publish
            self.mqtt_client.on_subscribe = self.subscribe
            self.mqtt_client.on_unsubscribe = self.unsubscribe
            self.mqtt_client.on_disconnect = self.disconnect

        # Create connect to the broker
        try:
            if self.debug:
                print("Attempting to connect to %s" % self.mqtt_client.broker)
            self.mqtt_client.connect()
        except MQTT.MMQTTException as e:
            print(e)
            time.sleep(10)
            # Reboot device a try again
            microcontroller.reset()

        # Create subscriber
        if self.subscriber:
            self.sub_topic = os.getenv('MQTT_SUB_TOPIC')
            self.mqtt_client.subscribe(self.sub_topic)

    # Define callback methods which are called when events occur
    def connect(self, mqtt_client, userdata, flags, rc) -> None:
        # This function will be called when the client is connected
        # successfully to the broker.
        print("Connected to MQTT Broker!")
        print("Flags: {0}\nRC: {1}".format(flags, rc))

    def disconnect(self, mqtt_client, userdata, rc) -> None:
        # This method is called when the client disconnects
        # from the broker.
        print("Disconnected from MQTT Broker!")

    def subscribe(self, mqtt_client, userdata, topic, granted_qos) -> None:
        # This method is called when the client subscribes to a new feed.
        print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))

    def unsubscribe(self, mqtt_client, user_data, topic, pid) -> None:
        # This method is called when the client unsubscribes from a feed.
        print("Unsubscribed from {0} with PID {1}".format(topic, pid))

    def publish(self, mqtt_client, userdata, topic, pid) -> None:
        # This method is called when the client publishes data to a feed.
        print("Published to {0} with PID {1}".format(topic, pid))

    def message(self, mqtt_client, topic, message) -> None:
        # Method callled when a client's subscribed feed has a new value.
        if self.debug:
            print("New message on topic {0}: {1}".format(topic, message))
        
        # Restart machine
        if message == "restart":
            try:
                self.mqtt_client.unsubscribe(self.sub_topic)
                self.mqtt_client.disconnect()
            except:
                pass
            microcontroller.reset()

        # Return system info
        if message == "status":
            status = dict({})
            try:

                # Get free memory in kB
                status["free_mem_kB"] = round(float(gc.mem_free()/1000))
                # Get the free space in kB
                stat = os.statvfs("/")
                free_space = stat[0] * stat[4]
                status["hdd_free_kB"] = free_space // 1024
                # Get machine name
                status["machine"] = str(os.uname().machine)
                # Get CPU temperature in °C
                status["cpu_temp_C"] = round(microcontroller.cpu.temperature,1)
                # Get IPv4 address
                status["ip_address"] = str(wifi.radio.ipv4_address)
                # Get and format MAC address of wifi
                mac = ''
                for i in wifi.radio.mac_address:
                    mac=mac+'{:02x}'.format(i)+":"
                status["mac_adress"]=mac[:-1]

                # MQTT Publish on .../status
                self.pub(msg=status, topic=self.pub_topic+"/status")
            except:
                microcontroller.reset()

    def is_subscriber(self) -> bool:
        return self.subscriber
    
    def pub(self, msg: dict, topic: str = None) -> None:
        """
        MQTT Publisher
        :params dict({}) msg
        :params string topic
        """
        try:
            if topic is not None:
                self.mqtt_client.publish(topic, json.dumps(msg))
                return
            self.mqtt_client.publish(self.pub_topic, json.dumps(msg))
        except:
            microcontroller.reset()
