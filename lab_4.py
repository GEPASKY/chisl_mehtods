from math import sqrt
import matplotlib.pyplot as plt

# переделать погрешность взять точки между узлами check


# fx = sqrt(2*x + 1) - sqrt(x + 1)
begin, end = 2, 10


def f(x_):
    return sqrt(2*x_ + 1) - sqrt(x_ + 1)


def lagrange(cnt_nodes):
    cnt_nodes -= 1
    segment = end - begin  # кол-во элементов в отрезке
    step = segment / cnt_nodes

    nodes = [begin]  # узлы x
    x_i = begin
    for i in range(cnt_nodes):
        x_i += step
        nodes.append(x_i)

    values_nodes = list(map(lambda x_: round(f(x_), 2), nodes))  # функция и ее y_i

    # Построим полином Лагранжа по формулам
    L = list()
    for x in nodes:
        L_x = 0
        for i in range(len(nodes)):
            p = 1
            for j in range(len(nodes)):
                if i != j:
                    p *= (x - nodes[j])/(nodes[i] - nodes[j])
            L_x += p*values_nodes[i]
        L.append(L_x)
    return nodes, L


def linear(cnt_nodes):
    cnt_nodes -= 1
    segment = end - begin  # кол-во элементов в отрезке
    step = segment / cnt_nodes

    nodes = [begin]  # узлы x
    x_i = begin
    for i in range(cnt_nodes):
        x_i += step
        nodes.append(x_i)

    values_nodes = list(map(lambda x_: round(f(x_), 2), nodes))  # функция и ее y_i+1
    values_nodes.append(round(f(end+step), 2))

    points = list()
    for i in range(cnt_nodes+1):
        b = values_nodes[i+1] - (values_nodes[i+1] - values_nodes[i]) / nodes[i]
        a = (values_nodes[i+1] - b) / nodes[i]
        points.append(a * nodes[i] + b)

    return nodes, points


# Зададим функцию в 5 узлах
plt.subplot(1, 2, 1)
lag_x, lag_y = lagrange(5)
plt.plot(lag_x, lag_y)
plt.title("Полином Лагранжа для 5 узлов")

plt.subplot(1, 2, 2)
lin_x, lin_y = linear(5)
plt.plot(lin_x, lin_y)
plt.title("Кусочно-линейная функция для 5 узлов")
plt.show()

print(" - Погрешности для 5 узлов")
values_nodes = list(map(lambda x_: round(f(x_), 2), lag_x))
approximate_value = [(round((values_nodes[i] - values_nodes[i-1]) / 2, 3) + values_nodes[i-1]) for i in range(1, len(values_nodes))]
approximate_value.append(round(values_nodes[-1] - values_nodes[-2], 3))
print(" Полином Лагранжа |f(x)-L(x)|:", [abs(approximate_value[i]-lag_y[i]) for i in range(len(values_nodes))])
print(" Кусочно-линейная |f(x)-g(x)|:", [abs(approximate_value[i]-lin_y[i]) for i in range(len(values_nodes))])

"---------------------------------------------"

# Зададим функцию в 7 узлах
plt.subplot(1, 2, 1)
lag_x, lag_y = lagrange(7)
plt.plot(lag_x, lag_y)
plt.title("Полином Лагранжа для 7 узлов")

plt.subplot(1, 2, 2)
lin_x, lin_y = linear(7)
plt.plot(lin_x, lin_y)
plt.title("Кусочно-линейная функция для 7 узлов")
plt.show()

print(" - Погрешности для 7 узлов")
values_nodes = list(map(lambda x_: round(f(x_), 2), lag_x))
approximate_value = [(round((values_nodes[i] - values_nodes[i-1]) / 2, 3) + values_nodes[i-1]) for i in range(1, len(values_nodes))]
approximate_value.append(round(values_nodes[-1] - values_nodes[-2], 3))
print(" Полином Лагранжа |f(x)-L(x)|:", [round(abs(approximate_value[i]-lag_y[i]), 3) for i in range(len(values_nodes))])
print(" Кусочно-линейная |f(x)-g(x)|:", [round(abs(approximate_value[i]-lin_y[i]), 3) for i in range(len(values_nodes))])

"---------------------------------------------"

# Зададим функцию в 10 узлах
plt.subplot(1, 2, 1)
lag_x, lag_y = lagrange(10)
print(lag_x, lag_y)
plt.plot(lag_x, lag_y)
plt.title("Полином Лагранжа для 10 узлов")

plt.subplot(1, 2, 2)
lin_x, lin_y = linear(10)
plt.plot(lin_x, lin_y)
plt.title("Кусочно-линейная функция для 10 узлов")
plt.show()

print(" - Погрешности для 10 узлов")
values_nodes = list(map(lambda x_: round(f(x_), 2), lag_x))
approximate_value = [(round((values_nodes[i] - values_nodes[i-1]) / 2, 3) + values_nodes[i-1]) for i in range(1, len(values_nodes))]
approximate_value.append(round(values_nodes[-1] - values_nodes[-2], 3))
print(" Полином Лагранжа |f(x)-L(x)|:", [round(abs(approximate_value[i]-lag_y[i]), 3) for i in range(len(values_nodes))])
print(" Кусочно-линейная |f(x)-g(x)|:", [round(abs(approximate_value[i]-lin_y[i]), 3) for i in range(len(values_nodes))])

"---------------------------------------------"

# Зададим функцию на всем промежутке
nodes = [i for i in range(begin, end+1)]
print(nodes)
values_nodes1 = list(map(lambda x_: round(f(x_), 2), nodes))  # функция и ее y_i
L = list()
for x in nodes:
    L_x = 0
    for i in range(len(nodes)):
        p = 1
        for j in range(len(nodes)):
            if i != j:
                p *= (x - nodes[j])/(nodes[i] - nodes[j])
        L_x += p*values_nodes1[i]
    L.append(L_x)

plt.subplot(1, 2, 1)
plt.plot(nodes, L)
plt.title("Полином Лагранжа всего промежутка")


values_nodes2 = list(map(lambda x_: round(f(x_), 2), nodes))  # функция и ее y_i
values_nodes2.append(round(f(end+1), 2))
points = list()
for i in range(len(nodes)):
    b = values_nodes2[i+1] - (values_nodes2[i+1] - values_nodes2[i]) / nodes[i]
    a = (values_nodes2[i+1] - b) / nodes[i]
    points.append(a * nodes[i] + b)
plt.subplot(1, 2, 2)
plt.plot(nodes, points)
plt.title("Кусочно-линейная функция для всего промежутка")
plt.show()


