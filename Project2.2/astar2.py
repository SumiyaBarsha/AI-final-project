import heapq

def heuristic(point, goal):
    return abs(point[0] - goal[0]) + abs(point[1] - goal[1])

def astar(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x, y = current[0] + dx, current[1] + dy
            neighbor = (x, y)
            tentative_g = g_score[current] + 1
            
            if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0:
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))
                    came_from[neighbor] = current
    
    return None
