# Processo de desenvolvimento
## Etapa 1 - Configurações iniciais
A primeira etapa de desenvolvimento do bot conversacional é a definição da plataforma para conversação. Nesse caso, foi decidido que seria utilizado o Discord, uma plataforma para conversas, chamadas e compartilhamento de links e arquivos. Essa plataforma possui amplo apoio e fontes de informação para desenvolvimento de bots, a qual possui uma página dedicada para isso. Segue o link [aqui](https://discord.com/developers/applications). <br />

Nessa página, foi necessário criar a aplicação e o bot em si, além de conseguir autorizar ele para ter permissão de mandar mensagens e se conectar ao servidor da disciplina. Essa etapa do desenvolvimento gerou dúvidas na etapa de permissões do bot, especialmente sobre configurações definidas no código de quais informações o bot deveria ouvir e divergências no portal do discord. Para exemplificar, a seguinte linha do código define quais eventos o bot deve ouvir, além de permitir que ele tenha acesso às informações dos membros do servidor.

```
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
```
Ao rodar o código, ele apresentava um erro de permissões na primeira linha de intents. A solução era simples, pois apenas deveria ser ajustada uma configuração na página de desenvolvedor do discord relacionada a *server members intent*, na aba 'Bot' nesse link [aqui](https://discord.com/developers/applications).

![Members Intent - Discord](https://user-images.githubusercontent.com/49311416/219165333-dca69534-cc77-43a5-a29a-e4379406ff87.png)

Para essa solução, foi utilizada essa thread do Stack Overflow [aqui](https://stackoverflow.com/questions/65371837/my-on-member-join-event-is-not-working-i-tried-intents-but-it-gives-this-error). Além dessa dificuldade, não houveram outros entraves para solução, mas pontos de atenção para rodar o bot na VM disponibilizada. <br />

O primeiro ponto de atenção é tomar cuidado para não subir o código com seu Token escrito, e sim utilizar o .gitignore para criar um arquivo que não será levado em consideração (ignorado) no momento de subir as atualizações no GitHub. Dito isso, importante relembrar de criar um arquivo e adicionar o nome desse arquivo no seu .gitignore para evitar problemas de vazamento de token. <br />

Em segundo lugar, utilizamos um servidor hospedado no Insper para rodar máquinas virtuais (VM) dedicadas para o projeto. Nestas máquinas virtuais, estariam os códigos dos nossos bots, pois assim não teriam a necessidade de ficar constantemente rodando nos nossos computadores e explora habilidades de hospedagem de aplicações. Com isso, outro desafio foi a hospedagem e manutenção do código funcionando no ambiente em nuvem. Para ter acesso às máquinas virtuais, foi utilizado um acesso via SSH no servidor disponibilizado via PowerShell. <br />

Para manutenção do código, foi utilizado o comando nohup do Linux ('No Hangups') para continuar rodando o arquivo do bot em background no processamento do servidor. A seguir estão os comandos utilizados para setar essa configuração.
