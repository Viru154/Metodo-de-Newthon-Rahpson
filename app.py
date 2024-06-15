import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

def newton_raphson(f, x0, tol=1e-6, max_iter=100):
    x = x0
    iterations = [x]
    for i in range(max_iter):
        fx = f(x)
        dfx = derivative(f, x)
        if dfx == 0:
            return None, "Derivada cero. El método no puede continuar."
        x_new = x - fx / dfx
        iterations.append(x_new)
        if abs(x_new - x) < tol:
            return iterations, None
        x = x_new
    return iterations, "El método no convergió en el número máximo de iteraciones."

def derivative(f, x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2 * h)

def solve():
    try:
        func_str = func_entry.get()
        f = lambda x: eval(func_str)
        x0 = float(x0_entry.get())
        max_iter = int(iter_entry.get())

        iterations, error = newton_raphson(f, x0, max_iter=max_iter)
        if error:
            messagebox.showerror("Error", error)
        else:
            plot_iterations(iterations)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def plot_iterations(iterations):
    plt.figure()
    plt.plot(range(len(iterations)), iterations, marker='o')
    plt.title('Iteraciones del Método de Newton-Raphson')
    plt.xlabel('Iteración')
    plt.ylabel('Valor de x')
    plt.grid(True)
    plt.show()

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Método de Newton-Raphson")

tk.Label(root, text="Función (f(x))").grid(row=0, column=0)
func_entry = tk.Entry(root, width=30)
func_entry.grid(row=0, column=1)

tk.Label(root, text="Estimación Inicial (x0)").grid(row=1, column=0)
x0_entry = tk.Entry(root, width=30)
x0_entry.grid(row=1, column=1)

tk.Label(root, text="Máximo de Iteraciones").grid(row=2, column=0)
iter_entry = tk.Entry(root, width=30)
iter_entry.grid(row=2, column=1)

tk.Button(root, text="Calcular", command=solve).grid(row=3, columnspan=2)

root.mainloop()
