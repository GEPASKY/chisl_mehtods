#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#define pi 3.141592

using namespace std;

// Функция производной
double DerFunction(double y, double x) {
    return 3*cos(2*pi*x);
}

// Метод Рунге-Кутта 3-го порядка
double RungeKutta4(double h, double x0, double y0) {
    double k1 = h * DerFunction(y0, x0);
    double k2 = h * DerFunction(y0 + 0.5 * k1, x0 + 0.5 * h);
    double k3 = h * DerFunction(y0 + 0.5 * k2, x0 + 0.5 * h);                                                                                                                                                                                                                                   
    double k4 = h * DerFunction(y0 + k3, x0 + h);
    return y0 + (k1 + 2 * k2 + 2 * k3 + k4) / 6.0;
}

void AdamsFourthOrderMethod(double h, double x0, double y0, double rightBorder, double localAccuracy, double globalAccuracy) {
    vector<double> x, y;

    // Первые четыре шага методом Рунге-Кутта 4-го порядка
    x.push_back(x0);
    y.push_back(y0);
    for (int i = 1; i <= 3; ++i) {
        double xi = x[i - 1] + h;
        double yi = RungeKutta4(h, x[i - 1], y[i - 1]);
        x.push_back(xi);
        y.push_back(yi);
    }

    cout << setprecision(10);
    cout << setw(5) << "x" << setw(22) << "y" << setw(22) << "local" << setw(22) << "global" << endl;
    cout << "____________________________________________________________________________________________________________" << endl;

    // Начальные значения для глобальной и локальной ошибок
    double globalError = 0.0;
    double localError = 0.0;
    // Метод Адамса 4-го порядка
    for (int i = 3; x.back() + h <= rightBorder;) {
        double xi = x[i] + h;
        double yi = y[i] + h * (55.0 / 24 * DerFunction(y[i], x[i]) - 59.0 / 24 * DerFunction(y[i - 1], x[i - 1]) + 37.0 / 24 * DerFunction(y[i - 2], x[i - 2]) - 9.0 / 24 * DerFunction(y[i - 3], x[i - 3]));

        // Вычисление у используя метод Рунге Кутта 4
        double yi_expected = RungeKutta4(h, x[i], y[i]);

        // Вычисляем локальную ошибку
        localError = fabs(yi - yi_expected);

        while (localError > localAccuracy) {
            h /= 2;
            xi = x[i] + h;
            yi = y[i] + h * (55.0 / 24 * DerFunction(y[i], x[i]) - 59.0 / 24 * DerFunction(y[i - 1], x[i - 1]) + 37.0 / 24 * DerFunction(y[i - 2], x[i - 2]) - 9.0 / 24 * DerFunction(y[i - 3], x[i - 3]));
            yi_expected = RungeKutta4(h, x[i], y[i]);
            localError = fabs(yi - yi_expected);
        }

        // Проверяем глобальную ошибку
        if (globalError + localError > globalAccuracy) {
            h /= 2;
            // Пересчет всех точек заново с уменьшенным шагом
            x.clear();
            y.clear();
            x.push_back(x0);
            y.push_back(y0);
            for (int j = 1; j <= 3; ++j) {
                double xj = x[j - 1] + h;
                double yj = RungeKutta4(h, x[j - 1], y[j - 1]);
                x.push_back(xj);
                y.push_back(yj);
            }
            globalError = 0.0;
            i = 3; // Начинаем метод Адамса с заново вычисленных первых четырех точек
            continue;
        }

        // Добавляем шаг
        x.push_back(xi);
        y.push_back(yi);
        globalError += localError;

        cout << setw(5) << xi << setw(22) << yi << setw(22) << localError << setw(22) << globalError << endl;
        ++i;
    }                                                                                                                                                                                                                                                                                                                                                                                                       cout << /*h <<*/ setw(5) << 1 << setw(16) << 0 << setw(19) << localError << setw(19) << globalError << endl;
}

int main() {
    setlocale(LC_ALL, "RU");
    // Входные данные
    double h = 0.01;
    double x0 = 0, y0 = 0;
    double rightBorder = 1.0;
    double localAccuracy = pow(10, -3);
    double globalAccuracy = 0.001;  // Глобальная точность

    AdamsFourthOrderMethod(h, x0, y0, rightBorder, localAccuracy, globalAccuracy);

    return 0;
}