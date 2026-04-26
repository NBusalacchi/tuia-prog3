"""
Módulo de estrategias para el juego del Tateti

Este módulo contiene las estrategias para elegir la acción a realizar.
Los alumnos deben implementar la estrategia minimax.

Por defecto, se incluye una estrategia aleatoria como ejemplo base.
"""

import random
from typing import List, Tuple
from tateti import Tateti, JUGADOR_MAX, JUGADOR_MIN

def estrategia_aleatoria(tateti: Tateti, estado: List[List[str]]) -> Tuple[int, int]:
    """
    Estrategia aleatoria: elige una acción al azar entre las disponibles.
  
    Args:
        tateti: Instancia de la clase Tateti
        estado: Estado actual del tablero
        
    Returns:
        Tuple[int, int]: Acción elegida (fila, columna)

    Raises:
        ValueError: Si no hay acciones disponibles
    """
    acciones_disponibles = tateti.acciones(estado)
    if not acciones_disponibles:
        raise ValueError("No hay acciones disponibles")
    
    return random.choice(acciones_disponibles)

def valor_maximo(tateti: Tateti, estado: List[List[str]]) -> float:
    """calcula el valor maximo para el nodo MAX."""
    # cortamos la recursión si es un estado final 
    if tateti.test_terminal(estado):
        return tateti.utilidad(estado, JUGADOR_MAX)
    
    v = -float('inf') # arranco en -infinito para ir buscando el maximo
    
    # pruebo todas las jugadas posibles desde este estado
    for accion in tateti.acciones(estado):
        # simulo la jugada y le paso el turno a MIN. me quedo con el valro mas alto
        v = max(v, valor_minimo(tateti, tateti.resultado(estado, accion)))
        
    return v


def valor_minimo(tateti: Tateti, estado: List[List[str]]) -> float:
    """calcula el valor minimo para el nodo MIN."""
    # cortamos la recursion si es un estado final
    if tateti.test_terminal(estado):
        return tateti.utilidad(estado, JUGADOR_MAX)
    
    v = float('inf') # arranco en infinito para ir buscando el minimo
    
    for accion in tateti.acciones(estado):
        # Simulo la jugada y le devuelvo el turno a MAX. mr quedo con el mas pequeño
        v = min(v, valor_maximo(tateti, tateti.resultado(estado, accion)))
        
    return v


def estrategia_minimax(tateti: Tateti, estado: List[List[str]]) -> Tuple[int, int]:
    # quien juega y que movimientos se pueden hacer
    jugador_actual = tateti.jugador(estado)
    acciones_posibles = tateti.acciones(estado)
    
    # en caso de que no se pueda hacer nada
    if not acciones_posibles:
        return None

    # logica para MAX 
    if jugador_actual == JUGADOR_MAX:
        mejor_valor = -float('inf')
        mejor_accion = None
        
        # evaluo las jugadas reales y elijo la que retorne mejor puntaje
        for accion in acciones_posibles:
            valor = valor_minimo(tateti, tateti.resultado(estado, accion))
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_accion = accion
                
        return mejor_accion

    # Lógica para MIN 
    else:
        mejor_valor = float('inf')
        mejor_accion = None
        
        # Lo mismo, pero me quedo con la jugada que devuelva el menor puntaje
        for accion in acciones_posibles:
            valor = valor_maximo(tateti, tateti.resultado(estado, accion))
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_accion = accion
                
        return mejor_accion