import os
import paho.mqtt.client as mqtt_client
import asyncio
from binance import AsyncClient, BinanceSocketManager
from binance import ThreadedWebsocketManager
from datetime import datetime

bclient = None
broker = ''
port = 1883
topic = "/binance/sub/"
client_id = f'subscriber-binance'
api_key = ""
api_secret = ""

dt = datetime.now()
dttt = datetime.timestamp(dt)



async def status():
    global bclient, dt, dttt
    dtt = datetime.timestamp(dt)
    if not bclient:
        aclient = await AsyncClient.create(api_key, api_secret)
    while True:
        try:
            # print('SDFSDFSDFSDFSDF')
            status = await aclient.get_system_status()
            # print(dir(status))
            if not status:
                print('kjsdf')
                asyncio.get_event_loop().close()
            ddt =  dtt - dttt
            if ddt >= 60:
                os.system("sudo pkill python3")
        except Exception as e:
            print('BREAK')
            os.system("sudo pkill python3")


        await asyncio.sleep(1)

def connect_mqtt():
    async def on_content(client, userdata, flags, rc):
        if rc == 0:
            print("Connect to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set("username")
    client.on_connect = on_content
    client.connect(broker, port)
    return client

client = connect_mqtt()

async def x():
    client = await AsyncClient.create(api_key, api_secret)
    mqttclient = connect_mqtt()
    bm = BinanceSocketManager(client)
    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    twm.start()

    async def get_tickers():
        exchange = await client.get_exchange_info()

        rows = []
        for e in exchange['symbols']:
            if 'USDT' in e['symbol']:
                rows.append(e['symbol'].lower()+'@miniTicker')
        return rows

    def handle_socket_message(msg):
        global dt
        dttt = datetime.timestamp(dt)

        if msg and 'data' in msg.keys():

            print(msg['data']['s'], msg['data']['c'])
            publish(client=mqttclient, topic='/binance/ticker/' + msg['data']['s'], msg=msg['data']['c'])
        else:
            print("msg empty")

    streams = await get_tickers()
    twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)


    await client.close_connection()

def publish(client, topic, msg):
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print("send to topic "+topic)
    else:
        os.system("sudo pkill python3")


async def run():
    task1 = asyncio.create_task(status())
    task2 = asyncio.create_task(x())
    await task1
    await task2

asyncio.run(run())