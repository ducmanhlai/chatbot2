import json
import aiohttp
from os import environ
from aiohttp import web
from code import update,sim
# fanpage token
PAGE_ACCESS_TOKEN = 'EAANKr7LqJe4BAA9MZCk2qMA9t0zZC6ziKu5TvgoJxTxqX7jPZAXLxBMPyjJvWBZBzVVxYgX0l76QqZA5mANJDQYylT9CqZA0ObZBKD1txbEmlZClzCaZBPDTl4u0HQaUjQ3KHPZBLx6t1kBelDhtfwP6Ljmt0nzEfaX5dqPqtZCAA3sTZBEVIsjS3fSr'
# verify token
VERIFY_TOKEN = 'token_cua_manh'
def get_message():
      chet,nhiem,khoi,dang=update()
      sample_responses = "Số ca tử vong: "+ str(chet)+"\n"+"Số ca nhiễm: "+str(nhiem)+"\n"+"Số ca khỏi: "+str(khoi)+"\n"+"Số ca đang điều trị: "+str(dang)+"\n"
      return sample_responses 
def xuli(mes):
    if "covid" in mes.lower or "corona" in mes.lower:
     a=get_message()
    else:
     a=sim(mes)
class BotControl(web.View):
     
   
    async def get(self):
        query = self.request.rel_url.query
        if(query.get('hub.mode') == "subscribe" and query.get("hub.challenge")):
            if not query.get("hub.verify_token") == VERIFY_TOKEN:
                return web.Response(text='Verification token mismatch', status=403)
            return web.Response(text=query.get("hub.challenge"))
        return web.Response(text='Forbidden', status=403)

    async def post(self):
        data = await self.request.json()
        if data.get("object") == "page":
            await self.send_greeting("Chào bạn. Mình là bot của Mạnh Gút Boi")

            for entry in data.get("entry"):
                for messaging_event in entry.get("messaging"):
                    if messaging_event.get("message"):
                        sender_id = messaging_event["sender"]["id"]
                        
                        await self.send_message(sender_id,xuli( messaging_event["message"]["text"]))
                          

        return web.Response(text='ok', status=200)

    async def send_greeting(self, message_text):
        params = {
            "access_token": PAGE_ACCESS_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "setting_type": "greeting",
            "greeting": {
                "text": message_text
            }
        })
        async with aiohttp.ClientSession() as session:
            await session.post("https://graph.facebook.com/v3.0/me/thread_settings", params=params, headers=headers, data=data)

    async def send_message(self, sender_id, message_text):

        params = {
            "access_token": PAGE_ACCESS_TOKEN
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": sender_id
            },
            "message": {
                "text": message_text
            }
        })

        async with aiohttp.ClientSession() as session:
            await session.post("https://graph.facebook.com/v3.0/me/messages", params=params, headers=headers, data=data)

    
routes = [
    web.get('/', BotControl, name='verify'),
    web.post('/', BotControl, name='webhook'),
]

app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app()
