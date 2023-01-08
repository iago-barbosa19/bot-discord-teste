# Discord Bot
> Esse código foi feito em Python, na versão 3.11
>
> Esse repositório está com poucos commits se comparado ao original, pois o original tinha no appsettings a minha chave pessoal do bot do discord,
> então foi necessário criar um  repositório novo.
>
> Também é necessário ter em mente que é para criar um arquivo "appsettings.json" da mesma forma que o disponibilizado como modelo, 
> para que possa fazer as configurações básicas do software.
>
> Para o Software funcionar na mais perfeita ordem, é necessário/recomendado que as seguintes dependência sejam instaladas.
>
> Dependências:
> | Dependência | Tipo | Comentário|
> |---------|-----|------------|
> | Python 3.11 | Linguagem | Python instalado na versão 3.11, para que seja compilado corretamente |
> | appsettings.json| Configuração | Arquivo de configuração do projeto|
> | redis | Banco de dados | Banco de dados que foi usado para armazenar alguns dados que o bot utiliza |
> | redis | pip-dependency | Dependência do Python para efetuar a conexão ao banco de dados |
> | discord | pip-dependency | Dependência PIP. Esta API do Discord é usada para fazer o Bot |
> | discord.py | pip-dependency | Dependência PIP. Outra dependência da API do Discord usada para fazer o Bot |
> | jsonpickle | pip-dependency | Dependência PIP. Usada para poder guardar os resultados das pesquisas em um arquivo JSON, em um formato que facilite para o Python ler |
> | textblob | pip-dependency | Dependência PIP. Esta dependência é usada para efetuar as traduções de alguns textos em inglês para português. Esta biblioteca é meio lenta, então precisa ser trocada |
> | requests | pip-dependency | Dependência PIP. Usada para fazer uma requisição a uma API que pega a cotação atual de algumas moedas |
> | Atlas Academy API | API | API de dados do Jogo Fate Grand Order. Essa API é utilizada para pegar algumas informações do jogo, e enviar pelo Bot |
> | Economia Awesome API| API | API de economia. Um endpoint de cotação monetária é utilizada. É usada para pegar a cotação de uma moeda para outra |
---
Esse Bot foi desenvolvido usando diversas dependências, como mostrado acima. Em casos de melhorias, ou dúvidas quanto ao funcionamento de certas funções, pode ser necessário olhar a biblioteca das dependências.


Links das documentações:
1. https://discordpy.readthedocs.io/en/stable/index.html
2. https://api.atlasacademy.io/rapidoc
3. https://redis.readthedocs.io/en/latest/genindex.html
4. https://docs.awesomeapi.com.br/api-de-moedas
5. https://jsonpickle.github.io/
6. https://textblob.readthedocs.io/en/dev/
7. https://requests.readthedocs.io/en/latest/
---
Como é um projeto que eu fiz para aprender a API do discord, e fazer alguns testes a mais, acabou por se tornar um projeto não muito "rebuscado". Mas ainda é um projeto que eu pretendo mais para frente melhorar, ou algo do tipo.
