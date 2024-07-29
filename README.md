# ArtAscii Huffman Compress

**Número da Lista**: X<br>
**Conteúdo da Disciplina**: Greed Algorithm<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 22/1008786 |  Mateus Villela Consorte |
| xx/xxxxxx  |  xxxx xxxx xxxxx |

### Motivação
Com o intuito de aplicar a codificação de Huffman para além de um contexto puramente textual, este projeto motiva-se a trazer a perspectiva da compactação de arquivos de imagem. Nesse sentido,
foi escolhido a representação por arte ASCII - uma abordagem simples e adequada para o algoritimo em questão - que captura a essência das técnicas de compressão de dados de imagens.

### Objetivos
 - Conversor de imagens para ascii art.
 - Compressor de arquivos: .txt -> .bin
 - Descompressor de arquivos: .bin -> .txt

Com isso, visa-se alcançar maior compreenção do algoritimo ambicioso de codificação de Huffman, além de contribuir para o entendimento e empolgação de outros estudantes e interessados acerca de tal algoritimo de extrema relevância.

## Arte ASCII

1. **Origens e Desenvolvimento Inicial:**
   - **Typewriter Art**: Antes dos computadores modernos, já existia uma forma semelhante de arte realizada com máquinas de escrever, conhecida como typewriter art. Nesse contexto, os artistas criavam desenhos e padrões usando os caracteres disponíveis nas máquinas de escrever.
   - A **ASCII Art** tem suas raízes nos primórdios da computação, quando os computadores eram usados principalmente para processar texto e não possuíam capacidade gráfica avançada.
   - Na década de 1960, o **Padrão ASCII** (American Standard Code for Information Interchange) foi estabelecido. Esse padrão definiu um conjunto de 128 caracteres, incluindo letras maiúsculas e minúsculas, números, símbolos de pontuação e caracteres de controle.
   - Artistas e entusiastas começaram a explorar maneiras criativas de usar esses caracteres para criar imagens e ilustrações.

3. **Kenneth Knowlton e os Laboratórios Bell:**
   - Um dos pioneiros em arte computacional foi Kenneth Knowlton, que trabalhava nos Laboratórios Bell na década de 1960.
   - Knowlton criou algumas das primeiras **ASCII Arts**, usando impressoras que frequentemente não tinham capacidade gráfica. Ele usava os caracteres disponíveis para formar padrões e desenhos.
   - Essas criações eram frequentemente impressas em grandes páginas de banner, facilitando a separação dos resultados por operadores ou funcionários de computador.

4. **Popularização na Década de 1970:**
   - Durante a década de 1970, a **ASCII Art** se tornou mais popular à medida que os computadores pessoais e mainframes se espalhavam.
   - Programadores, hackers e entusiastas começaram a criar arte usando os caracteres ASCII disponíveis em seus terminais de texto.
   - A **ASCII Art** era usada em banners, cabeçalhos de documentos, cartazes e até mesmo em jogos de texto.

5. **Variedade e Criatividade:**
   - A criatividade na **ASCII Art** era vasta. Alguns artistas criavam retratos detalhados, enquanto outros faziam padrões abstratos ou ilustrações temáticas.
   - A limitação dos 95 caracteres imprimíveis do **Padrão ASCII** incentivava a inovação. Artistas usavam diferentes combinações de caracteres para obter sombras, texturas e detalhes.
   - Classes:
      - Typewriter art,
      - Text art,
      - TTY e RTTY art,
      - Line art,
      - Block art; e outros.

6. **Declínio e Revival:**
   - Com o advento dos gráficos de alta resolução e a popularização da internet, a **ASCII Art** perdeu parte de sua relevância.
   - No entanto, houve um renascimento nos últimos anos, com artistas digitais revisitando essa forma de expressão e criando novas obras usando caracteres ASCII.

7. **Aplicação no contexto do projeto: ArtAsciiCompress**
   - Perceba que **ASCII art** é uma forma de representar figuras gráficas por elementos textuais do padrão ASCII, os quais possuem densidadese visuais e capacidades representativas distintas. *Por exemplo*: caracteres como '#', '@', '*' e '.' podem ser usados para simular diferentes níveis de tonalidade entre clara, intermediária e escura.
   - Nesse sentido, ele presume uma relação de conversão de texturas e tonalidades para esses caracteres. Ou seja, um histograma de caracteres ASCII pode ser uma maneira intuitiva para representam as texturas e tonalidade da imagem.
   - Em compressores de imagem baseado na codificação de Huffman, está presente a geração dos histogramas para representar as distribuições de frequência. De modo semelhante, um dos objetivos do projeto é converter imagens para ASCII Art, o que será feita pela escala de cinza aplicada à imagem e, a partir daí, relacionada a caracteres que o representarão.

Em resumo, a **ASCII Art** é uma forma criativa e nostálgica de expressão visual que remonta aos primórdios da computação e continua a inspirar artistas e entusiastas até hoje.

Claro! Vamos aprofundar os detalhes do **algoritmo de Huffman**, incluindo sua premissa, demonstração matemática e considerações sobre seu desempenho. Também abordarei possíveis restrições e limitações, especialmente em relação à compressão de imagens.

## Código de Huffman

O **algoritmo de Huffman** é um método de **compressão de dados sem perdas** que otimiza o espaço usando **códigos variáveis** baseados na frequência dos caracteres. Ele oferece insights valiosos em análise de frequência e otimização de algoritmos, com aplicações além da compressão de dados².

### Premissa do Algoritmo de Huffman

A ideia fundamental do **algoritmo de Huffman** é usar **códigos curtos** para os caracteres que ocorrem com **maior frequência** e deixar os códigos mais longos para os caracteres mais raros. Esses códigos são, portanto, de **comprimento variável**. A escolha da melhor tabela de códigos é o segredo do algoritmo de Huffman¹.

### Demonstração Matemática

Vamos provar que o algoritmo de Huffman é ótimo em termos de comprimento médio de bits por símbolo. Para isso, consideremos o seguinte:

1. **Teorema de Shannon**:
   - O comprimento médio de bits por símbolo em qualquer codificação de fonte não pode ser menor que a **entropia** da fonte.
   - A **entropia** é uma medida da incerteza ou imprevisibilidade da fonte.

2. **Entropia**:
   - A entropia de uma fonte discreta com probabilidades $(p_1, p_2, \ldots, p_n)$ é dada por:

     $$H(X) = - \sum_{i=1}^{n} p_i \ log_2(p_i)$$

3. **Codificação de Huffman**:
   - O algoritmo de Huffman constrói uma árvore binária de códigos de prefixo, onde os códigos são atribuídos com base nas frequências dos símbolos.
   - A árvore de Huffman é construída de forma a minimizar o comprimento médio de bits por símbolo.

4. **Tamanho do arquivo comprimido**
Se $T$ é a árvore que representa a codificação, $d_T(c)$ é a profundidade da folha representando o caracter $c$ e $f(c)$ é a sua frequência, o tamanho do arquivo comprimido será:
$$B(T) = \sum_{c \in C} f(c) \ d_T(c) \ \ .$$

- $B(T)$ é o custo da árvore T, extamente o tamanho do arquivo codificado.
 
6. **Prova**:
   - A árvore de Huffman é construída de forma a aproximar a entropia da fonte.
   - Portanto, o comprimento médio de bits por símbolo usando Huffman é próximo à entropia da fonte.
   - Como a entropia é o limite inferior para o comprimento médio de bits, o algoritmo de Huffman é ótimo.

### Considerações e Restrições
  - O algoritmo de Huffman pode ser aplicado a imagens, mas tem limitações.
  - Ele não leva em consideração a relação espacial entre pixels vizinhos, o que outros algoritmos (como JPEG) fazem.
  - A compressão de imagens usando Huffman pode não ser tão eficiente quanto métodos baseados em entropia.

## Screenshots
Adicione 3 ou mais screenshots do projeto em funcionamento.

## Instalação 
**Linguagem**: Python<br>
**Framework**: --<br>

### Requisitos

## Uso 
Explique como usar seu projeto caso haja algum passo a passo após o comando de execução.

## Outros 
Quaisquer outras informações sobre seu projeto podem ser descritas abaixo.




