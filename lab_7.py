import numpy as np
import matplotlib.pyplot as plt


# y_derivative_first = -((y + 2*x*pow(y, 2), np.log(x)) / x)
# analytical_solution = 1 / x*(pow(np.log(x), 2) + 1)


# заданная функция
def f(x, y):
    return -((y + 2*x*pow(y, 2)*np.log(x)) / x)


# аналитическое решение
def analytical_solution(x):
    return 1 / x * (np.log(x)**2 + 1)


# заданные данные
y_0 = 1
a, b = 1, 4


h = 0.1  # шаг
m = (b - a) / h
x_range = (a, b)


# явный метод Эйлера
def euler_method(f, y_0, x_range, h):
    x = np.arange(x_range[0], x_range[1] + h, h)  # делим промежуток с шагом h
    y = [y_0]  # находим у
    for n in range(1, len(x)):
        y_n = y[n-1] + h * f(x[n-1], y[n-1])
        y.append(y_n)
    return x, y


# метод Рунге-Кутты 4 порядке
def runge_cutta(f, y_0, x_range, h):
    x = np.arange(x_range[0], x_range[1] + h, h)  # делим промежуток с шагом h
    y = [y_0]
    for n in range(1, len(x)):
        k_1 = h*f(x[n-1], y[n-1])
        k_2 = h*f(x[n-1] + h/2, y[n-1] + k_1/2)
        k_3 = h*f(x[n-1] + h/2, y[n-1] + k_2/2)
        k_4 = h*f(x[n-1] + h, y[n-1] + k_3)
        y_n = y[n-1] + (k_1 + 2*k_2 + 2*k_3 + k_4) / 6
        y.append(y_n)
    return x, y


# Многошаговый метод Адамса 2 порядка точности
def adams_2(f, y_0, x_range, h):
    x = np.arange(x_range[0], x_range[1] + h, h)  # делим промежуток с шагом h
    y = [y_0]
    for n in range(1, len(x)):
        if n == 1:
            y_n = y[n - 1] + h * f(x[n - 1], y[n - 1])
            y.append(y_n)
            continue
        y_n = y[n-1] + (h/2)*(3*f(x[n-1], y[n-1]) - f(x[n-2], y[n-2]))
        y.append(y_n)
    return x, y


# Многошаговый метод Адамса 3 порядка точности
def adams_3(f, y_0, x_range, h):
    x = np.arange(x_range[0], x_range[1] + h, h)  # делим промежуток с шагом h
    y = [y_0]
    for n in range(1, len(x)):
        if n in (1, 2):
            y_n = y[n - 1] + h * f(x[n - 1], y[n - 1])
            y.append(y_n)
            continue
        y_n = y[n-1] + (h/12)*(23*f(x[n-1], y[n-1]) - 16*f(x[n-2], y[n-2]) + 5*f(x[n-2], y[n-2]))
        y.append(y_n)
    return x, y


x_euler, y_euler = euler_method(f, y_0, x_range, h)
x_runge_cutta, y_runge_cutta = runge_cutta(f, y_0, x_range, h)
x_adams_2, y_adams_2 = adams_2(f, y_0, x_range, h)
x_adams_3, y_adams_3 = adams_3(f, y_0, x_range, h)

# Строим графики
plt.figure(figsize=(10, 5))
plt.plot(x_euler, y_euler, label='Численное решение (метод Эйлера)')
plt.plot(x_runge_cutta, y_runge_cutta, label='Численное решение (метод Рунге-Кутты)')
plt.plot(x_adams_2, y_adams_2, label='Численное решение (метод Адамса 2 порядка точности)')
plt.plot(x_adams_3, y_adams_3, label='Численное решение (метод Адамса 3 порядка точности)')
plt.plot(x_adams_3, analytical_solution(x_adams_3), label='Аналитическое решение')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Решение дифференциального уравнения ')
plt.legend()
plt.grid(True)
plt.show()


# Расчет погрешности для каждого метода
def calculate_error(x_values, y_values, analytical_values):
    return np.max(np.abs(y_values - analytical_values))


# Построение графика изменения погрешности от шага интегрирования h
def plot_error(method, method_name, f, y_0, x_range, h):
    h_min = (b - a) / 1000
    h_max = (b - a) / 10
    h_values = np.linspace(h_min, h_max, 20)
    errors = []
    for h in h_values:
        x_values, y_values = method(f, y_0, x_range, h)
        analytical_values = analytical_solution(x_values)
        errors.append(calculate_error(x_values, y_values, analytical_values))
    plt.plot(h_values, errors, label=method_name)
    plt.xlabel('Шаг интегрирования (h)')
    plt.ylabel('Погрешность')
    plt.title('Зависимость погрешности от шага интегрирования')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.show()


# Построение графика изменения погрешности от шага интегрирования h для каждого метода
plot_error(euler_method, 'Метод Эйлера', f, y_0, x_range, h)
plot_error(runge_cutta, 'Метод Рунге-Кутты', f, y_0, x_range, h)
plot_error(adams_2, 'Многошаговый метод Адамса (2 порядок)', f, y_0, x_range, h)
plot_error(adams_3, 'Многошаговый метод Адамса (3 порядок)', f, y_0, x_range, h)
