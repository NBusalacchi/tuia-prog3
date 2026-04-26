from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        
        # creamos la raiz
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # frontera lifo para profundidad
        frontera = StackFrontier()
        
        # agregamos la raiz a la frontera
        frontera.add(root)

        # diccionario de expandidos para no ciclar
        expanded = dict()

        # comprobamos si el estado inicial es el optimo
        if grid.objective_test(root.state):
            return Solution(root, expanded)

        # iniciamos el bucle principal
        while True:
            # si la pila esta vacia es porque no hay camino posible
            if frontera.is_empty():
                return NoSolution(expanded)

            # sacamos el ultimo nodo que entro a la pila
            n = frontera.remove()

            # si ya habiamos expandido este nodo lo salteamos
            if n.state in expanded:
                continue

            # lo marcamos como expandido para no volver a analizarlo
            expanded[n.state] = True

            # exploramos todos los movimientos permitidos desde ese nodo
            for a in grid.actions(n.state):
                # calculamos en que casilla caemos tras movernos
                s = grid.result(n.state, a)

                # si es una casilla por la que nunca expandimos
                if s not in expanded:
                    # armamos el nodo del hijo
                    son = Node(
                        "",
                        state=s,
                        cost=n.cost + grid.individual_cost(n.state, a),
                        parent=n,
                        action=a,
                    )

                    # preguntamos si es la meta el hijo
                    if grid.objective_test(s):
                        return Solution(son, expanded)

                    # lo mandamos al tope de la pila de la frontera
                    frontera.add(son)

        # por si se rompe el bucle
        return NoSolution(expanded)