import discord
import requests,os
import pandas as pd
import df2img

my_secret = os.environ['TOKEN']

def get_data(name):
    response = requests.get('https://live.nepse.repl.co/api.php').json()
    # fnmae = db[name]
    for x in response['live_data']:
        if(x['symbol']== name):
            change = "{:.2f}".format(float(x['percent_change']))
            data = {'LTP':[x['ltp']],
              '%change':[change],
              'High':[x['high']],
              'Low':[x['low']],
              'Qty':[x['qty']]}
            df = pd.DataFrame(data,index=[name])
            if float(change)>=0:
              fig = df2img.plot_dataframe(df,tbl_header=dict(
              align="center",
              fill_color="green",
              font_color="white",
              font_size=14,
              ),fig_size=(500,60))
            else:
              fig = df2img.plot_dataframe(df,tbl_header=dict(
              align="center",
              fill_color="red",
              font_color="white",
              font_size=14,
              ),fig_size=(500,60))
            df2img.save_dataframe(fig=fig, filename="plot.png")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
    
    async def on_message(self, message):
      msg = message.content
      if msg.startswith('$'):
        msg = (msg[1:]).upper()
        msg = get_data(msg)
        await message.channel.send(file=discord.File("plot.png"))

# get_data()
client = MyClient()
client.run(my_secret)