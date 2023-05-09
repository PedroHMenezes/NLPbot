import discord
import config
import finance_functions as ff
import crawl_functions as cf
import generation as ge
import requests
from bs4 import BeautifulSoup
import re
import multiprocessing
import time

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

indice_palavras = {}
doc_links = []
doc_title = []
doc_frases = []
score = []
frase = ''

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name='A Cidade dos Robôs')
    channel = discord.utils.get(guild.text_channels, name='bot-fest')

@client.event
async def on_message(message):
    global indice_palavras, doc_links, doc_title, doc_frases, score, frase

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
            tickers = ff.tickers(mensagem)
            df = ff.database(mensagem)       
            for company in tickers:
                try:
                    await message.channel.send(ff.last_price(company,df))
                    await message.channel.send(ff.return_1w(company,df))
                    await message.channel.send(ff.return_1m(company,df))
                    await message.channel.send(ff.return_1y(company,df))
                    await message.channel.send("---------------------------------")
                except:
                    await message.channel.send('Vish... não achei nada para {} aqui não, é esse ticker mesmo?'.format(company))
                    await message.channel.send("---------------------------------")
        except:
            await message.channel.send('Vish... não achei nada para {} aqui não, é esse ticker mesmo?'.format(tickers[0]))
        
    if "!crawl" in message.content.lower():
        await message.channel.send('Só um segundo...')
        mensagem = message.content.lower().replace("!crawl","")
        try:
            doc_frases, doc_links, doc_title = cf.crawl(mensagem)
            await message.channel.send('Só mais um pouco... Preciso de três minutos')
            indice_palavras, score = cf.indice_invertido(doc_frases, doc_links, doc_title)
            await message.channel.send('Adicionei ao meu banco de dados!')
        except:
            await message.channel.send('Tive um erro com esse link...')

    if "!search" in message.content.lower():
        await message.channel.send('Só um segundo...')
        mensagem = message.content.lower().replace('!search','').strip()
        mensagem = mensagem.split(' ')

        if len(indice_palavras) == 0:
            indice_palavras, score = cf.indice_invertido(doc_frases, doc_links, doc_title)

        if len(mensagem) > 1:
            mensagem[1] = float(mensagem[1].replace('th=',''))
            return_message = cf.search(mensagem[0], indice_palavras, doc_links, doc_title, score,mensagem[1])
        else:
            return_message = cf.search(mensagem[0], indice_palavras, doc_links, doc_title, score,threshold=-1)
        await message.channel.send(return_message)

    if "!wn_search" in message.content.lower():
        await message.channel.send('Só um segundo...')
        mensagem = message.content.lower().replace('!wn_search','').strip()
        mensagem = mensagem.split(' ')
        if len(indice_palavras) == 0:
            indice_palavras, score = cf.indice_invertido(doc_frases, doc_links, doc_title)
        if len(mensagem) > 1:
            mensagem[1] = float(mensagem[1].replace('th=',''))
            return_message = cf.search(mensagem[0], indice_palavras, doc_links, doc_title, score,mensagem[1])
        else:
            return_message = cf.search(mensagem[0], indice_palavras, doc_links, doc_title, score,threshold=-1)
        await message.channel.send(return_message)

    if "!generate" in message.content.lower():
        await message.channel.send('Só um segundo...')
        mensagem = message.content.lower().replace('!generate','').strip()
        frase = ge.retorna_resultado(mensagem)
        await message.channel.send(frase)

    if "!help" in message.content.lower():
        await message.channel.send('Para utilizar minhas funções, basta rodar **!run + (Ticker de alguma empresa)** para ter informações sobre o preço da ação daquela empresa \n')
        await message.channel.send('__**Exemplo:**__ !run AMD para ter informações sobre a ação da AMD (ou !run AMD NVDA para ter acesso à múltiplas informações da AMD e NVIDIA)\n')
        await message.channel.send('> Alguns tickers para facilitar: \n> • Nvidia - NVDA\n> • Intel - INTC\n> • Ambev - ABEV\n> • Alibaba - BABA \n\nTodos os tickers podem ser acessados por aqui: https://finance.yahoo.com/')
        await message.channel.send('\nOBS: As informações são até o fechamento do último dia útil antes de hoje.')

    if "!clear" in message.content.lower():
        cf.clear()
        await message.channel.send('Banco de dados está limpo.')

client.run(config.token)