import sys
from collections import deque

def solve():
    # Read all input from standard input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    m = int(input_data[1])
    
    a = [0] * (n + 1)
    for i in range(1, n + 1):
        a[i] = int(input_data[1 + i])
        
    pairs = []
    idx = 2 + n
    for _ in range(m):
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        idx += 2
        pairs.append((u, v))
        
    # Extract prime factors for each number a[i]
    factors_list = [{} for _ in range(n + 1)]
    for i in range(1, n + 1):
        x = a[i]
        d = 2
        if x % d == 0:
            count = 0
            while x % d == 0:
                count += 1
                x //= d
            factors_list[i][d] = count
        d = 3
        while d * d <= x:
            if x % d == 0:
                count = 0
                while x % d == 0:
                    count += 1
                    x //= d
                factors_list[i][d] = count
            d += 2
        if x > 1:
            factors_list[i][x] = 1

    # Map each (index, prime) to a unique node ID
    node_id = 2
    node_map = {}
    for i in range(1, n + 1):
        for p in factors_list[i]:
            node_map[(i, p)] = node_id
            node_id += 1
            
    num_nodes = node_id
    graph = [{} for _ in range(num_nodes)]
    
    def add_edge(u, v, cap):
        if v not in graph[u]:
            graph[u][v] = 0
            graph[v][u] = 0
        graph[u][v] += cap
        
    # Source is 0, Sink is 1
    # Even indices connect from Source, Odd indices connect to Sink
    for i in range(1, n + 1):
        for p, count in factors_list[i].items():
            u = node_map[(i, p)]
            if i % 2 == 0:
                add_edge(0, u, count)
            else:
                add_edge(u, 1, count)
                
    INF = 10**15
    for u, v in pairs:
        # Ensure u is the even index, v is the odd index
        if u % 2 != 0:
            u, v = v, u 
        
        common_primes = set(factors_list[u].keys()).intersection(set(factors_list[v].keys()))
        for p in common_primes:
            node_u = node_map[(u, p)]
            node_v = node_map[(v, p)]
            add_edge(node_u, node_v, INF)

    graph = [{} for _ in range(num_nodes)]     
    
    def bfs():
        parent = [-1] * num_nodes
        parent[0] = -2
        q = deque([(0, INF)])
        
        while q:
            u, flow = q.popleft()
            
            for v, cap in graph[u].items():
                if parent[v] == -1 and cap > 0:
                    parent[v] = u
                    new_flow = min(flow, cap)
                    if v == 1:
                        return new_flow, parent
                    q.append((v, new_flow))
        return 0, parent

    max_flow = 0
    while True:
        flow, parent = bfs()
        if flow == 0:
            break
            
        max_flow += flow
        
        # Update residual capacities along the path
        curr = 1
        while curr != 0:
            prev = parent[curr]
            graph[prev][curr] -= flow
            graph[curr][prev] += flow
            curr = prev
            
    print(max_flow)

if __name__ == '__main__':
    solve()
