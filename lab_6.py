import numpy as np
import matplotlib.pyplot as plt


# Определим функцию для интегрирования
def f(x):
    return np.exp(np.arccos(x))


# Определим точное значение интеграла
exact_value = (1 + np.exp(np.pi / 2)) / 2


# Метод прямоугольников (левых)
def left_rectangles_integration(f, a, b, n):
    x = np.linspace(a, b, n + 1)  # Генерируем равномерные узлы
    integral = 0
    for i in range(n):
        integral += f(x[i]) * (x[i+1] - x[i])
    return integral


# Метод прямоугольников (правых)
def right_rectangles_integration(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    integral = 0
    for i in range(n):
        integral += f(x[i+1]) * (x[i+1] - x[i])
    return integral


# Метод прямоугольников (средних)
def middle_rectangles_integration(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    integral = 0
    for i in range(n):
        integral += f((x[i+1] + x[i]) / 2) * (x[i+1] - x[i])
    return integral


# Метод трапеций
def trapezoidal_integration(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    integral = 0
    for i in range(n):
        integral += ((f(x[i]) + f(x[i+1])) / 2) * (x[i+1] - x[i])  # Суммируем значения функции на остальных узлах
    return integral


# Метод парабол
def simpsons_integration(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    integral = 0
    for i in range(1, n):
        integral += (f(x[i]) + 4*f((x[i+1] + x[i]) / 2) + f(x[i+1])) * (x[i+1] - x[i])
    integral *= 1/6
    return integral


# Зададим количество разбиений n
n_values = np.arange(10, 1001, 10)

# Вычислим интегралы и оценим погрешности для каждого метода
errors_left_rectangles = []
errors_right_rectangles = []
errors_middle_rectangles = []
errors_trapezoidal = []
errors_simpsons = []

for n in n_values:
    # Вычисляем интегралы для каждого метода
    integral_left = left_rectangles_integration(f, 0, 1, n)
    integral_right = right_rectangles_integration(f, 0, 1, n)
    integral_middle = middle_rectangles_integration(f, 0, 1, n)
    integral_trapezoidal = trapezoidal_integration(f, 0, 1, n)
    integral_simpsons = simpsons_integration(f, 0, 1, n)

    # Оцениваем погрешности для каждого метода
    errors_left_rectangles.append(abs(integral_left - exact_value))
    errors_right_rectangles.append(abs(integral_right - exact_value))
    errors_middle_rectangles.append(abs(integral_middle - exact_value))
    errors_trapezoidal.append(abs(integral_trapezoidal - exact_value))
    errors_simpsons.append(abs(integral_simpsons - exact_value))

# Построим графики зависимости погрешности от шага разбиения для каждого метода
plt.figure(figsize=(12, 8))

plt.plot(n_values, errors_left_rectangles, label='Прямоугольники (левые)', marker='o')
plt.plot(n_values, errors_right_rectangles, label='Прямоугольники (правые)', marker='s')
plt.plot(n_values, errors_middle_rectangles, label='Прямоугольники (средние)', marker='^')
plt.plot(n_values, errors_trapezoidal, label='Трапеции', marker='x')
plt.plot(n_values, errors_simpsons, label='Параболы (Симпсон)', marker='d')

plt.title('Зависимость погрешности от шага разбиения для различных методов')
plt.xlabel('Количество разбиений (n)')
plt.ylabel('Погрешность')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.grid(True)
plt.show()


print(simpsons_integration(f, 0, 1, 100))
print(right_rectangles_integration(f, 0, 1, 100))
print(exact_value)

