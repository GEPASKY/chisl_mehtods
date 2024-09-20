# даны значения
x0 = 0.724
y0 = 0.90000

x1 = 0.725
y1 = 0.89957

x2 = 0.726
y2 = 0.89914

x3 = 0.727
y3 = 0.89870

x4 = 0.728
y4 = 0.89825

x = [x0, x1, x2, x3, x4]
y = [y0, y1, y2, y3, y4]


derivatives = dict()
for i in range(5):
    first_derivative_two = (y[i+1] - y[i]) / (x[i+1] - x[i])
    if i == len(x) - 2:
        first_derivative_three = (y[i-2] - 4*y[i-1] + 3*y[i]) / (2*(x[i+1] - x[i]))
        second_derivative = (y[i-1] - 2*y[i] + y[i+1]) / (x[i+1] - x[i]) ** 2
        derivatives[i] = [round(first_derivative_two, 5), round(first_derivative_three, 5), round(second_derivative, 5)]
        break
    first_derivative_three = (-3*y[i] + 4*y[i+1] - y[i+2]) / (2*(x[i+1] - x[i]))
    second_derivative = (y[i] - 2*y[i+1] + y[i+2]) / (x[i+1] - x[i])**2
    derivatives[i] = [round(first_derivative_two, 5), round(first_derivative_three, 5), round(second_derivative, 5)]

for key, value in derivatives.items():
    print("Узел x{0}: первая двухточечная производная {1[0]}, первая трехточечная производная {1[1]}, вторая"
          " производная {1[2]}".format(key, value))
