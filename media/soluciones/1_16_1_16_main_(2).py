import tkinter as tk
from tkinter import ttk, messagebox

# Variables globales para almacenar procesos
procesos = []

# Función para agregar un proceso
def agregar_proceso():
    nombre = entry_nombre.get()
    at = entry_at.get()
    bt = entry_bt.get()

    if nombre and at.isdigit() and bt.isdigit():
        procesos.append({
            "nombre": nombre,
            "AT": int(at),
            "BT": int(bt)
        })
        actualizar_lista()
        entry_nombre.delete(0, tk.END)
        entry_at.delete(0, tk.END)
        entry_bt.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Completa todos los campos correctamente")

# Función para actualizar la lista de procesos
def actualizar_lista():
    listbox.delete(0, tk.END)
    for proceso in procesos:
        listbox.insert(tk.END, f"{proceso['nombre']} - AT: {proceso['AT']} - BT: {proceso['BT']}")

# Función para iniciar la simulación
def iniciar_simulacion():
    algoritmo = combo_algoritmo.get()
    if algoritmo == "FIFO":
        ejecutar_fifo()
    elif algoritmo == "SJF":
        ejecutar_sjf()
    elif algoritmo == "Round Robin":
        ejecutar_rr()
    else:
        messagebox.showerror("Error", "Selecciona un algoritmo")

# Algoritmo FIFO (Primero en entrar, primero en salir)
def ejecutar_fifo():
    resultados = []
    tiempo_actual = 0
    for proceso in sorted(procesos, key=lambda x: x['AT']):
        if tiempo_actual < proceso['AT']:
            tiempo_actual = proceso['AT']
        tiempo_actual += proceso['BT']
        ct = tiempo_actual
        tat = ct - proceso['AT']
        wt = tat - proceso['BT']
        resultados.append([proceso['nombre'], proceso['AT'], proceso['BT'], ct, tat, wt])
    
    mostrar_resultados(resultados)

# Algoritmo SJF (Trabajo más corto primero)
def ejecutar_sjf():
    resultados = []
    tiempo_actual = 0
    lista_procesos = sorted(procesos, key=lambda x: (x['AT'], x['BT']))
    while lista_procesos:
        disponibles = [p for p in lista_procesos if p['AT'] <= tiempo_actual]
        if disponibles:
            proceso = min(disponibles, key=lambda x: x['BT'])
            lista_procesos.remove(proceso)
            tiempo_actual += proceso['BT']
            ct = tiempo_actual
            tat = ct - proceso['AT']
            wt = tat - proceso['BT']
            resultados.append([proceso['nombre'], proceso['AT'], proceso['BT'], ct, tat, wt])
        else:
            tiempo_actual += 1  # Avanzar el tiempo si no hay procesos disponibles
    
    mostrar_resultados(resultados)

# Algoritmo Round Robin
def ejecutar_rr():
    try:
        quantum = int(entry_quantum.get())
        if quantum <= 0:
            raise ValueError
        
        resultados = []
        tiempo_actual = 0
        cola = procesos.copy()
        tiempos_espera = {p['nombre']: 0 for p in procesos}
        
        while cola:
            proceso = cola.pop(0)
            if proceso['AT'] > tiempo_actual:
                tiempo_actual = proceso['AT']
            
            tiempo_ejec = min(proceso['BT'], quantum)
            proceso['BT'] -= tiempo_ejec
            tiempo_actual += tiempo_ejec
            
            if proceso['BT'] > 0:
                cola.append(proceso)
            else:
                ct = tiempo_actual
                tat = ct - proceso['AT']
                wt = tat - (proceso['BT'] + tiempo_ejec)
                resultados.append([proceso['nombre'], proceso['AT'], proceso['BT'] + tiempo_ejec, ct, tat, wt])
        
        mostrar_resultados(resultados)
    
    except ValueError:
        messagebox.showerror("Error", "El Quantum debe ser un número entero positivo.")

# Función para mostrar resultados en una nueva ventana
def mostrar_resultados(resultados):
    resultados_window = tk.Toplevel(root)
    resultados_window.title("Resultados")
    tree = ttk.Treeview(resultados_window, columns=("AT", "BT", "CT", "TAT", "WT"), show="headings")
    tree.heading("AT", text="AT")
    tree.heading("BT", text="BT")
    tree.heading("CT", text="CT")
    tree.heading("TAT", text="TAT")
    tree.heading("WT", text="WT")
    tree.pack(fill=tk.BOTH, expand=True)
    
    for res in resultados:
        tree.insert("", tk.END, values=(res[1], res[2], res[3], res[4], res[5]))

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Simulador de Planificación de Procesos")
root.geometry("400x450")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Nombre Proceso").grid(row=0, column=0)
entry_nombre = tk.Entry(frame)
entry_nombre.grid(row=0, column=1)

tk.Label(frame, text="Tiempo de Llegada (AT)").grid(row=1, column=0)
entry_at = tk.Entry(frame)
entry_at.grid(row=1, column=1)

tk.Label(frame, text="Tiempo de Rafaga (BT)").grid(row=2, column=0)
entry_bt = tk.Entry(frame)
entry_bt.grid(row=2, column=1)

btn_agregar = tk.Button(frame, text="Agregar Proceso", command=agregar_proceso)
btn_agregar.grid(row=3, column=0, columnspan=2, pady=5)

listbox = tk.Listbox(root)
listbox.pack(pady=10, fill=tk.BOTH)

combo_algoritmo = ttk.Combobox(root, values=["FIFO", "SJF", "Round Robin"])
combo_algoritmo.set("Selecciona Algoritmo")
combo_algoritmo.pack()

tk.Label(root, text="Quantum (Solo para Round Robin):").pack()
entry_quantum = tk.Entry(root)
entry_quantum.pack()

btn_simular = tk.Button(root, text="Iniciar Simulación", command=iniciar_simulacion)
btn_simular.pack(pady=10)

root.mainloop()
