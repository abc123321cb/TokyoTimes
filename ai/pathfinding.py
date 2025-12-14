import heapq

class Pathfinding:
    def __init__(self, cell_size: int = 20):
        self.cell = cell_size

    def _heuristic(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def astar(self, walkable_fn, start, goal, bounds):
        """
        A* over a grid. walkable_fn(x, y) -> bool for center of NPC hitbox.
        start, goal are world coords (pixels). bounds=(w,h).
        Returns list of world positions (pixels) for centers to follow.
        """
        cell = self.cell
        w, h = bounds

        def to_cell(p):
            return (int(p[0]//cell), int(p[1]//cell))
        def to_world(c):
            return (c[0]*cell + cell//2, c[1]*cell + cell//2)

        start_c = to_cell(start)
        goal_c = to_cell(goal)

        open_set = []
        heapq.heappush(open_set, (0, start_c))
        came_from = {}
        gscore = {start_c: 0}

        def neighbors(c):
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx, ny = c[0]+dx, c[1]+dy
                wx, wy = to_world((nx, ny))
                if 0 <= wx < w and 0 <= wy < h and walkable_fn(wx, wy):
                    yield (nx, ny)

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal_c:
                # reconstruct
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return [to_world(c) for c in path]
            for nb in neighbors(current):
                tentative = gscore[current] + 1
                if nb not in gscore or tentative < gscore[nb]:
                    came_from[nb] = current
                    gscore[nb] = tentative
                    f = tentative + self._heuristic(nb, goal_c)
                    heapq.heappush(open_set, (f, nb))
        return []
