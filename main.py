""" imports """
import discord
import requests
import json
import my_token

""" to get json file to map SYMBOL to company NAME """
file = open('company.json')
data = json.load(file)

""" get the essential data of the company """
async def get_data(name):
    response = requests.get('https://nepse-data-api.herokuapp.com/data/todaysprice').json()
    fname = data[f'{name}']
    for x in response:
        if(x['companyName']==fname):
            return(x)

""" discord bot client to handle all related task to bot """
class MyClient(discord.Client):
    """ to initialize bot """
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    """ to send the message on appropriate command (i.e $ followed by company name) """
    async def on_message(self, message):
        if message.author == self.user:
            return 

        msg = message.content
        if msg.startswith('$'):
            req = (str(msg[1:])).upper()
            cdata = await get_data(req)
            await message.channel.send(f"{req}:\n \tLTP : {cdata['closingPrice']}\t\t\t\t Difference : {cdata['difference']} \n Traded Share : {cdata['tradedShares']}\t TAmount : {cdata['amount']}")

client = MyClient()
client.run(my_token.token)
