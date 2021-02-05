import json
from channels.generic.websocket import (
    AsyncWebsocketConsumer, WebsocketConsumer)
from asgiref.sync import async_to_sync


class SpinConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.spin_name = self.scope['url_route']['kwargs']['spin_name']
        self.spin_group_name = 'daru_spin'

        # Join spin group
        await self.channel_layer.group_add(
            self.spin_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
       
        await self.channel_layer.group_discard(
            self.spin_group_name,
            self.channel_name
        )

    # Receive pointer from WebSocket
    async def receive(self, text_data): # not needed if FrontEnd is not communicating/Our case
        text_data_json = json.loads(text_data)
        pointer = text_data_json['pointer']

        print(f'MESWEB{pointer}')

        # Send pointer to spin group
        await self.channel_layer.group_send(
            self.spin_group_name,
            {
                'type': 'spin_pointer',
                'pointer': pointer,
            }
        )

    # Receive pointer from spin group
    async def spin_pointer(self, event):
        pointer = event['pointer']
        # secondvalu = event['secondvalu']

        print(f'SPINNER{ pointer}')

        # Send pointer to WebSocket
        await self.send(text_data=json.dumps({
            'pointer': pointer,
            # 'second_valu':secondvalu
        }))

    # Receive pointer from spin group
    async def second_value(self, event):
        secondvalu = event['secondvalu']
        # mssg = ''
        # if secondvalu >50:
        #     mssg ='Betting is Active'
        # else:
        #    mssg ='Wait for next Market'
        # print(f'TIMER:{secondvalu}')

        # Send secondvalu to WebSocket
        await self.send(text_data=json.dumps({
            'secondvalu': secondvalu,
            # 'mssg':mssg,
        }))
    # Receive pointer from spin group

    async def market_info(self, event):
        market = event['market']

        print(f'MAKO {market}')
        
        # Send pointer to WebSocket
        await self.send(text_data=json.dumps({
            'market': market
        }))



class IspinConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.spin_name = self.scope['url_route']['kwargs']['spin_name']
        self.spin_group_name = 'i_spin'

        # Join spin group
        await self.channel_layer.group_add(
            self.spin_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
       
        await self.channel_layer.group_discard(
            self.spin_group_name,
            self.channel_name
        )

    # Receive pointer from WebSocket
    async def receive(self, text_data): # not needed if FrontEnd is not communicating/Our case
        text_data_json = json.loads(text_data)
        ipointer = text_data_json['ipointer']

        print(f'I_MESWEB{ipointer}')

        # Send pointer to spin group
        await self.channel_layer.group_send(
            self.spin_group_name,
            {
                'type': 'ispin_pointer',
                'ipointer': ipointer,
            }
        )

    # Receive pointer from spin group
    async def ispin_pointer(self, event):
        ipointer = event['ipointer']
        # secondvalu = event['secondvalu']

        print(f'I_SPINNER{ ipointer}')

        # Send pointer to WebSocket
        await self.send(text_data=json.dumps({
            'ipointer': ipointer,
            # 'second_valu':secondvalu
        }))








class QspinConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        ipointer = text_data_json['ipointer']
        print(f'QQMESWEB{ipointer}')
        #     # Send pointer to spin group
        self.send(
            {
                # 'type': 'ispin_pointer',
                'ipointer': ipointer,
            }
        )

    # # # Receive pointer from spin group
    # def ispin_pointer(self, event):
    #     ipointer = event['ipointer']
    #     print(f'QQSPINNER{ ipointer}')

    # #     # Send pointer to WebSocket
    #     self.send(text_data=json.dumps(
    #         {
    #             'ipointer': ipointer,
    #         }))
