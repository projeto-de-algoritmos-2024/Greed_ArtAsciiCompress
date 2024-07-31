# ArtAscii Huffman Compress

**Número da Lista**: 29<br>
**Conteúdo da Disciplina**: Greed Algorithm<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 22/1008786 |  Mateus Villela Consorte |
| 22/1008679 |  Pablo Serra Carvalho|

### Motivação
Com o intuito de aplicar a codificação de Huffman para além de um contexto puramente textual, este projeto motiva-se a trazer a perspectiva da compactação de arquivos de imagem. Nesse sentido,
foi escolhido a representação por arte ASCII - uma abordagem simples e adequada para o algoritimo em questão - que captura a essência das técnicas de compressão de dados de imagens.

### Objetivos
 - Conversor de imagens para ascii art.
 - Compressor de arquivos: .txt -> .bin
 - Descompressor de arquivos: .bin -> .txt

Com isso, visa-se alcançar maior compreenção do algoritimo ambicioso de codificação de Huffman, além de contribuir para o entendimento e empolgação de outros estudantes e interessados acerca de tal algoritimo de extrema relevância.

## Arte ASCII

<details>
<summary><strong>1. Origens e Desenvolvimento Inicial:</strong></summary>

- **Typewriter Art**: Antes dos computadores modernos, já existia uma forma semelhante de arte realizada com máquinas de escrever, conhecida como typewriter art. Nesse contexto, os artistas criavam desenhos e padrões usando os caracteres disponíveis nas máquinas de escrever.
- A **ASCII Art** tem suas raízes nos primórdios da computação, quando os computadores eram usados principalmente para processar texto e não possuíam capacidade gráfica avançada.
- Na década de 1960, o **Padrão ASCII** (American Standard Code for Information Interchange) foi estabelecido. Esse padrão definiu um conjunto de 128 caracteres, incluindo letras maiúsculas e minúsculas, números, símbolos de pontuação e caracteres de controle.
- Artistas e entusiastas começaram a explorar maneiras criativas de usar esses caracteres para criar imagens e ilustrações.
</details>

<details>
<summary><strong>3. Kenneth Knowlton e os Laboratórios Bell:</strong></summary>

- Um dos pioneiros em arte computacional foi Kenneth Knowlton, que trabalhava nos Laboratórios Bell na década de 1960.
- Knowlton criou algumas das primeiras **ASCII Arts**, usando impressoras que frequentemente não tinham capacidade gráfica. Ele usava os caracteres disponíveis para formar padrões e desenhos.
- Essas criações eram frequentemente impressas em grandes páginas de banner, facilitando a separação dos resultados por operadores ou funcionários de computador.
</details>

<details>
<summary><strong>4. Popularização na Década de 1970:</strong></summary>

- Durante a década de 1970, a **ASCII Art** se tornou mais popular à medida que os computadores pessoais e mainframes se espalhavam.
- Programadores, hackers e entusiastas começaram a criar arte usando os caracteres ASCII disponíveis em seus terminais de texto.
- A **ASCII Art** era usada em banners, cabeçalhos de documentos, cartazes e até mesmo em jogos de texto.
</details>

<details>
<summary><strong>5. Variedade e Criatividade:</strong></summary>

- A criatividade na **ASCII Art** era vasta. Alguns artistas criavam retratos detalhados, enquanto outros faziam padrões abstratos ou ilustrações temáticas.
- A limitação dos 95 caracteres imprimíveis do **Padrão ASCII** incentivava a inovação. Artistas usavam diferentes combinações de caracteres para obter sombras, texturas e detalhes.
- Classes:
  - Typewriter art,
  - Text art,
  - TTY e RTTY art,
  - Line art,
  - Block art; e outros.
</details>

<details>
<summary><strong>6. Declínio e Revival:</strong></summary>

- Com o advento dos gráficos de alta resolução e a popularização da internet, a **ASCII Art** perdeu parte de sua relevância.
- No entanto, houve um renascimento nos últimos anos, com artistas digitais revisitando essa forma de expressão e criando novas obras usando caracteres ASCII.
</details>

7. **Aplicação no contexto do projeto: ArtAsciiCompress**
   - Perceba que **ASCII art** é uma forma de representar figuras gráficas por elementos textuais do padrão ASCII, os quais possuem densidadese visuais e capacidades representativas distintas. *Por exemplo*: caracteres como '#', '@', '*' e '.' podem ser usados para simular diferentes níveis de tonalidade entre clara, intermediária e escura.
   - Nesse sentido, ele presume uma relação de conversão de texturas e tonalidades para esses caracteres. Ou seja, um histograma de caracteres ASCII pode ser uma maneira intuitiva para representam as texturas e tonalidade da imagem.
   - Em compressores de imagem baseado na codificação de Huffman, está presente a geração dos histogramas para representar as distribuições de frequência. De modo semelhante, um dos objetivos do projeto é converter imagens para ASCII Art, o que será feita pela escala de cinza aplicada à imagem e, a partir daí, relacionada a caracteres que o representarão.

Em resumo, a **ASCII Art** é uma forma criativa e nostálgica de expressão visual que remonta aos primórdios da computação e continua a inspirar artistas e entusiastas até hoje.

## Código de Huffman

O **algoritmo de Huffman** é um método de **compressão de dados sem perdas** que otimiza o espaço usando **códigos variáveis** baseados na frequência dos caracteres. Ele oferece insights valiosos em análise de frequência e otimização de algoritmos, com aplicações além da compressão de dados.

### Premissa do Algoritmo de Huffman

A ideia fundamental do **algoritmo de Huffman** é usar **códigos curtos** para os caracteres que ocorrem com **maior frequência** e deixar os códigos mais longos para os caracteres mais raros. Esses códigos são, portanto, de **comprimento variável**. A escolha da melhor tabela de códigos é o segredo do algoritmo de Huffman.

### Definição e Corretude do Algoritimo
<details>
<summary>Definição</summary>
 
Códigos *livres de prefixo* são aqueles onde, dados dois caracteres quaisquer $i$ e $j$ representados pela codificação, a sequência de bits associadas a $i$ **não** é um *prefixo* da sequência associada a $j$. Em outras palavras, não há nenhuma sequência de bits que seja um prefixo de outra sequência no código.

**_Note_**: Sempre há uma solução ótima do problema da codificação que é dado por um código *livre de prefixo*.

<details>
 <summary>Dem.</summary>
    - Suponha um conjunto de caracteres $C = {c_1, c_2, \ldots, c_n}$ que precisam ser codificados. Assim, objetiva-se encontrar um código livre de prefixo para esses caracteres. Além disso, seja $L$ o comprimento médio do código, o qual queremos minimizar.
    - Suponha que temos dois caracteres i e j no código ótimo, onde a sequência de bits associada a i é um prefixo da sequência associada a j.
    - Agora, trocaremos as sequências de bits associadas a i e j. Ou seja, atribuiremos a sequência de bits originalmente associada a j a i e vice-versa.
    - Essa troca não viola a propriedade de prefixo, pois agora a sequência de bits originalmente associada a i não é mais um prefixo da sequência associada a j.
    - Além disso, o comprimento médio do código após a troca não será maior do que o comprimento médio original, pois estamos apenas trocando sequências de bits sem alterar seus comprimentos individuais.
    - Portanto, após essa troca, obtemos um código com comprimento médio menor ou igual ao código original, mas que é livre de prefixo.
    - Repetindo esse processo para todos os pares de caracteres onde a sequência de bits de um é um prefixo da sequência do outro, eventualmente obteremos um código livre de prefixo com comprimento médio igual ou menor do que o código original.
    - Assim, sempre existe uma solução ótima para o problema da codificação que é dada por um código livre de prefixo.
</details>
</details>
<details>
 <summary>Corretude</summary>

 1. **Codificação de Huffman**:
   - O algoritmo de Huffman constrói uma árvore binária de códigos de prefixo, onde os códigos são atribuídos com base nas frequências dos símbolos.
   - A árvore de Huffman é construída de forma a minimizar o comprimento médio de bits por símbolo.
   - Ideia do algoritimo de Huffman:
     - Começar com $|C|$ folhas e realizar sequencialmente  $|C| - 1$ operações de "intercalação" de dois vertices da árvore. Cada uma destas intercalações dá origem a um novo vértice interno que será o **pai** dos vertices que participarem da intercalação.
     - A escolha do par de vertices que dará origem a intercalação em cada passo depende da soma das frequências das folhas das subárvores com raizes nos vertices que ainda não participaram de intercalações.

2. **Tamanho do arquivo comprimido**
Se $T$ é a árvore que representa a codificação, $d_T(c)$ é a profundidade da folha representando o caracter $c$ e $f(c)$ é a sua frequência, o tamanho do arquivo comprimido será:

$$B(T) = \sum_{c \in C} f(c) \ d_T(c) \ \ .$$

- $B(T)$ é o custo da árvore T, extamente o tamanho do arquivo codificado.

3. **Lema 1 (escolha ambiciosa)**

Seja $C$ um alfabeto onde cada caracter $c \in C$ tem frequência $f[c]$. Sejam $x$ e $y$ dois caracteres em $C$ com as menores frequências. Então, existe um código ótimo livre de prefixo para $C$ no qual os códigos para $x$ e $y$ tem o mesmo comprimento e diferem apenas no último bit.

4. **Lema 2 (subestrutura ótima)**

Suponha $C$ um alfabeto com frequência $f[c]$ definida para cada caracter $c \in C$. Sejam $x$ e $y$ dois caracteres de $C$ com as menores frequências. Além disso, seja $C'$ o alfabeto obtido pela remoção de $x$ e $y$ e pela inclusão de um novo caracter $z$; logo, $C' = C \cup (z) - (x, y)$. As frequências dos caracteres em $C' \cap C$ são as mesmas que em $C$, e $f[z]$ é definida como sendo $f[z] = f[x] + f[y]$.

Seja $T'$ uma árvore binária representando um código ótimo, livre de prefixo para $C'$. Então, a árvore binária $T$ obtida de $T'$ substituindo-se o vertice (folha) $z$ por um vertice interno tendo $x$ e $y$ como filhos, representa um código ótimo livre de prefixo para $C$.

5. **Teorema**

A partir do *Lema 1* e do *Lema 2*, percebe-se que o conjunto de escolhas ambiciosas realmente constroi um algoritimo ótimo (livre de prefixos) e, portanto, o algoritimo de codificação de Huffman é ótimo.
</details>

### Considerações e Restrições
  - O algoritmo de Huffman pode ser aplicado a imagens, mas tem limitações.
  - Ele não leva em consideração a relação espacial entre pixels vizinhos, o que outros algoritmos (como JPEG) fazem.
  - O algoritimo de Huffman é minima, no sentido: nenhuma outra cadeia produzida por um código livre de prefixos é mais curtas que a cadeia produzida pelo código de Huffman, pois ela ajusta com o mínimo necessário para representar dado um conjunto de frequências.

## Screenshots
![Captura de tela 2024-07-30 212914](https://github.com/user-attachments/assets/771a2785-15cc-46ad-a031-4a0a733b754b)

![Captura de tela 2024-07-30 212938](https://github.com/user-attachments/assets/e93d2228-5183-4a0b-82d8-142dce5b63bd)

![Captura de tela 2024-07-30 003424](https://github.com/user-attachments/assets/22c8238a-aced-478f-bbfe-e6aa59c3f52c)

![Captura de tela 2024-07-30 003443](https://github.com/user-attachments/assets/5f853482-0efe-4c01-95c5-670f382c9d95)

![Captura de tela 2024-07-30 003503](https://github.com/user-attachments/assets/d2c5e7e0-e022-4f8a-86d9-5a9a99bdc215)
**Paea descodificação são necessário dois arquivos o arquivo.bin e o arquivo.tree
![Captura de tela 2024-07-30 003517](https://github.com/user-attachments/assets/b61a54af-b9b8-411b-9625-c49feefd511d)

![Captura de tela 2024-07-30 003542](https://github.com/user-attachments/assets/beed1259-9a09-4dd7-ab2f-340c5d7a1e2d)

![Captura de tela 2024-07-30 003554](https://github.com/user-attachments/assets/f6ad58a7-e2ab-474c-8bb1-80acaa42e4c7)
## Instalação 
**Linguagem**: Python<br>

**Bibliotecas**:<br>
    - pip install pillow
    <br>
    - pip install numpy

### Requisitos

## Uso 
Explique como usar seu projeto caso haja algum passo a passo após o comando de execução.

## Outros 
Quaisquer outras informações sobre seu projeto podem ser descritas abaixo.

[Link para o vídeo de apresentação do projeto](https://youtu.be/FyiUfEFkPuY).




