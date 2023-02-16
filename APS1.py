import discord
import config
import YFinance

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name='A Cidade dos Robôs')
    channel = discord.utils.get(guild.text_channels, name='bot-fest')
    await channel.send('O bot está online!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == '!oi':
        await message.channel.send('Olá!')

    if message.content.lower() == '!source':
        await message.channel.send('Essa é a fonte do meu código:\nhttps://github.com/PedroHMenezes/NLPbot')
    
    if message.content.lower() == '!author':
        await message.channel.send('Fala meu! Meu criador é o Pedro Menezes.\nSe quiser falar com ele, esse é o email: pedrohmo@al.insper.edu.br')

    if "!run" in message.content.lower():
        message = message.content.lower().replace("!run","")
        tickers = YFinance.tickers(message)
        df = YFinance.database(message)
        for company in tickers:
            await message.channel.send(YFinance.last_price(company,df))
            await message.channel.send(YFinance.return_1w(company,df))
            await message.channel.send(YFinance.return_1m(company,df))
            await message.channel.send(YFinance.return_1y(company,df))


client.run(config.token)
 """

 """