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

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == '!oi':
        await message.channel.send('Olá!')

    if message.content.lower() == '!source':
        await message.channel.send('Essa é a fonte do meu código:\nhttps://github.com/PedroHMenezes/NLPbot')
    
    if message.content.lower() == '!author':
        await message.channel.send('Tudo bem? Meu criador é o Pedro Menezes.\nSe quiser falar com ele, esse é o email: pedrohmo@al.insper.edu.br')

    if "!run" in message.content.lower():
        await message.channel.send('Só um segundo...')
        mensagem = message.content.lower().replace("!run","")
        try:
            tickers = YFinance.tickers(mensagem)
            df = YFinance.database(mensagem)       
            for company in tickers:
                await message.channel.send(YFinance.last_price(company,df))
                await message.channel.send(YFinance.return_1w(company,df))
                await message.channel.send(YFinance.return_1m(company,df))
                await message.channel.send(YFinance.return_1y(company,df))
                await message.channel.send("---------------------------------")
        except:
            await message.channel.send('Vish... não achei nada aqui não, é esse ticker mesmo?')


    if "!help" in message.content.lower():
        await message.channel.send('Para utilizar minhas funções, basta rodar **!run + (Ticker de alguma empresa)** para ter informações sobre o preço da ação daquela empresa \n')
        await message.channel.send('__**Exemplo:**__ !run AMD para ter informações sobre a ação da AMD \n')
        await message.channel.send('> Alguns tickers para facilitar: \n> • Nvidia - NVDA\n> • Intel - INTC\n> • Ambev - ABEV\n> • Alibaba - BABA \n\nTodos os tickers podem ser acessados por aqui: https://finance.yahoo.com/')
        await message.channel.send('\nOBS: As informações são até o fechamento do último dia útil antes de hoje.')
                                


client.run(config.token)