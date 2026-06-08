
---

# Atividade de Acompanhamento

**Universidade de Fortaleza (UNIFOR)**   
**Disciplina:** Resolução de Problemas com Grafos   
**Professor:** Ricardo Carubbi   
**Grupo D:** Victor Lins, Gabriel de Sousa e Lorenzo Barros   
**Problema:** Codeforces 498C (Array and Operations)   

### 1. Resumo do problema

Temos um array de $n$ números inteiros positivos e uma lista com $m$ pares de índices válidos. A regra para um par $(i, j)$ ser válido é que a soma $i + j$ seja um número ímpar.

O que podemos fazer em uma operação é pegar um desses pares válidos e dividir ambos os números do par por um divisor comum maior que 1. Nosso objetivo é maximizar o número total de operações. Para conseguir o número máximo absoluto de divisões, nunca devemos dividir por números compostos. É muito melhor dividir por fatores primos. Portanto, o problema quer saber, no fundo, qual é a quantidade máxima de fatores primos em comum que conseguimos parear e cancelar usando as arestas permitidas.

### 2. Interpretação da Entrada e da Saída

Na entrada, vamos ler $n$ e $m$. Depois lemos o array de tamanho $n$. Por fim, lemos as $m$ linhas que indicam as conexões válidas.

A chave da entrada está na regra "$i+j$ é ímpar". Para a soma de dois inteiros ser ímpar, obrigatoriamente um precisa ser par e o outro precisa ser ímpar. Isso divide todos os índices em dois conjuntos isolados. Isso indica que a estrutura é um grafo bipartido.

A saída será apenas um único número inteiro. Esse número será exatamente o valor do nosso fluxo máximo encontrado na rede, que representa o número de operações.

### 3. Modelagem da rede de fluxo

Vamos modelar isso como um problema de fluxo em um grafo bipartido conectando fatores primos idênticos.

* **Vértices:** Além de uma Origem ($S$) e um Sorvedouro ($T$), não vamos usar os números inteiros como vértices, mas sim a fatoração deles. Se o número na posição 2 for 12, ele é $2^2 \times 3^1$. Então criaremos um vértice para o "primo 2 do índice 2" e outro para o "primo 3 do índice 2".
* **Conjuntos Bipartidos:** Do lado esquerdo da rede, colocamos os vértices derivados dos índices pares originais. Do lado direito, colocamos os vértices dos índices ímpares.
* **Arestas da Origem ($S$) para a Esquerda:** Criamos arestas direcionadas de $S$ para todos os nós do conjunto da esquerda. A capacidade de cada aresta será o expoente daquele primo.
* **Arestas do Meio (Pares válidos):** Para cada par $(i, j)$ lido na entrada, ligamos do nó do índice par para o nó do índice ímpar. A direção do caminho aqui vai ser explicitamente de $u$ até $v$. Conectamos apenas vértices que representam o mesmo número primo. A capacidade aqui colocamos como infinita, pois o que realmente limita a operação é a quantidade de primos em $S$ e $T$.
* **Arestas da Direita para o Sorvedouro ($T$):** Criamos arestas direcionadas dos nós ímpares para $T$. A capacidade será o expoente daquele primo do lado direito.

### 4. Justificativa: Ford-Fulkerson ou Edmonds-Karp

Nós vamos implementar o Edmonds-Karp. O Ford-Fulkerson com DFS puro até passaria nesse problema porque o fluxo máximo é pequeno (como os números vão até $10^9$, o expoente máximo de um primo não passa da casa dos 30, então o fluxo não cresce muito). Porém, usar o Edmonds-Karp com BFS garante sempre encontrar o caminho aumentante mais curto, nos livra de casos degenerados de pior cenário e deixa o tempo de execução previsível, permitindo que o código não ultrapasse o limite de tempo na plataforma.

### 5. Instância pequena para teste

Vamos resolver manualmente o segundo caso de teste de exemplo do próprio enunciado do Codeforces.

* $n = 3$, $m = 2$
* Array: $[8, 12, 8]$
* Pares válidos: $(1, 2)$ e $(2, 3)$

Fatorando e separando os índices em Par e Ímpar:

* Índice 1 (Ímpar): $a[1] = 8 = 2^3$. Vértice gerado: $(1, \text{primo } 2)$
* Índice 2 (Par): $a[2] = 12 = 2^2 \times 3^1$. Vértices: $(2, \text{primo } 2)$ e $(2, \text{primo } 3)$
* Índice 3 (Ímpar): $a[3] = 8 = 2^3$. Vértice gerado: $(3, \text{primo } 2)$

### 6. Execução manual passo a passo

Primeiro, montamos as capacidades das arestas da rede:

1. $S \to (2, \text{primo } 2)$ com capacidade 2
2. $S \to (2, \text{primo } 3)$ com capacidade 1
3. Aresta do par $(1, 2)$: $(2, \text{primo } 2) \to (1, \text{primo } 2)$ com capacidade $\infty$
4. Aresta do par $(2, 3)$: $(2, \text{primo } 2) \to (3, \text{primo } 2)$ com capacidade $\infty$
5. $(1, \text{primo } 2) \to T$ com capacidade 3
6. $(3, \text{primo } 2) \to T$ com capacidade 3    
*Observação: O fator primo 3 do índice 2 não se conecta com ninguém, pois não tem nenhum fator 3 do lado ímpar.*

Agora rodando a busca (BFS) por caminhos aumentantes:

* **Primeira Iteração:** A BFS acha o caminho $S \to (2, \text{primo } 2) \to (1, \text{primo } 2) \to T$.
* **Gargalo:** O menor valor nesse caminho é o mínimo entre $(2, \infty, 3)$, que resulta em 2.
* **Atualizando o Residual:** O fluxo de 2 passa. A capacidade da aresta saindo de $S$ para $(2, \text{primo } 2)$ zera. A aresta reversa ganha capacidade 2. A capacidade do $(1, \text{primo } 2) \to T$ cai para 1.
* **Segunda Iteração:** A BFS tenta buscar outro caminho. O nó $(2, \text{primo } 2)$ não pode mais receber fluxo de $S$. O único nó que ainda tem capacidade vindo de $S$ é o $(2, \text{primo } 3)$, mas as arestas que saem dele não levam a lugar nenhum. A BFS não alcança $T$.
* O algoritmo para aqui.

### 7. Verificação da resposta final

O valor final do fluxo acumulado na nossa execução manual foi 2. A resposta esperada pelo Codeforces para esse caso é exatamente 2.

Neste problema, o valor direto do fluxo máximo capacitado já é a resposta bruta final. Não precisaremos fazer DFS no grafo residual para achar o corte mínimo, nem rastrear quais arestas ficaram com fluxo positivo para reconstruir rotas. Assim que o Edmonds-Karp terminar de rodar, basta imprimir o valor do fluxo.