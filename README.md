# Codeforces 498C - Array and Operations

**Link do Problema:** [https://codeforces.com/problemset/problem/498/C](https://codeforces.com/problemset/problem/498/C)

**Integrantes do Grupo:**
- Victor Lins
- Gabriel de Sousa
- Lorenzo Barros

**Linguagem Utilizada:** Python

## Como Executar

A partir da raiz do projeto, você pode enviar o arquivo de texto com os casos de teste direto para o código através do redirecionamento no terminal:

```bash
# No Linux/Mac ou no Prompt de Comando (Windows):
python src/main.py < dados/entradas_do_problema.txt

# No PowerShell (Windows):
Get-Content dados\entradas_do_problema.txt | python src\main.py
ou
cat dados\entradas_do_problema.txt | python src\main.py
```

## Modelagem da Rede de Fluxo

A solução foi modelada como um problema de fluxo máximo em um grafo bipartido. A chave do problema é maximizar divisões por fatores em comum. Por isso, não usamos os números inteiros do array original como vértices da rede, mas sim os seus **fatores primos**. O fato de a regra de pareamento exigir que a soma dos índices $i + j$ seja ímpar divide naturalmente os índices disponíveis em dois conjuntos: pares e ímpares.

### Definição de Origem, Sorvedouro, Vértices, Arestas e Capacidades

- **Vértices da Rede:** Cada fator primo presente na fatoração de um número do array se torna um vértice único.
- **Origem (S):** Vértice `0`. 
- **Sorvedouro (T):** Vértice `1`. 
- **Arestas e Capacidades:**
  - **De $S$ para índices Pares:** Criamos arestas direcionadas da Origem para os vértices derivados de índices pares. A capacidade da aresta é igual ao expoente desse fator primo.
  - **De Índices Ímpares para $T$:** Criamos arestas direcionadas dos vértices ímpares para o Sorvedouro. A capacidade também é igual ao expoente do fator primo do lado direito.
  - **Entre pares válidos (Meio da rede):** Conectamos o vértice do índice Par ao vértice do índice Ímpar caso eles representem o mesmo fator primo. A capacidade aqui é infinita (`INF = 10**15`), pois o gargalo de divisões possíveis é natural e estruturalmente ditado pelas capacidades nas extremidades da rede (Origem e Sorvedouro).

## Algoritmo Utilizado


Foi utilizado o algoritmo de **Edmonds-Karp** para encontrar o fluxo máximo. Essa abordagem foi preferida no lugar do Ford-Fulkerson com DFS para garantir a localização do caminho aumentante mais curto a cada iteração (usando BFS). Isso nos livra de casos degenerados de pior cenário e deixa o tempo de execução previsível, prevenindo o risco de *Time Limit Exceeded* (TLE).

### O Papel do Grafo Residual


A cada caminho aumentante encontrado do Source ao Sink pela nossa BFS, o fluxo daquele caminho restringe a capacidade das arestas diretas na mesma proporção em que aumenta a capacidade em arestas reversas. Isso permite ao algoritmo "desfazer" ou "redirecionar" rotas alocadas previamente se houver um caminho que otimize o fluxo total ao final.

### Conversão do Fluxo na Resposta


O valor direto do fluxo máximo capacitado que atinge o Sorvedouro equivale exatamente ao número máximo absoluto de operações possíveis. Portanto, assim que a rede esgota os caminhos aumentantes, nós apenas imprimimos a soma de todos os fluxos parciais obtidos, sem a necessidade de processamentos adicionais.

## Análise de Complexidade

> *[PLACEHOLDER: Descrever a complexidade do algoritmo para o Edmonds-Karp, como ele se traduz com V e E neste problema de fatores primos e citar qual a estrutura mais ocupou memória (dicionários do grafo/capacidades).]*

## Casos Especiais Relevantes

> *[PLACEHOLDER: Discutir casos em que não há pares válidos formando conexões, cenários com max_flow == 0 na primeira rodada e o cuidado para evitar estouro numérico nas capacidades da aresta infinita (10**15).]*

## Comprovação de Accepted

![Accepted](evidencias/accepted.png)
