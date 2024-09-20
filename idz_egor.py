# 1+(y/(x*(x+1)))
# (x**2+x*log(x))/(x+1)

from numpy import *
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from fractions import Fraction

PI = 3.14159265358979323846

ACCURACY = 1e-3
# Диапазон значений x
RANGE = (0.0, 2.0)

# Начальные условия
CAUCHY_CONDITION = (0, 0)


# Метод Ингленда 4 порядка для численного решения ОДУ
def england_method(f, range_, step, x, y_old, cauchy_condition):
    k1 = step * f(x, y_old)
    k2 = step * f(x + (step / 2.0), y_old + k1 / 2)
    k3 = step * f(x + (step / 2.0), y_old + (k1 + k2) / 4.0)
    k4 = step * f(x + step, y_old + 2 * k3 - k2)
    k5 = step * f(x + (step * (2 / 3)), y_old + (7 * k1 + 10 * k2 + k4) / 27)
    k6 = step * f(x + (step * 0.2), y_old + (28 * k1 - 125 * k2 + 546 * k3 + 54 * k4 - 378 * k5) / 625)
    return (
    y_old + (k1 + (k3 * 4.0) + k4) / 6.0, abs((-42 * k1 - 224 * k3 + 21 * k4 + 162 * k5 + 125 * k6) / (336 / ACCURACY)))


def endland_err_corr(f, range_, step, cauchy_condition):
    temp_step = step
    sol = 0
    hsol = 0
    err_global = 0
    solution = []
    x = range_[0]
    x0 = range_[0]
    solution.append((cauchy_condition[0], cauchy_condition[1], 0, 0))
    while x <= range_[1]:
        sol = england_method(f, range_, temp_step, x, solution[-1][1], cauchy_condition)
        if sol[1] > 1e-4:
            temp_step = temp_step / 2
        else:
            err_global += abs(sol[1])
            x += temp_step
            solution.append((range_[0] + x, sol[0], sol[1], err_global))
            print(x)
    return solution


def EnglandSolve():
    exec("def f(x,y) -> float:return " + f_entry.get(), globals())
    yerrLocal = []
    yerrGlobal = []
    yerrC = 0
    TableRows = []
    step = float(e_step.get())
    solution = endland_err_corr(f, RANGE, step, CAUCHY_CONDITION)
    for i in range(len(solution)):
        TableRows.append(solution[i])
    for Row in TableRows:
        tree.insert("", END, values=Row)
    graph(solution)


def graph(solutions):
    fig, (a1, a3, a4) = plt.subplots(1, 3)
    xaxis = []
    yaxis = []
    yerrLocal = []
    yerrGlobal = []
    step = float(e_step.get())
    for i in range(len(solutions)):
        xaxis.append(solutions[i][0])
        yaxis.append(solutions[i][1])
        yerrLocal.append(solutions[i][2])
        yerrGlobal.append(solutions[i][3])
    a1.set_title("Приближённое решение")
    a3.set_title("Локальная ошибка")
    a4.set_title("Глобальная ошибка")
    a1.plot(xaxis, yaxis)
    a3.plot(xaxis, yerrLocal)
    a4.plot(xaxis, yerrGlobal)
    a1.grid()
    a3.grid()
    a4.grid()
    plt.show()


root = Tk()
root.title("Application")
root.geometry("400x420")

f_entry = Entry(root)
f_entry.pack()

e_step = Entry(root)
e_step.pack()

Calc = Button(root, text="Метод Рунге-Кутты 3 порядка", command=lambda: EnglandSolve())
Calc.pack()

columns = ("x", "approx", "local", "global")

tree = ttk.Treeview(columns=columns, show="headings")
tree.heading("x", text="X")
tree.heading("approx", text="Приближённое решение")
tree.heading("local", text="Локальная ошибка")
tree.heading("global", text="Глобальная ошибка")
tree.pack(fill=BOTH, expand=1)
root.mainloop()
