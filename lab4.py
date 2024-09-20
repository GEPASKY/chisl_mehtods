"""Интерполяция."""
from math import pi, sin
import matplotlib.pyplot as plt


def calc_node_x(diapason, nodesNumber):
    """Рассчитывает координаты узлов."""

    # Длина отрезка
    lenght = diapason[1] - diapason[0]
    # Шаг до следующего узла
    x_step = lenght/nodesNumber

    return [diapason[0] + x_step * i for i in range(nodesNumber+1)]

def f_x(x): # (можно менять)
    """Рассчитывает значение функции."""

    return 1/(1-sin(x))

def lagrange(nodes, diapason):
    """Функция проходящая через узлы.

    Аргументы:
    [1] nodes: список координат x узлов
    [2] diapason: область функции
    Возвращает:
    -  Координаты x,y восстановленной функции
    """
    
    L_x = []
    L_y = []
    
    for x in nodes:
        L = 0
        for i in range(len(nodes)):
            p = 1
            for j in range(len(nodes)):
                if i == j:
                    continue
                # Вычисляем Pi    
                p *= (x-nodes[j])/(nodes[i]-nodes[j])
                
            L += f_x(nodes[i]) * p
            
        L_x.append(x)
        L_y.append(L)
    return L_x, L_y

def linear(nodes, diapason):
    linear_x = []
    linear_y = []

    linear_x = nodes
    
    for i in range(len(nodes)-1):
        x = nodes[i]
        x_next = nodes[i+1]
        y = f_x(x)
        y_next = f_x(x_next)
        
        # Рассчёт коэфициентов a,b.
        a = (y_next-y)/(x_next-x)
        b = y - a * x

        linear_y.append(a*x+b)
    else:
        linear_y.append(f_x(nodes[-1]))

    return linear_x, linear_y

    
# Область функции (можно менять)
diapason = [pi, 2 * pi]

# Для 5 узлов.
# Рассчёт полинома Лагранжа.
L_x, L_y = lagrange(calc_node_x(diapason, 5), diapason)

# Рассчёт кусочно-линейной функции
linear_x, linear_y = linear(calc_node_x(diapason, 5), diapason)
# Погрешности.
print(" - Погрешности для 5 узлов")
origFuncY = [f_x(x) for x in calc_node_x(diapason, 5)]
print(" Полином Лагранжа |f(x)-L(x)|:", [abs(origFuncY[i]-L_y[i]) for i in range(len(origFuncY))])
print(" Кусочно-линейная |f(x)-g(x)|:", [abs(origFuncY[i]-linear_y[i]) for i in range(len(origFuncY))])


# График
plt.subplot(1, 2, 1)
plt.plot(L_x, L_y)
plt.title("Полином Лагранжа")
plt.subplot(1, 2, 2)
plt.plot(linear_x, linear_y)
plt.title("Кусочно-линейная функция")
plt.show()

# Для 7 узлов.
# Рассчёт полинома Лагранжа.
L_x, L_y = lagrange(calc_node_x(diapason, 7), diapason)
# Рассчёт кусочно-линейной функции
linear_x, linear_y = linear(calc_node_x(diapason, 7), diapason)
# Погрешности.
print(" - Погрешности для 7 узлов")
origFuncY = [f_x(x) for x in calc_node_x(diapason, 7)]
print(" Полином Лагранжа |f(x)-L(x)|:", [abs(origFuncY[i]-L_y[i]) for i in range(len(origFuncY))])
print(" Кусочно-линейная |f(x)-g(x)|:", [abs(origFuncY[i]-linear_y[i]) for i in range(len(origFuncY))])

# График
plt.subplot(1, 2, 1)
plt.plot(L_x, L_y)
plt.title("Полином Лагранжа")
plt.subplot(1, 2, 2)
plt.plot(linear_x, linear_y)
plt.title("Кусочно-линейная функция")
plt.show()

# Для 10 узлов.
# Рассчёт полинома Лагранжа.
L_x, L_y = lagrange(calc_node_x(diapason, 10), diapason)
# Рассчёт кусочно-линейной функции
linear_x, linear_y = linear(calc_node_x(diapason, 10), diapason)
# Погрешности.
print(" - Погрешности для 10 узлов")
origFuncY = [f_x(x) for x in calc_node_x(diapason, 10)]
print(" Полином Лагранжа |f(x)-L(x)|:", [abs(origFuncY[i]-L_y[i]) for i in range(len(origFuncY))])
print(" Кусочно-линейная |f(x)-g(x)|:", [abs(origFuncY[i]-linear_y[i]) for i in range(len(origFuncY))])

# График
plt.subplot(1, 2, 1)
plt.plot(L_x, L_y)
plt.title("Полином Лагранжа")
plt.subplot(1, 2, 2)
plt.plot(linear_x, linear_y)
plt.title("Кусочно-линейная функция")
plt.show()
