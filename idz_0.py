import numpy as np
import time
import tracemalloc
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math


# Аналитическое решение для сравнения
def analytical_solution(x):
    return 1 / (x + 1)


# Метод Рунге-Кутты 3-го порядка
def rk3(f, x0, y0, h, x_end):
    x_values = [x0]
    y_values = [y0]
    x = x0
    y = y0

    while x < x_end:
        k1 = h * f(x, y)
        k2 = h * f(x + h / 2, y + k1 / 2)
        k3 = h * f(x + h, y + 2 * k2 - k1)
        y += (k1 + 4 * k2 + k3) / 6
        x += h
        x_values.append(x)
        y_values.append(y)

    return np.array(x_values), np.array(y_values)


# Функция для вычисления глобальной ошибки
def global_error(y_numeric, y_analytical):
    return np.abs(y_numeric - y_analytical).max()


# Функция для вычисления локальной ошибки
def local_errors(y_numeric, h):
    return [np.abs(y_numeric[i + 1] - y_numeric[i]) / h for i in range(len(y_numeric) - 1)]


# Функция для оценки затрат памяти и процессора
def evaluate_method(method, *args):
    tracemalloc.start()
    start_time = time.process_time()
    x_values, y_values = method(*args)
    end_time = time.process_time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memory_usage = peak / 1024
    cpu_time = end_time - start_time
    return x_values, y_values, memory_usage, cpu_time


# Основная функция для выполнения вычислений и обновления GUI
def run_simulation():
    try:
        # Чтение входных данных из GUI
        x0 = float(entry_x0.get())
        y0 = float(entry_y0.get())
        x_end = float(entry_x_end.get())
        h = float(entry_h.get())
        f_str = entry_function.get()

        # Компиляция строки функции в Python функцию
        def f(x, y):
            return eval(f_str, {"x": x, "y": y, "cos": math.cos, "sin": math.sin, "tan": math.tan,
                                "cot": lambda x: 1 / math.tan(x), "exp": math.exp, "pi": math.pi})

        # Решение методом Рунге-Кутты 3-го порядка
        x_exact = np.arange(x0, x_end + h, h)
        y_exact = analytical_solution(x_exact)

        methods = {
            "Рунге-Кутты 3": (rk3, f, x0, y0, h, x_end)
        }

        results = []
        for name, (method, *args) in methods.items():
            x_values, y_values, memory_usage, cpu_time = evaluate_method(method, *args)
            y_analytical = analytical_solution(x_values)
            glob_error = global_error(y_values, y_analytical)
            loc_errors = local_errors(y_values, h)
            results.append((name, x_values, y_values, y_analytical, memory_usage, cpu_time, glob_error, loc_errors))

            # Построение графика
            ax.plot(x_values, y_values, label=f'{name} Solution')

        # Построение аналитического решения
        ax.plot(x_exact, y_exact, 'k--', label='Аналитическое решение')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()
        ax.set_title('Сравнение численного и аналитического решений')
        ax.grid(True)
        canvas.draw()

        # Обновление результатов вычислений
        text_results.delete(1.0, END)
        text_results.insert(END, "Метод: Рунге-Кутты 3\n")
        text_results.insert(END, "x           y           y_аналитическое   Глобальная ошибка    Локальная ошибка\n")
        text_results.insert(END, "---------------------------------------------------------------------\n")
        for name, x_values, y_values, y_analytical, memory_usage, cpu_time, glob_error, loc_errors in results:
            for i in range(len(x_values)):
                loc_error = loc_errors[i - 1] if i > 0 else 0
                text_results.insert(END,
                                    f"{x_values[i]:<12.6f} {y_values[i]:<12.6f} {y_analytical[i]:<18.6f} {glob_error:<20.6f} {loc_error:<18.6f}\n")
            text_results.insert(END,
                                f"\nПамять (KB): {memory_usage:.2f}\nCPU Время (s): {cpu_time:.6f}\nГлобальная ошибка: {glob_error:.6f}\n")

    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


# Создание главного окна
root = Tk()
root.title("Решение ОДУ методом Рунге-Кутты 3-го порядка")

# Параметры метода
frame_params = Frame(root)
frame_params.pack(pady=10)

Label(frame_params, text="Начальное x0:").grid(row=0, column=0, padx=5, pady=5)
entry_x0 = Entry(frame_params)
entry_x0.grid(row=0, column=1, padx=5, pady=5)

Label(frame_params, text="Начальное y0:").grid(row=1, column=0, padx=5, pady=5)
entry_y0 = Entry(frame_params)
entry_y0.grid(row=1, column=1, padx=5, pady=5)

Label(frame_params, text="Конечное x:").grid(row=2, column=0, padx=5, pady=5)
entry_x_end = Entry(frame_params)
entry_x_end.grid(row=2, column=1, padx=5, pady=5)

Label(frame_params, text="Шаг h:").grid(row=3, column=0, padx=5, pady=5)
entry_h = Entry(frame_params)
entry_h.grid(row=3, column=1, padx=5, pady=5)

Label(frame_params, text="Функция f(x, y):").grid(row=4, column=0, padx=5, pady=5)
entry_function = Entry(frame_params)
entry_function.grid(row=4, column=1, padx=5, pady=5)

Button(frame_params, text="Запустить", command=run_simulation).grid(row=5, columnspan=2, pady=10)

# График результатов
frame_graph = Frame(root)
frame_graph.pack(pady=10)

fig, ax = plt.subplots(figsize=(5, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_graph)
canvas.get_tk_widget().pack()

# Результаты вычислений
frame_results = Frame(root)
frame_results.pack(pady=10)

text_results = Text(frame_results, height=15, width=100)
text_results.pack()

root.mainloop()
