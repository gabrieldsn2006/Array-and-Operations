from collections import defaultdict
import sys

input = sys.stdin.readline

# -------------------------
# Ford-Fulkerson
# -------------------------

class Edge:
    def __init__(self, to, cap, rev):
        self.to = to
        self.cap = cap
        self.rev = rev


class MaxFlow:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, u, v, cap):
        fwd = Edge(v, cap, len(self.g[v]))
        rev = Edge(u, 0, len(self.g[u]))
        self.g[u].append(fwd)
        self.g[v].append(rev)

    def dfs(self, v, t, f, vis):
        if v == t:
            return f

        vis[v] = True

        for e in self.g[v]:
            if e.cap > 0 and not vis[e.to]:
                pushed = self.dfs(e.to, t, min(f, e.cap), vis)

                if pushed:
                    e.cap -= pushed
                    self.g[e.to][e.rev].cap += pushed
                    return pushed

        return 0

    def max_flow(self, s, t):
        flow = 0

        while True:
            vis = [False] * self.n
            pushed = self.dfs(s, t, float('inf'), vis)

            if pushed == 0:
                break

            flow += pushed

        return flow


# -------------------------
# Fatoração
# -------------------------

def factorize(x):
    factors = defaultdict(int)

    d = 2
    while d * d <= x:
        while x % d == 0:
            factors[d] += 1
            x //= d
        d += 1

    if x > 1:
        factors[x] += 1

    return factors


# -------------------------
# Leitura
# -------------------------

n, m = map(int, input().split())
a = list(map(int, input().split()))

pairs = []

for _ in range(m):
    u, v = map(int, input().split())

    # garantir:
    # u = índice ímpar
    # v = índice par
    if u % 2 == 0:
        u, v = v, u

    pairs.append((u - 1, v - 1))


# -------------------------
# Fatorar todos os números
# -------------------------

facts = [factorize(x) for x in a]

all_primes = set()

for f in facts:
    all_primes.update(f.keys())


# -------------------------
# Resolver primo por primo
# -------------------------

answer = 0
INF = 10**9

for p in all_primes:

    S = n
    T = n + 1

    mf = MaxFlow(n + 2)

    # source -> ímpares
    for i in range(n):
        if (i + 1) % 2 == 1:
            cnt = facts[i].get(p, 0)
            if cnt:
                mf.add_edge(S, i, cnt)

    # pares -> sink
    for i in range(n):
        if (i + 1) % 2 == 0:
            cnt = facts[i].get(p, 0)
            if cnt:
                mf.add_edge(i, T, cnt)

    # arestas permitidas
    for u, v in pairs:
        mf.add_edge(u, v, INF)

    answer += mf.max_flow(S, T)

print(answer)