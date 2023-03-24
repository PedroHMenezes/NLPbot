# Configuração do web crawling / scraping
## Comentário inicial
O desenvolvimento dessa etapa do chatbot se pautou em criar uma funcionalidade de web crawling. A partir do fornecimento de uma URL, o bot deve ser capaz de indicar quais são as referências a determinados termos procurados por cada usuário.

Para essa funcionalidade, foi utilizado o ChatGPT, no qual foi perguntado a ele "How can I make a web scraping in python?". A resposta dele contempla explicações junto com códigos a serem executados.

Naturalmente, foram necessárias algumas iterações com o chatbot para compreensão completa do problema e ajustes de pequenos erros que surgiram, sendo algumas das perguntas: "How can I make the web scraping above find all occurrences of a specific term?" ou "How can I save the page content in a local database?" 

## Bibliotecas necessárias

```
pip install -U scikit-learn
```
```
pip install nltk
```
