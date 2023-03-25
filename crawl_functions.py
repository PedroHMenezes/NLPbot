import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import json
import random
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import wordnet
import nltk
nltk.download('wordnet')
nltk.download('omw')
nltk.download('omw-1.4')

def crawl (url):
    
    # Inicialização de variáveis
    human_text = []
    doc_frases = []
    doc_links = []
    doc_title = []
    depth = 3

    # Primeira busca sem utilizar crawl exige isso
    if len(url) == 0:
        url = 'https://en.wikipedia.org/wiki/Special:Random'
        depth = 1

    # Coleta dos dados do HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.get_text()

    for paragraph in soup.find_all('p'):
        if 'class' in paragraph.attrs and 'mw-empty-elt' in paragraph.attrs['class']:
            continue
        text = paragraph.get_text().strip()
        if text:
            human_text.append(text)

    # Junção do texto presente no HTML
    texto = '\n'.join(human_text)

    # Encontra todos os links na página e armazena eles, começando pelo link da página em si
    links = [response.url]
    links_main = [response.url]
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            absolute_url = urljoin(url.replace('Special:Random',''), href)
            if absolute_url.startswith('//'):
                absolute_url = urljoin('https:',absolute_url)
            elif absolute_url.startswith('/'):
                absolute_url = urljoin('https://en.wikipedia.org',absolute_url)
            links_main.append(absolute_url)    
            links.append(absolute_url)

    # Criação da pasta para armazenamento
    folder_name = "links"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Verifica se já existe aquela página
    json_file_path = f"{folder_name}/{title}.json"
    title_exists = False
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as f:
            data = json.load(f)
            for item in data:
                if item == title:
                    title_exists = True
                    break

    # Roda um for para todos os links (em uma largura de 'depth'), coletando texto e links
    link_data = {}
    for i in range(0,depth):
        n = random.randint(0,len(links))
        link = links[n]
        print(link)
        try:
            link_response = requests.get(link)
            links_children = [link_response.url]
            link_soup = BeautifulSoup(link_response.text, 'html.parser')
            link_title = link_soup.title.get_text()
            link_text = []
            for paragraph in link_soup.find_all('p'):
                if 'class' in paragraph.attrs and 'mw-empty-elt' in paragraph.attrs['class']:
                    continue
                text = paragraph.get_text().strip()
                if text:
                    link_text.append(text)

            for link in link_soup.find_all('a'):
                href = link.get('href')
                if href:
                    absolute_url = urljoin(url.replace('Special:Random',''), href)
                    if absolute_url.startswith('//'):
                        absolute_url = urljoin('https:',absolute_url)
                    elif absolute_url.startswith('/'):
                        absolute_url = urljoin('https://en.wikipedia.org',absolute_url)
                    links_children.append(absolute_url)
                    links.append(absolute_url)
            link_data[link_title] = {'text': '\n'.join(link_text), 'links': links_children}
        except:
            del links[n]

    # Anexa tudo em um só dicionário
    new_data_joint = {title: {'text': texto, 'links': links_main}}
    new_data_joint.update(link_data) 

    # Se o JSON não existir, adiciona o file na pasta
    if not title_exists:
        with open(json_file_path, "w+") as f:
            json.dump(new_data_joint, f)

    # Coleta dos dados para montagem do índice invertido
    folder_path = 'links'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(f"{folder_path}/{filename}", 'r+') as f:
                dic_file = dict(json.load(f))
                for indice, values in dic_file.items():
                    doc_frases.append(values['text'])
                    doc_links.append(values['links'][0])
                    doc_title.append(indice)

    # Vetorização por TFIDF
    vectorizer = TfidfVectorizer(use_idf=True, stop_words = 'english')
    tfidf = vectorizer.fit_transform(doc_frases)

    # Montagem do índice invertido
    indice_palavras = dict()
    for w in vectorizer.vocabulary_.keys():
        indice_palavras[w] = dict()
        for j in range(tfidf.shape[0]):
            if tfidf[j, vectorizer.vocabulary_[w] ] > 0:
                indice_palavras[w][j] = tfidf[ j, vectorizer.vocabulary_[w] ]
                
    return indice_palavras, doc_links, doc_title
                
def search(palavras, indice, doc_links, doc_title):
    n = 1
    palavras = re.findall('\w+',palavras)
    assert type(palavras)==list
    resultado = dict()
    try:
        for p in palavras:
            if p in indice.keys():
                for documento in indice[p].keys():
                    if documento not in resultado.keys():
                        resultado[documento] = indice[p][documento]
                    else:
                        resultado[documento] += indice[p][documento]
        if not bool(resultado):
            raise ValueError("Não está presente no banco de dados")
        dict_search = dict(sorted(resultado.items(), reverse = True, key=lambda item: item[1])[0:n])
        index = list(dict_search.keys())[0]
        return 'Achei esse link para sua busca:\n{0}: {1}'.format(doc_title[index],doc_links[index])    
    except:
        return 'Não há informações para {} no meu banco de dados. Gostaria de pesquisar outro termo?'.format(" ".join(palavras))

def wn_search(palavras, indice, doc_links, doc_title):
    n = 1
    palavras = re.findall('\w+',palavras)
    assert type(palavras)==list
    resultado = dict()
    try:
        for p in palavras:
            if p in indice.keys():
                for documento in indice[p].keys():
                    if documento not in resultado.keys():
                        resultado[documento] = indice[p][documento]
                    else:
                        resultado[documento] += indice[p][documento]
            else:
                syn = wordnet.synsets(p)
                for s in syn:
                    for l in s.lemmas():
                        if l.name() != p:
                            if l.name() in list(indice.keys()):
                                palavras.append(l.name())
        dict_search = dict(sorted(resultado.items(), reverse = True, key=lambda item: item[1])[0:n])
        index = list(dict_search.keys())[0]
        return "Achei esse link para sua busca: {0}: {1}".format(doc_title[index],doc_links[index])
    
    except: 
        return 'Não há informações para {} no meu banco de dado mais amplo. Gostaria de pesquisar outro termo?'.format(" ".join(palavras))