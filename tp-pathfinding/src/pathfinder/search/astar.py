from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:

        root = Node("", state=grid.initial, cost=0, parent=None, action=None)
        reached = {}
        frontera = PriorityQueueFrontier()

        frontera.add(root, root.cost + grid.heuristic(root.state)) 

        while not frontera.is_empty():
            n = frontera.pop()
            
            
            if grid.objective_test(n.state):
                return Solution(n, reached)

            if n.state in reached:
                continue
            reached[n.state] = True

            # Expansión de hijos
            for a in grid.actions(n.state):
                s = grid.result(n.state, a)
                
                if s not in reached:
                    son = Node(
                        "",
                        state=s,
                        cost=n.cost + grid.individual_cost(n.state, a), 
                        parent=n,
                        action=a,
                    )
                    
                    
                    f_n = son.cost + grid.heuristic(s)
                    frontera.add(son, f_n) 

        return NoSolution(reached)