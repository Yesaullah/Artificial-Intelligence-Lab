from collections import defaultdict, deque
import heapq

class RomaniaMap:
    def __init__(self):
        self.graph = {
            'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
            'Zerind': {'Arad': 75, 'Oradea': 71},
            'Oradea': {'Zerind': 71, 'Sibiu': 151},
            'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
            'Timisoara': {'Arad': 118, 'Lugoj': 111},
            'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
            'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
            'Drobeta': {'Mehadia': 75, 'Craiova': 120},
            'Craiova': {'Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
            'Rimnicu Vilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
            'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
            'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
            'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
            'Giurgiu': {'Bucharest': 90},
            'Urziceni': {'Bucharest': 85, 'Vaslui': 142, 'Hirsova': 98},
            'Hirsova': {'Urziceni': 98, 'Eforie': 86},
            'Eforie': {'Hirsova': 86},
            'Vaslui': {'Urziceni': 142, 'Iasi': 92},
            'Iasi': {'Vaslui': 92, 'Neamt': 87},
            'Neamt': {'Iasi': 87}
        }
        self.heuristic = {
            'Arad': 366, 'Bucharest': 0, 'Craiova': 160,
            'Drobeta': 242, 'Eforie': 161, 'Fagaras': 176,
            'Giurgiu': 77, 'Hirsova': 151, 'Iasi': 226,
            'Lugoj': 244, 'Mehadia': 241, 'Neamt': 234,
            'Oradea': 380, 'Pitesti': 100, 'Rimnicu Vilcea': 193,
            'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80,
            'Vaslui': 199, 'Zerind': 374
        }
    def bfs(self, start, goal):
        visited = set()
        q = deque([(start, [start], 0)])
        
        while q:
            current, path, cost = q.popleft()
            
            if current == goal:
                return path, cost
                
            if current not in visited:
                visited.add(current)
                for neighbor in self.graph[current]:
                    if neighbor not in visited:
                        new_cost = cost + self.graph[current][neighbor]
                        q.append((neighbor, path + [neighbor], new_cost))
        
        return None, 0

    def ucs(self, start, goal):
        visited = set()
        pq = [(0, start, [start])]
        
        while pq:
            cost, current, path = heapq.heappop(pq)
            
            if current == goal:
                return path, cost
                
            if current not in visited:
                visited.add(current)
                for neighbor in self.graph[current]:
                    if neighbor not in visited:
                        new_cost = cost + self.graph[current][neighbor]
                        heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))
        
        return None, 0

    def gbfs(self, start, goal):
        """Greedy Best First Search"""
        visited = set()
        pq = [(self.heuristic[start], start, [start], 0)]
        
        while pq:
            _, current, path, cost = heapq.heappop(pq)
            
            if current == goal:
                return path, cost
                
            if current not in visited:
                visited.add(current)
                for neighbor in self.graph[current]:
                    if neighbor not in visited:
                        new_cost = cost + self.graph[current][neighbor]
                        heapq.heappush(pq, 
                                     (self.heuristic[neighbor], neighbor, path + [neighbor], new_cost))
        
        return None, 0

    def iddfs(self, start, goal):
        def dfs(node, goal, depth, path, cost):
            if depth < 0:
                return None, 0
            if node == goal:
                return path, cost
            
            for neighbor in self.graph[node]:
                new_cost = cost + self.graph[node][neighbor]
                result, final_cost = dfs(neighbor, goal, depth - 1, 
                                       path + [neighbor], new_cost)
                if result is not None:
                    return result, final_cost
            return None, 0

        for depth in range(50): 
            result, cost = dfs(start, goal, depth, [start], 0)
            if result is not None:
                return result, cost
        return None, 0

def main():
    romania = RomaniaMap()
    
    start = input("Enter start city: ")
    goal = input("Enter destination city: ")
    
    results = []
    
    # running bfs algo
    path, cost = romania.bfs(start, goal)
    if path:
        results.append(("Breadth First Search", path, cost))
    
    # running ucs algo
    path, cost = romania.ucs(start, goal)
    if path:
        results.append(("Uniform Cost Search", path, cost))
    
    # running gbfs algo
    path, cost = romania.gbfs(start, goal)
    if path:
        results.append(("Greedy Best First Search", path, cost))
    
    # running iddfs algo
    path, cost = romania.iddfs(start, goal)
    if path:
        results.append(("Iterative Deepening DFS", path, cost))
    
    results.sort(key=lambda x: x[2])
    
    print("\nResults sorted by path cost:")
    for algorithm, path, cost in results:
        print(f"\n{algorithm}:")
        print(f"Path: {' -> '.join(path)}")
        print(f"Cost: {cost}")

if __name__ == "__main__":
    main()