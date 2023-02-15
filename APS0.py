import discord
import config

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

client.run(config.token)
