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

        # Crear el frame principal para dividir la ventana
        self.frame_controles = tk.Frame(root)
        self.frame_controles.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.frame_grafico = tk.Frame(root)
        self.frame_grafico.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Controles iniciales en el frame de controles
        tk.Label(self.frame_controles, text="Ingrese las dimensiones de la matriz de costos").grid(row=0, columnspan=2)
        tk.Label(self.frame_controles, text="Número de orígenes (filas):").grid(row=1, column=0)
        self.entry_m = tk.Entry(self.frame_controles, width=5)
        self.entry_m.grid(row=1, column=1)

        tk.Label(self.frame_controles, text="Número de destinos (columnas):").grid(row=2, column=0)
        self.entry_n = tk.Entry(self.frame_controles, width=5)
        self.entry_n.grid(row=2, column=1)

        tk.Button(self.frame_controles, text="Continuar", command=self.crear_tablas, bootstyle="success").grid(row=3, column=0, columnspan=2, pady=5)

    def reiniciar(self):
        # Eliminar todos los widgets actuales
        for widget in self.frame_controles.winfo_children():
            widget.destroy()
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        # Volver a mostrar la interfaz inicial
        self.__init__(self.root)

    def crear_tablas(self):
        try:
            self.m = int(self.entry_m.get())
            self.n = int(self.entry_n.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese números válidos.")
            return

        # Limpiar el frame de controles
        for widget in self.frame_controles.winfo_children():
            widget.destroy()

        tk.Label(self.frame_controles, text="Matriz de costos").grid(row=0, column=0, columnspan=self.n)
        self.entries_costos = []
        for i in range(self.m):
            fila = []
            for j in range(self.n):
                e = tk.Entry(self.frame_controles, width=5)
                e.grid(row=i+1, column=j, padx=5, pady=5)
                fila.append(e)
            self.entries_costos.append(fila)

        tk.Label(self.frame_controles, text="Ofertas").grid(row=0, column=self.n + 1)
        self.entries_ofertas = []
        for i in range(self.m):
            e = tk.Entry(self.frame_controles, width=5)
            e.grid(row=i+1, column=self.n + 1, padx=5, pady=5)
            self.entries_ofertas.append(e)

        tk.Label(self.frame_controles, text="Demandas").grid(row=self.m+1, column=0, columnspan=self.n)
        self.entries_demandas = []
        for j in range(self.n):
            e = tk.Entry(self.frame_controles, width=5)
            e.grid(row=self.m+2, column=j, padx=5, pady=5)
            self.entries_demandas.append(e)

        tk.Button(self.frame_controles, text="Calcular", command=self.calcular, bootstyle="primary").grid(row=self.m+3, column=0, columnspan=2, pady=10)
        tk.Button(self.frame_controles, text="Nueva matriz", command=self.reiniciar, bootstyle="danger").grid(row=self.m+4, column=0, columnspan=2, pady=10)

        self.resultado = tk.Text(self.frame_controles, height=10, width=40)
        self.resultado.grid(row=self.m+5, column=0, columnspan=self.n + 2, pady=10)

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
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(8, 6))  # Aumentar el tamaño del gráfico
        im = ax.imshow(asignaciones, cmap="Blues", aspect="auto")

        # Mostrar valores de las asignaciones en las celdas
        for i in range(self.m):
            for j in range(self.n):
                ax.text(j, i, f"{int(asignaciones[i, j])}", ha="center", va="center", color="black", fontsize=10)

        # Etiquetas de los ejes con los valores de oferta y demanda
        ax.set_xticks(range(self.n))
        ax.set_yticks(range(self.m))
        ax.set_xticklabels([f"{d:.1f}" for d in demandas], fontsize=10, rotation=45)  # Etiquetas de demanda en el eje X
        ax.set_yticklabels([f"{o:.1f}" for o in ofertas], fontsize=10)  # Etiquetas de oferta en el eje Y

        # Títulos y etiquetas
        ax.set_title(f"Asignaciones (Costo total = {costo_total:.2f})", fontsize=12, pad=15)
        ax.set_xlabel("Demanda", fontsize=10)
        ax.set_ylabel("Oferta", fontsize=10)

        # Mostrar el gráfico en el canvas de Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Window(themename="superhero")
    root.geometry("800x800")
    app = EsquinaNoroesteApp(root)
    root.mainloop()
