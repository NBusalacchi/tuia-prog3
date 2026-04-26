from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        
        # creamos la raiz
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)
        
        # diccionario de alcanzados
        reached = {}
        
        # frontera fifo para anchura
        frontera = QueueFrontier()
        
        # agregamos la raiz a la frontera y el estado inicial a los alcanzados
        frontera.add(root)
        reached[root.state] = True
        
        # comprobamos si el estado inicial es el optimo, en caso contrario continua
        if grid.objective_test(root.state):
            return Solution(root, reached)

        # iniciamos el bucle principal
        while True:
            # si la frontera esta vacia es porque no hay camino posible
            if frontera.is_empty():
                return NoSolution(reached)

            # sacamos el nodo mas viejo de la cola
            n = frontera.remove()

            # exploramos todos los movimientos permitidos desde ese nodo
            for a in grid.actions(n.state):
                # calculamos en que casilla caemos tras movernos
                s = grid.result(n.state, a)

                # si es una casilla por la que nunca pasamos
                if s not in reached:
                    # armamos el nodo del hijo sumando el costo del paso
                    son = Node(
                        "",
                        state=s,
                        cost=n.cost + grid.individual_cost(n.state, a),
                        parent=n,
                        action=a,
                    )

                    # en anchura se pregunta si es la meta apenas se crea el nodo para ahorrar tiempo
                    if grid.objective_test(s):
                        return Solution(son, reached)

                    # lo guardamos en el diccionario para no volver a pasar por aca
                    reached[s] = True
                    # lo mandamos al fondo de la frontera
                    frontera.add(son)

        # por si se rompe el bucle
        return NoSolution(reached)