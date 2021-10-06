import json
from timeit import default_timer as timer

from channels.generic.websocket import AsyncWebsocketConsumer
import matplotlib.pyplot as plt

from api.locator import Locator

locator = Locator()


class DistancesConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = "1"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)  # {'distance': '429', 'id': 'TM3'}
        if text_data_json['id'] == 'start':
        
            locator.coords = []
            locator.TM1 = -100
            locator.TM2 = -100
            locator.TM3 = -100
            locator.ZTM4 = -100
            return
        if text_data_json['id'] == 'stop':
            plt.figure()
            plt.plot([locator.coords[i][0] for i in range(0, len(locator.coords))],
                     [locator.coords[i][1] for i in range(0, len(locator.coords))])
            plt.gca().set(xlim=(0, 500), ylim=(0, 500), xlabel='X', ylabel='Y')
            plt.savefig('static/1.png')

            plt.figure()
            plt.plot([locator.coords[i][0] for i in range(0, len(locator.coords))],
                     [locator.coords[i][2] for i in range(0, len(locator.coords))])
            plt.gca().set(xlim=(0, 500), ylim=(0, 500), xlabel='X', ylabel='Z')
            plt.savefig('static/2.png')

            locator.coords = []
            locator.TM1 = -100
            locator.TM2 = -100
            locator.TM3 = -100
            locator.ZTM4 = -100
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'front_message',
                    'X': -1,
                    'Y': -1,
                    'Z': -1,
                }
            )
            return
        locator.updateValue(text_data_json)
        if (timer() - locator.start_time) * 1000 > 10:

            X, Y, Z = locator.planB()
            if X == -1:
                return

            locator.TM1 = -100
            locator.TM2 = -100
            locator.TM3 = -100
            locator.ZTM4 = -100

            locator.coords.append([X, Y, Z])

            locator.start_time = timer()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'front_message',
                    'X': X,
                    'Y': Y,
                    'Z': Z,
                }
            )

    async def front_message(self, event):
        X = event['X']
        Y = event['Y']
        Z = event['Z']

        await self.send(text_data=json.dumps({
            'X': X,
            'Y': Y,
            'Z': Z,
        }, ensure_ascii=False))
