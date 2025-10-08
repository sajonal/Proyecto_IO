##import tkinter as tk
import ttkbootstrap as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EsquinaNoroesteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Método Esquina Noroeste")

        self.frame_inicio = tk.Frame(root)
        self.frame_inicio.pack(pady=10)
        tk.Label(self.frame_inicio, text="Ingrese las dimensiones de la matriz de costos").grid(row=0, columnspan=2)
        tk.Label(self.frame_inicio, text="Número de orígenes (filas):").grid(row=1, column=0)
        self.entry_m = tk.Entry(self.frame_inicio, width=5)
        self.entry_m.grid(row=1, column=1)

        tk.Label(self.frame_inicio, text="Número de destinos (columnas):").grid(row=2, column=0)
        self.entry_n = tk.Entry(self.frame_inicio, width=5)
        self.entry_n.grid(row=2, column=1)

        tk.Button(self.frame_inicio, text="Continuar", command=self.crear_tablas).grid(row=3, column=0, columnspan=2, pady=5)

    def crear_tablas(self):
        try:
            self.m = int(self.entry_m.get())
            self.n = int(self.entry_n.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese números válidos.")
            return

        self.frame_inicio.pack_forget()

        self.frame_tablas = tk.Frame(self.root)
        self.frame_tablas.pack(pady=10)

        tk.Label(self.frame_tablas, text="Matriz de costos").grid(row=0, column=0, columnspan=self.n)
        self.entries_costos = []
        for i in range(self.m):
            fila = []
            for j in range(self.n):
                e = tk.Entry(self.frame_tablas, width=5)
                e.grid(row=i+1, column=j)
                fila.append(e)
            self.entries_costos.append(fila)

        tk.Label(self.frame_tablas, text="Ofertas").grid(row=0, column=self.n)
        self.entries_ofertas = []
        for i in range(self.m):
            e = tk.Entry(self.frame_tablas, width=5)
            e.grid(row=i+1, column=self.n)
            self.entries_ofertas.append(e)

        tk.Label(self.frame_tablas, text="Demandas").grid(row=self.m+1, column=0, columnspan=self.n)
        self.entries_demandas = []
        for j in range(self.n):
            e = tk.Entry(self.frame_tablas, width=5)
            e.grid(row=self.m+2, column=j)
            self.entries_demandas.append(e)

        tk.Button(self.root, text="Calcular", command=self.calcular).pack(pady=10)

        self.resultado = tk.Text(self.root, height=15, width=60)
        self.resultado.pack()

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack()

    def calcular(self):
        try:
            costos = np.zeros((self.m, self.n))
            for i in range(self.m):
                for j in range(self.n):
                    costos[i][j] = float(self.entries_costos[i][j].get())

            ofertas = np.array([float(e.get()) for e in self.entries_ofertas])
            demandas = np.array([float(e.get()) for e in self.entries_demandas])
        except ValueError:
            messagebox.showerror("Error", "Todos los campos deben ser números válidos.")
            return

        # Balanceo
        if sum(ofertas) != sum(demandas):
            if sum(ofertas) > sum(demandas):
                demandas = np.append(demandas, sum(ofertas) - sum(demandas))
                costos = np.hstack((costos, np.zeros((self.m, 1))))
                self.n += 1
            else:
                ofertas = np.append(ofertas, sum(demandas) - sum(ofertas))
                costos = np.vstack((costos, np.zeros((1, self.n))))
                self.m += 1

        # Método Esquina Noroeste
        asignaciones = np.zeros((self.m, self.n))
        i = j = 0

        while i < self.m and j < self.n:
            if ofertas[i] == 0:
                i += 1
                continue
            if demandas[j] == 0:
                j += 1
                continue

            cantidad = min(ofertas[i], demandas[j])
            asignaciones[i][j] = cantidad
            ofertas[i] -= cantidad
            demandas[j] -= cantidad

            if ofertas[i] == 0:
                i += 1
            if demandas[j] == 0:
                j += 1

        costo_total = np.sum(asignaciones * costos)

        # Mostrar resultados en texto
        self.resultado.delete("1.0", tk.END)
        self.resultado.insert(tk.END, "Matriz de costos:\n")
        self.resultado.insert(tk.END, f"{costos}\n\n")

        self.resultado.insert(tk.END, "Matriz de asignaciones:\n")
        self.resultado.insert(tk.END, f"{asignaciones}\n\n")

        self.resultado.insert(tk.END, f"Costo total de transporte es: {costo_total}\n")



        # Mostrar resultados con matplotlib
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 4))
        im = ax.imshow(asignaciones, cmap="Blues")

        # Agregar anotaciones
        for i in range(self.m):
            for j in range(self.n):
                text = ax.text(j, i, int(asignaciones[i, j]),
                               ha="center", va="center", color="black")

        ax.set_title(f"Asignaciones (Costo total = {costo_total})")
        ax.set_xlabel("Destinos")
        ax.set_ylabel("Orígenes")

        fig.colorbar(im, ax=ax)

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


if __name__ == "__main__":
    root = tk.Window(themename="superhero")
    app = EsquinaNoroesteApp(root)
    root.mainloop()
