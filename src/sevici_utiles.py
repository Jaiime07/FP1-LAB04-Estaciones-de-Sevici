from collections import namedtuple

EstacionSevici = namedtuple("EstacionSevici", 
    "nombre, direccion, latitud, longitud, capacidad, puestos_libres, bicicletas_disponibles")

def selecciona_color(estacion:EstacionSevici) -> str:
    """
    Devuelve el color en que debe pintarse cada estación según su disponibilidad.

    Parámetros:
    estacion: EstacionSevici

    Devuelve:
    str: "green", "orange", "red" o "gray"
    """
    if estacion.capacidad == 0: #evitamos la división entre 0, que da un error
        return "gray"
    d = estacion.bicicletas_disponibles / estacion.capacidad #disponibilidad de la estación
    if d >= 2/3:
        return "green"
    if d >= 1/3:
        return "orange"
    if d > 0:
        return "red"
    
def calcula_estadisticas(estaciones: list[EstacionSevici]) -> tuple[int, int, float, int]:
    """
    Calcula estadísticas de las estaciones.
    Parametros:
    estaciones: lista de EstacionSevici
    Devuelve:
    tupla con (total de bicicletas libres, total de capacidad, porcentaje de ocupación, total de estaciones)
    """
    total_bicicletas_disponibles = 0
    total_capacidad = 0
    total_estaciones = 0
        
    for estacion in estaciones:
        total_bicicletas_disponibles += estacion.bicicletas_disponibles
        total_capacidad += estacion.capacidad
        total_estaciones += 1
   
    porcentaje_ocupacion = (1 - total_bicicletas_disponibles / total_capacidad) * 100
       
    return total_bicicletas_disponibles, total_capacidad, porcentaje_ocupacion, total_estaciones
    
    


def busca_estaciones_direccion(estaciones: list[EstacionSevici], direccion_parcial: str) -> list[EstacionSevici]:
    """
    Busca las estaciones que contengan en su dirección (subcadena, sin distinguir mayúsculas/minúsculas) la dirección parcial dada.    

    Parametros:
    estaciones: lista de EstacionSevici
    direccion_parcial: subcadena a buscar en la dirección de las estaciones

    Devuelve:
    lista de EstacionSevici que cumplen el criterio
    """
    estaciones_direccion_parcial = []
    for estacion in estaciones:
        if direccion_parcial.lower() in estacion.direccion.lower():
            estaciones_direccion_parcial.append(estacion)
    return estaciones_direccion_parcial
        

        
def busca_estaciones_con_disponibilidad(estaciones:list[EstacionSevici], min_disponibilidad: float = 0.5) -> list[EstacionSevici]:
    """
    Devuelve una lista de EstacionSevici con al menos el porcentaje mínimo de bicicletas disponible
    indicado.

    Parametros:
    estaciones: lista de EstacionSevici
    min_disponibilidad: porcentaje mínimo de bicicletas disponibles (0.0 a 1.0)
    
    Devuelve:
    lista de EstacionSevici
    """
    estaciones_buena_disponibilidad = []
    for estacion in estaciones:
        if estacion.capacidad !=0:
            porcentaje_ocupacion = estacion.bicicletas_disponibles / estacion.capacidad
            if porcentaje_ocupacion > min_disponibilidad:
                estaciones_buena_disponibilidad.append(estacion)
    return estaciones_buena_disponibilidad

def calcula_distancia(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """
    Calcula la distancia euclídea entre dos puntos (latitud, longitud).

    Parámetros:
    p1: tupla (latitud, longitud) del primer punto
    p2: tupla (latitud, longitud) del segundo punto

    Devuelve:
    float: distancia euclídea entre los dos puntos
    """
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**(1/2)

def busca_estacion_mas_cercana(estaciones:list[EstacionSevici], punto:tuple[float, float]) -> EstacionSevici | None:
    """
    Devuelve la estación más cercana al punto dado (latitud, longitud) que tenga al menos una bicicleta disponible.
    
    Parametros:
    estaciones: lista de EstacionSevici
    punto: tupla (latitud, longitud)

    Devuelve:
    EstacionSevici más cercana con al menos una bicicleta disponible, o None si no hay ninguna.
    """ 
    
    distancia_menor = 100000000000
    mas_cercana = None
    for estacion in estaciones:
        if estacion.bicicletas_disponibles > 0:
            distancia = calcula_distancia((estacion.latitud, estacion.longitud), (punto[0], punto[1]))
        
            if distancia < distancia_menor:
                distancia_menor = distancia
                mas_cercana = estacion
    return mas_cercana




def calcula_ruta(estaciones:list[EstacionSevici], origen:tuple[float, float], destino:tuple[float, float]) -> tuple[EstacionSevici | None, EstacionSevici | None]   :
    """
    Devuelve las estaciones más cercanas al punto de origen y destino dados, que tengan al menos una bicicleta disponible.

    Parametros: 
    estaciones: lista de EstacionSevici
    origen: tupla (latitud, longitud) del punto de origen
    destino: tupla (latitud, longitud) del punto de destino

    Devuelve:
    tupla con (estacion_origen, estacion_destino)
    """
    return  busca_estacion_mas_cercana(estaciones, origen), busca_estacion_mas_cercana(estaciones, destino)
    

