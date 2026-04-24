from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        
        #creamos la Raiz
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)
        
        #Diccionario de Alcanzados
        reached = {}
        
        #Frontera
        frontera = QueueFrontier()
        
        #Agreamamos la raiz a la frontera y el estado inicial al los alcanzados
        frontera.add(root)
        reached[root.state] = True
        
        #Comprobamos si el estado inicial es el Optimo, en caso contrario continua
        if grid.objective_test(root.state):
            return Solution(root, reached)

        while True:
            if frontera.is_empty():
                return NoSolution(reached)

            n = frontera.remove()

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

                    if grid.objective_test(s):
                        return Solution(son, reached)

                    reached[s] = True
                    frontera.add(son)

        return NoSolution(reached)