# Personalize a aparência da sua aplicação

Primeiro, crie um diretório chamado static no seu diretório polls. O Django vai procurar os arquivos estáticos ali, de maneira similar a como o Django encontra os templates dentro de polls/templates/.

A configuração STATICFILES_FINDERS do Django contém uma lista de buscadores que sabem como descobrir os arquivos estáticos de diversas fontes. Um dos padrões é o AppDirectoriesFinder que procura por um subdiretório “static” em cada uma das INSTALLED_APPS, como a polls que nós acabamos de criar. O site de administração usa a mesma estrutura de diretórios para os arquivos estáticos.

Arquivo estático namespace

Assim como os modelos, poderíamos conseguir colocar nossos arquivos estáticos diretamente polls/static(em vez de criar outro polls subdiretório), mas na verdade seria uma má ideia. O Django escolherá o primeiro arquivo estático que encontrar cujo nome corresponda, e se você tivesse um arquivo estático com o mesmo nome em uma aplicação diferente , o Django não conseguiria distinguir entre eles. Precisamos ser capazes de apontar o Django para o caminho certo, e a melhor maneira de garantir isso é colocando nomes neles. Ou seja, colocando esses arquivos estáticos dentro de outro diretório nomeado para o próprio aplicativo.


## imagens

A seguir, criaremos um subdiretório para imagens. Crie um imagessubdiretório no polls/static/polls/diretório. Dentro deste diretório, adicione qualquer arquivo de imagem que você gostaria de usar como plano de fundo. Para os fins deste tutorial, estamos usando um arquivo chamado background.png, que terá o caminho completo polls/static/polls/images/background.png.

Em seguida, adicione uma referência à sua imagem na sua folha de estilo ( polls/static/polls/style.css):

```css
body {
    background: white url("images/background.png") no-repeat;
}
```

![alt text](image-2.png)
