db = {
    1: {"nombre": "Ana", "edad": 25, "ciudad": "Madrid"},
    2: {"nombre": "Carlos", "edad": 30, "ciudad": "Barcelona"},
    3: {"nombre": "Elena", "edad": 28, "ciudad": "Valencia"},
}

def BusquedaSecuencial (db, id_clave):
    for id, registros in db.items():
        if (id == id_clave):
            return registros

def busqueda_binaria_recursiva(db, id_clave, izq, der):
    if izq > der:
        return None  

    mid = (izq + der) // 2  
    clave_mid, datos = list(db.items())[mid] 

    if clave_mid == id_clave:
        return datos 

    elif clave_mid < id_clave:
        return busqueda_binaria_recursiva(db, id_clave, mid + 1, der)  
    else:
        return busqueda_binaria_recursiva(db, id_clave, izq, mid - 1)

def busqueda_hash(db, id_clave):
    return db.get(id_clave, None)  