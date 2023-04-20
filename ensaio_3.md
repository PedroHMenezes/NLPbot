## Contexto Inicial
Como ponto de partida, foi utilizado o código da entrega anterior, na qual precisávamos fazer o web scrapping de páginas na internet em busca de conteúdo que pudesse criar um buscador próprio.
No desenvolvimento do código dessa entrega foi realizada alterações no código anterior, uma vez que ele é a base para a filtragem de conteúdo nas páginas. 

## Desenvolvimento
Em primeiro lugar, foi buscado um banco de dados que possuísse informações sobre conteúdos considerados tóxicos para o posterior desenvolvimento de um modelo que pudesse
separar aquilo que é tóxico do não tóxico. O banco de dados está disponível [aqui](https://www.kaggle.com/datasets/fizzbuzz/cleaned-toxic-comments).

Com essas informações, foi selecionado os dados para esse projeto, como caracterização de tóxico vs. não tóxico para treinamento de um modelo. Foram testados alguns métodos e 
o mais adequado para esse projeto nas minhas pesquisas foi o regressor logístico por sua baixa complexidade e alta acurácia nos testes (~85%).

Dessa forma, foi desenvolvido um modelo que pudesse prever a probabilidade daquele conteúdo ser tóxico ou não dado o texto presente na página, realizado um cálculo para que o 
nivel de sensibilidade do modelo estivesse entre -1 a 1. Esse modelo, então, foi levado para o código do chatbot já pronto para ser utilizado e acoplado nas funções de crawling.

Por fim, foram realizadas algumas alterações nas funções de crawling para que o filtro inputado pelo usuário fosse considerado junto.
