from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        
        # creamos la raiz
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)
        
        # diccionario de alcanzados que guarda el menor costo encontrado para cada estado
        reached = {root.state: 0} 
        
        # frontera de cola de prioridad para costo uniforme
        frontera = PriorityQueueFrontier()

        # agregamos la raiz a la frontera usando solo su costo acumulado ( 0)
        frontera.add(root, root.cost)

        # iniciamos el bucle principal
        while not frontera.is_empty():
            
            # sacamos el nodo con el menor costo acumulado total
            n = frontera.pop()

            # comprobamos si llegamos al objetivo
            if grid.objective_test(n.state):
                return Solution(n, reached)

            # exploramos todos los movimientos permitidos desde ese nodo
            for a in grid.actions(n.state):
                # calculamos en que casilla caemos tras movernos
                s = grid.result(n.state, a)
                
                # calculamos el costo de llegar a esta nueva casilla
                nuevo_costo = n.cost + grid.individual_cost(n.state, a)

                # si nunca pasamos por aca o encontramos un camino mas barato al mismo estado
                if s not in reached or nuevo_costo < reached[s]:
                    # armamos el nodo del hijo 
                    son = Node(
                        "",
                        state=s,
                        cost=nuevo_costo,
                        parent=n,
                        action=a,
                    )
                    
                    # actualizamos el diccionario con el costo mas barato para esta casilla
                    reached[s] = nuevo_costo 
                    
                    # lo mandamos a la frontera ordenado por su costo real acumulado
                    frontera.add(son, son.cost)

        # por si se agota la frontera y no habia solucion posible
        return NoSolution(reached)