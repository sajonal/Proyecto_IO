import numpy as np


print("Bienvienido a Esquina_NorOeste") 
print("Por favor ingrese el tamaño de la matriz de datos")
m = int(input("Ingrese el número de filas (orígenes): "))
n = int(input("Ingrese el número de columnas (destinos): "))
print("Ingrese los costos de transporte:")  # acá de vamos a iniciar a pedir datos al usuario 
costos = np.zeros((m, n)) # se define la matriz con la que se piensa trabajar 
for i in range(m):
    for j in range(n):
        costos[i][j] = float(input(f"Costo de transporte desde el origen {i+1} al destino {j+1}: ")) # ciclo recorre la matriz y pide los costos de transporte 
print("Ingrese las ofertas de cada origen:")


ofertas = np.zeros(m) # se asigna el tamaño del vector de ofertas 

for i in range(m):
    ofertas[i] = float(input(f"Oferta del origen {i+1}: ")) # ciclo que asigna las ofertas de cada origen 
print("Ingrese las demandas de cada destino:")

demandas = np.zeros(n) # se asigna el tamaño del vector de demandas 


for j in range(n):
    demandas[j] = float(input(f"Demanda del destino {j+1}: ")) # ciclo que asigna las demandas de cada destino



# Verificar si el problema está balanceado
if sum(ofertas) != sum(demandas):  #verifica si la suma de las ofertas es igual a la suma de las demandas 
    print("El problema no está balanceado. Ajustando ofertas y demandas...")
    if sum(ofertas) > sum(demandas):
        demandas = np.append(demandas, sum(ofertas) - sum(demandas)) # si la suma de las ofertas es mayor a la suma de las demandas, se agrega una demanda ficticia
        costos = np.hstack((costos, np.zeros((m, 1)))) # se agrega una columna de ceros a la matriz de costos
        n += 1
    else:
        ofertas = np.append(ofertas, sum(demandas) - sum(ofertas)) # si la suma de las demandas es mayor a la suma de las ofertas, se agrega una oferta ficticia
        costos = np.vstack((costos, np.zeros((1, n)))) # se agrega una fila de ceros a la matriz de costos
        m += 1
        
# Inicializar la matriz de asignaciones - acá se decice que costo se va a asignar a cada celda 
asignaciones = np.zeros((m, n))
i = 0
j = 0

while i < m and j < n:
    if ofertas[i] == 0:
        i += 1
        continue # si la oferta es cero, se pasa al siguiente origen 
    if demandas[j] == 0:
        j += 1
        continue # si la demanda es cero, se pasa al siguiente destino
    
    cantidad = min(ofertas[i], demandas[j]) # se asigna la cantidad mínima entre la oferta y la demanda por ejemplo si la oferta es 20 y la demanda es 30, se asigna 20
    asignaciones[i][j] = cantidad # se asigna la cantidad a la matriz de asignaciones
    ofertas[i] -= cantidad  # se resta la cantidad asignada a la oferta 
    demandas[j] -= cantidad  # se resta la cantidad asignada a la demanda
    if ofertas[i] == 0:  # si la oferta es cero, se pasa al siguiente origen
        i += 1
    if demandas[j] == 0: # si la demanda es cero, se pasa al siguiente destino 
        j += 1
# Calcular el costo total

print("Matris de costos:")
print(costos)  # se imprime la matriz de costos
costo_total = np.sum(asignaciones * costos) # se calcula el costo total multiplicando la matriz de asignaciones por la matriz de costos y sumando todos los elementos
print("Matriz de asignaciones:")
print(asignaciones)  # se imprime la matriz de asignaciones 

print(f"Costo total de transporte: {costo_total}")

print("Gracias por usar Esquina_NorOeste")


