from math import log, trunc, sqrt, hypot

# Часть 1
# Пункт 1
print("Проверка условий применимости метода итераций.")


for x in range(-1000, 1000, 1):
    fi_diff = abs((pow(4,x)*log(4))/((9-pow(4,x))*log(5)))

    if fi_diff > 1:
        print("- Значение модуля производной функции слева становится > 1 от x =", x)
        print(fi_diff)
        break

print()

for x in range(100, -1000, -1):
    fi_diff = abs((pow(4,x)*log(4))/((9-pow(4,x))*log(5)))

    if fi_diff > 1:
        print("- Значение модуля производной функции справа становится > 1 от x =", x)
        print(fi_diff)
        break

# Пункт 2,3
# начальное приближение
print("Метод Ньютона.")
# диапазон x0 [0, 441]
x0 = 100
x_old = x0
# счётчик итераций
counter = 1
# для производной
dx = pow(10, -10)

while counter < 1000:
    f_x = pow(5, x_old) - pow(4, x_old) - 9
    f_x_diff = ((pow(5, x_old + dx) - pow(4, x_old + dx) - 9) - f_x) / dx
    
    x_new = x_old - f_x / f_x_diff
    
    # критерий остановки
    if abs(x_new - x_old) < pow(10,-4):
        print(" - Начальное приближение:", x0)
        print(" - Кол-во итераций:", counter)
        print(" - Ответ:", x_new)
        print(" - Область сходимости для нач. приближ: [-2, 214]")
        break

    x_old = x_new
    counter += 1
else:
    print("- Слишком много итераций...")


# Часть 3
print("Метод Ньютона для систем.")
# начальное приближение
x0,y0 = 1.5, 4

# достаточное условие
df_dx = 3*(x0**2)
df_dy = 3*(y0**2)
dg_dx = 2*x0
dg_dy = 2*y0
# проверка знаменателя на неравность нулю
denumerator = df_dx*dg_dy - df_dy*dg_dx

if (denumerator != 0):
    print(" - Необходимое условие выполняется: df_dx*dg_dy-df_dy*dg_dx =", denumerator)
else:
    print(" - Необходимое условие НЕ выполняется: df_dx*dg_dy-df_dy*dg_dx =", denumerator)

# счётчик итераций
counter = 1
# начальное приближение
x_old, y_old = x0, y0

# итерационный процесс
while counter < 500:
    # коэффициенты 
    a11 = 3*(x_old**2)
    a12 = 3*(y_old**2)
    a21 = 2*x_old
    a22 = 2*y_old

    b1 = -(x_old**3 + y_old*3 -35) + a11 * x_old + a12 * y_old
    b2 = -(x_old**2 + y_old**2 - 13) + a21 * x_old + a22 * y_old
    
    
    if (a11*a22-a21*a12) == 0:
        print("Знаменатель равн нулю. Остановка.")
        break

    # Xk+1, Yk+1
    x_new = (b1*a22-b2*a12)/(a11*a22-a21*a12)
    y_new = (b2*a11-b1*a21)/(a11*a22-a21*a12)

    # print("[DEBUG] Xk+1,Yk+1:",x_new, y_new)
    
    # счётчик итераций
    counter += 1

    
    # критерий остановки
    if hypot(x_new-x_old, y_new-y_old) < pow(10,-4):
        print(" - Кол-во итераций:", counter)
        print(" - Ответ:", x_new, "|", y_new)
        break
    
    
    x_old, y_old = x_new, y_new
    
else:
    print("- Слишком много итераций...")

