import numpy as np
import time
import tracemalloc
import matplotlib.pyplot as plt


# 3*np.cos(2*np.pi*x)
# пример функции для правой части ОДУ
def f(x, y):
    return 3*np.cos(2*np.pi*x)


def analytical_solution(x):
    return 1 / (x + 1)


# метод Рунге-Кутты 3-го порядка
def rk3(f, x0, y0, h, x_end):
    x_values = [x0]
    y_values = [y0]
    x = x0
    y = y0
    
    while x < x_end:
        k1 = h * f(x, y)
        k2 = h * f(x + h/2, y + k1/2)
        k3 = h * f(x + h, y + 2*k2 -k1)
        y += (k1 + 4*k2 + k3) / 6
        x += h
        x_values.append(x)
        y_values.append(y)
    
    return np.array(x_values), np.array(y_values)


# Функция для вычисления глобальной ошибки
def global_error(y_numeric, y_analytical):
    return np.abs(y_numeric - y_analytical).max()


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


# параметры
x0 = 0
y0 = 0
yp = 0
x_end = 1
hl = 0.01
h = 0.01
t = 0.001


# решение методом Рунге-Кутты 3 порядка
x_exact = np.arange(x0, x_end + h, h)
y_exact = analytical_solution(x_exact)

methods = {
    "Рунге-Кутты 3": (rk3, f, x0, y0, h, x_end)
}

results = []
glob = 0
i = 0
r = 0
for name, (method, *args) in methods.items():
    x_values, y_values, memory_usage, cpu_time = evaluate_method(method, *args)
    error = global_error(y_values, analytical_solution(x_values))
    results.append((name, memory_usage, cpu_time, error))
    print("Метод " + name)
    print("x           y         локальная          глобальная")
    while i < len(y_values):
        if i == 0:
            loc = abs(y_values[i - 1] - yp)/1000
        else:
            loc = abs(y_values[i] - y_values[i - 1])/1000
        if hl < loc:
            hl = hl/2
        glob += loc
        print(x_values[i], ' ', y_values[i], ' ', loc, ' ', glob)
        i += 1

    plt.plot(x_values, y_values, label=f'{name} Solution')


print("Метод         | Память (KB) | CPU Время (s) |  Эффективность")
print("------------------------------------------------------------")
for name, memory_usage, cpu_time, error in results:
    
    eff = memory_usage / error 
    print(f"{name:<15} | {memory_usage:<12} | {cpu_time:<12} |  {eff:<12}")
  
