import numpy as np
from math import sqrt, pow
import matplotlib.pyplot as plt

# точные решения
ans = [89/170, 167/170, 419/510, -311/510]

""" Нахождение числа обусловленности матрицы СЛАУ """
# матрица A из коэффициентов СЛАУ (Ax = b) (МОЖНО ИЗМЕНИТЬ)
A = np.array([[5, 1, 4, 4], [8, 9, 6, 9], [6, 0, 2, 0], [1, 12, 1, 3]])

# матрица ответов СЛАУ (Ax = b) (МОЖНО ИЗМЕНИТЬ)
b = np.array([[3], [5], [3], [2]])

# обратная матрица к А
rev_A = np.linalg.inv(A)

# 1. Вычисление нормы матрицы через собств. знач.
def Enorm(A):
    # транспонированная матрица А
    A_trans = A.transpose()

    # матрица произведение А x А_транспон.
    multi = np.dot(A_trans, A)

    # собственные значения multi
    eigenvalues = np.linalg.eig(multi)[0]

    # вычисление нормы для А
    norm_1 = sqrt(max(eigenvalues))

    return norm_1

# вычисление числа обусловленности
cond_number_1 = Enorm(A) * Enorm(rev_A)


# 2. Вычисление нормы по формуле (2).
def Snorm(A):
    string_values = []

    # проходимся по каждой строчке матрицы и считаем её сумму
    for string in range(A.shape[0]):
        string_sum = 0
        
        for column in range(A.shape[1]):
            string_sum += abs(A[string][column])

        string_values.append(string_sum)

    # вычисление норм и числа обусловленности
    norm_2 = max(string_values)
    
    return norm_2
    
cond_number_2 = Snorm(A) * Snorm(rev_A)


# 3. Вычисление нормы по формуле (3).
def Cnorm(A):
    column_values = []

    for column in range(A.shape[1]):
        column_sum = 0
        
        for string in range(A.shape[0]):
            column_sum += abs(A[string][column])

        column_values.append(column_sum)

    # вычисление норм и числа обусловленности
    norm_3 = max(column_values)

    return norm_3


cond_number_3 = Cnorm(A) * Cnorm(rev_A)

# вывод
print("• Нахождение числа обусловленности матрицы СЛАУ")
print("- Матрица A\n", A, "\n- Её числа обусловленности:", cond_number_1, ",", cond_number_2, ",", cond_number_3)


""" Метод простой итерации """
print("\n• Решение СЛАУ методом простой итерации")
# устанавливаем таy (МОЖНО ИЗМЕНИТЬ)
tay = 0.05
print("- Тау =", tay)
# достаточное условие
# матрица E-tA
EtA = np.eye(A.shape[0]) - tay * A
# норма E-tA
EtA_norm = [Enorm(EtA), Snorm(EtA), Cnorm(EtA)]

for i in range(3):
    print(f"- Норма {i+1}:")
    if EtA_norm[i] < 1:
        print("  Достаточное условие выполняется")
        print("  ||E - t*A|| = ", EtA_norm[i])
    else:
        print("  Достаточное условие НЕ выполняется")
        print("  ||E - t*A|| = ", EtA_norm[i])

# критерий сходимости
eigenvalues_EtA = np.linalg.eig(EtA)[0]

for val in eigenvalues_EtA:
    if abs(val) < 1:
        print("- Критерий сходимости выполняется")
        print("  Собств. знач:", eigenvalues_EtA)
        break
else:
    print("- Критерий сходимости НЕ выполняется")
    print("  Собств. знач:", eigenvalues_EtA)

# устанавливаем параметры 
prec_values = [pow(10, -2), pow(10, -3), pow(10, -4)]
x0 = np.array([
    [[pow(10,-1)], [pow(10,-1)], [pow(10,-1)], [pow(10,-1)]],
    [[pow(10,-2)], [pow(10,-2)], [pow(10,-2)], [pow(10,-2)]],
    [[pow(10,-3)], [pow(10,-3)], [pow(10,-3)], [pow(10,-3)]],
    ]) # (МОЖНО ИЗМЕНИТЬ)
counter = 0

# для графиков
x_axis = []
y_axis = []

# метод итерации
for i in range(3):
    # точность
    prec = prec_values[i]
    
    for k in range(3):
        # начальное приближение
        x_old = x0[k][:][:]
        
        while counter < 10000:
            counter += 1
            x_new = np.dot(EtA, x_old) + tay * b
            
            if (np.linalg.norm(x_new-x_old) < prec):
                print(f" {i+1}.{k+1})Кол-во итераций", counter, "\n", "точность", prec, "\n", "начальное приближение", x0[k][0][0])
                print(" Приблизительный ответ:\n", x_new, "\n")
                x_axis.append(np.linalg.norm(ans - x0[k][0][0]))
                y_axis.append(counter)
                break
            
            x_old = x_new
        else:
            print("...\n Слишком большое кол-во итераций!")
            
    plt.plot(x_axis, y_axis, marker='o', markersize=7)
    plt.legend (("0.1","0.01","0.001"))
    x_axis.clear()
    y_axis.clear()
    
# построение графика
plt.xlabel('Норма разности') # Подпись для оси х
plt.ylabel('Кол-во итераций') # Подпись для оси y
plt.title('Метод простой итерации') #Название
plt.show()

""" Метод Якоби """
print("\n• Решение СЛАУ методом Якоби")
D = A * np.eye(A.shape[0], dtype="int32")

L_eye = np.array([[0,0,0,0], [1,0,0,0], [1,1,0,0], [1,1,1,0]])
L = A * L_eye

U_eye = np.array([[0,1,1,1], [0,0,1,1], [0,0,0,1], [0,0,0,0]])
U = A * U_eye

# проверка достаточного условия
for string in range(A.shape[0]):
    str_sum = 0
    diag_value = A[string][string]
    
    for column in range(A.shape[1]):
        if column != string:
            str_sum += A[string][column]

    if not diag_value > str_sum:
        print("- Достаточное условие НЕ выполняется")
        break
    
else:
    print("- Достаточное условие выполняется")

# критерий сходимости
check_matrix = -np.dot(np.linalg.inv(D),(L+U))
# собств. знач.
check_matrix_eig = np.linalg.eig(check_matrix)[0]
# проверка
for val in check_matrix_eig:
    if abs(val) <= 1:
        print("- Критерий сходимости выполняется")
        print("  Собств. знач:", check_matrix_eig)
        break
else:
    print("- Критерий сходимости НЕ выполняется")
    print("  Собств. знач:", check_matrix_eig)
    
# для графиков
x_axis = []
y_axis = []

# метод Якоби
counter = 0
for i in range(3):
    prec = prec_values[i]
    
    for k in range(3):
        x_old = x0[k][:][:]
        
        while counter < 5000:
            counter += 1
            # обратная матрица к D
            rev_D = np.linalg.inv(D)
            x_new = np.dot(rev_D, (b-np.dot((L+U), x_old)))
            
            if (np.linalg.norm(x_new-x_old) < prec):
                print(f" {i+1}.{k+1})Кол-во итераций", counter, "\n", "точность", prec, "\n", "начальное приближение", x0[k][0][0])
                print(" Приблизительный ответ:\n", x_new, "\n")
                x_axis.append(np.linalg.norm(ans - x0[k][0][0]))
                y_axis.append(counter)
                break
            
            x_old = x_new
        else:
            print("...\n Слишком большое кол-во итераций!")
            
    plt.plot(x_axis, y_axis, marker='o', markersize=7)
    plt.legend (("0.1","0.01","0.001"))
    x_axis.clear()
    y_axis.clear()
    
# построение графика
plt.xlabel('Норма разности') # Подпись для оси х
plt.ylabel('Кол-во итераций') # Подпись для оси y
plt.title('Метод Якоби') #Название
plt.show()

""" Метод Гаусса-Зейделя """
print("\n• Решение СЛАУ методом Гаусса-Зейделя")
# достаточное усл. не проверяем, а критерий - да
check_matrix_2 = - np.dot((np.linalg.inv(L+D)), U)
check_matrix_2_eig = np.linalg.eig(check_matrix_2)[0]

for val in check_matrix_2_eig:
    if abs(val) <= 1:
        print("- Критерий сходимости выполняется")
        print("  Собств. знач:", check_matrix_2_eig)
        break
else:
    print("- Критерий сходимости НЕ выполняется")
    print("  Собств. знач:", check_matrix_2_eig)

# для графиков
x_axis = []
y_axis = []

# метод Гаусса-Зейделя
counter = 0
for i in range(3):
    prec = prec_values[i]

    for k in range(3):
        x_old = x0[k][:][:]
        
        while counter < 5000:
            counter += 1
            # обратная матрица к D
            rev_D = np.linalg.inv(D)
            x_new = np.dot((np.linalg.inv(L+D)), b) - np.dot((np.linalg.inv(L+D)),(np.dot(U, x_old)))
            
            if (np.linalg.norm(x_new-x_old) < prec):
                print(f" {i+1}.{k+1})Кол-во итераций", counter, "\n", "точность", prec, "\n", "начальное приближение", x0[k][0][0])
                print(" Приблизительный ответ:\n", x_new, "\n")
                x_axis.append(np.linalg.norm(ans - x0[k][0][0]))
                y_axis.append(counter)
                break
            
            x_old = x_new
        else:
            print("...\n Слишком большое кол-во итераций!")

    plt.plot(x_axis, y_axis, marker='o', markersize=7)
    plt.legend (("0.1","0.01","0.001"))
    x_axis.clear()
    y_axis.clear()

# построение графика
plt.xlabel('Норма разности') # Подпись для оси х
plt.ylabel('Кол-во итераций') # Подпись для оси y
plt.title('Метод Гаусса-Зейделя') #Название
plt.show()
