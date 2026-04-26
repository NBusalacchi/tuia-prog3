from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        
        # creamos la raiz
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)
        
        # diccionario de alcanzados para no ciclar
        reached = {}
        
        # frontera de cola de prioridad para a estrella
        frontera = PriorityQueueFrontier()

        # agregamos la raiz a la frontera usando f(n) = g(n) + h(n) 
        frontera.add(root, root.cost + grid.heuristic(root.state)) 

        # iniciamos el bucle principal
        while not frontera.is_empty():
            
            # sacamos el nodo con el menor costo total estimado
            n = frontera.pop()
            
            # comprobamos si llegamos al objetivo
            if grid.objective_test(n.state):
                return Solution(n, reached)

            # si ya habiamos visitado este estado lo salteamos
            if n.state in reached:
                continue
                
            # lo marcamos como visitado para no volver a procesarlo
            reached[n.state] = True

            # exploramos todos los movimientos permitidos desde ese nodo
            for a in grid.actions(n.state):
                # calculamos en que casilla caemos tras movernos
                s = grid.result(n.state, a)
                
                # si es una casilla por la que nunca pasamos
                if s not in reached:
                    # armamos el nodo del hijo 
                    son = Node(
                        "",
                        state=s,
                        cost=n.cost + grid.individual_cost(n.state, a), 
                        parent=n,
                        action=a,
                    )
                    
                    # calculamos f(n) sumando el costo real recorrido mas la heuristica(manhatan)
                    f_n = son.cost + grid.heuristic(s)
                    
                    # lo mandamos a la frontera con su valor total
                    frontera.add(son, f_n) 

        # por si se agota la frontera y no habia solucion posible
        return NoSolution(reached)
    