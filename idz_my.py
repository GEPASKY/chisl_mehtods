import numpy as np
import sympy as sp
# Алексей Владимирович


# Парсер консоли
def pars(inpt):
    # Определяем символы и константы
    x, y = sp.symbols('x y')
    pi = sp.pi
    e = sp.E

    # Преобразуем строку в математическое выражение
    expression = sp.sympify(inpt)

    return expression


# Вводим математическое выражение и преобразуем его
user_input = input("Введите математическое выражение: ")
parsed_expr = pars(user_input)
# print(f"Parsed expression: {parsed_expr}")

# Определяем символьную функцию на основе введенного выражения
x, y = sp.symbols('x y')
f_expr = sp.lambdify((x, y), parsed_expr, 'numpy')


# Метод Рунге-Кутты 3 порядка
def runge_kutta_3(f, x_values, y_values, h, n):
    x_n, y_n = x_values[n], y_values[-1]
    k_1 = h * f(x_n, y_n)
    k_2 = h * f(x_n + h / 2, y_n + k_1 / 2)
    k_3 = h * f(x_n + h, y_n + 2 * k_2 - k_1)
    y_next = y_n + (k_1 + 4 * k_2 + k_3) / 6
    return y_next


def euler_method(f, x_valye, y_n, h, n):
    y_n = y[n-1] + h * f(x[n-1], y[n-1])
    y.append(y_n)
    return y


# Задаем начальные условия и параметры
y_0 = float(input("Введите начальное значение y_0: "))  # Начальное значение y_0
a = float(input("Введите начальное значение х_0: "))  # Начальное значение x_0
b = float(input("Введите конечное значение b: "))  # Конечное значение
step = float(input("Введите начальный шаг: "))  # Начальный шаг интегрирования
loc_accuracy = float(input("Введите начальную локальную точность: "))  # Точность локальная
glob_accuracy = float(input("Введите начальную глобальную точность: "))  # Точность глобальная
local_errors = []
global_errors = []


def main(f, y_0, step, a, b, loc_accuracy, glob_accuracy):
    h = step
    x_values = [a]  # Начальное значение x
    y_values = [y_0]  # Начальное значение y
    local_error = 0
    global_error = 0

    n = 0
    while x_values[-1] < b:
        if len(y_values) > 30:
            del x_values[-1]
            break
        if x_values[-1] + h > b:
            h = b - x_values[-1]

        y_next = runge_kutta_3(f, x_values, y_values, h, n)
        if len(y_values) > 1:
            local_error = abs(y_next - y_values[-1])
        else:
            local_error = 0.0

        if local_error > loc_accuracy:
            while local_error > loc_accuracy:
                h = h / 2
                del y_values[-1]
                y_last = runge_kutta_3(f, x_values, y_values, h, n)
                y_values.append(y_last)
                if len(y_values) > 1:
                    local_error = abs(y_last - y_values[-2])
                else:
                    local_error = 0.0
            x_values.append(x_values[-1] + h)
        else:
            y_values.append(y_next)
            x_values.append(x_values[-1] + h)
            local_errors.append(local_error)
            global_error += local_error

        if global_error > glob_accuracy:
            h *= 0.5
            global_error -= local_error
        global_errors.append(global_error)

            # n += 1
        # print(f"x_i {x_values[-1]:>12.10f}, y_i {y_values[-1]:>12.10f}, local_error {local_error:>12.20f}, global_error {global_error:>12.20f}")
        n += 1

    return x_values, y_values


# Вызываем метод Рунге-Кутты
x_values, y_values = main(f_expr, y_0, step, a, b, loc_accuracy, glob_accuracy)

# Вывод результатов
print("____________________________")
print("|  x_i  |     y_i      |  local_error  |  global_error  |")
for i in range(len(x_values)):
    local_error = local_errors[i] if i < len(local_errors) else 0
    global_error = global_errors[i] if i < len(global_errors) else 0
    print(f"| {x_values[i]:>5.20f} | {y_values[i]:>12.20f} | {local_error:>12.20f} | {global_error:>12.20f} |")

if global_errors:
    print(f"\nПриблизительная глобальная ошибка: {global_errors[-1]:.8f}")
else:
    print("\nНет доступных данных для глобальной ошибки.")
