#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <muParser.h>
#include <fstream>

constexpr auto e = 2.7182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274;
constexpr auto M_PI = 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679;

// Структура для хранения результата
struct Result {
    double x;
    double y;
    double e_local;
    double e_global;
};

// Функция для вычисления значения выражения
double evaluate_expression(mu::Parser& parser, double x, double y) {
    parser.DefineVar("x", &x);
    parser.DefineVar("y", &y);
    return parser.Eval();
}

// Функция для одного шага метода Рунге-Кутты третьего порядка
double rk3_step(mu::Parser& parser, double x, double y, double h) {
    double k1 = h * evaluate_expression(parser, x, y);
    double k2 = h * evaluate_expression(parser, x + h / 2, y + k1 / 2);
    double k3 = h * evaluate_expression(parser, x + h, y - k1 + 2 * k2);
    return y + (k1 + 4 * k2 + k3) / 6;
}

// Функция для выполнения метода Рунге-Кутты третьего порядка с контролем ошибок
std::vector<Result> rk3_with_error_control(std::string& f, double x0, double y0, double x_end, double h, double tol) {
    mu::Parser parser;
    parser.DefineConst("e", e);
    parser.DefineConst("pi", M_PI);
    parser.SetExpr(f);

    std::vector<Result> table;
    double x = x0;
    double y = y0;
    double e_global = 0;
    table.push_back({ x, y, 0, 0 });

    while (x < x_end) {
        if (x + h > x_end) {
            h = x_end - x;
        }

        double y_temp = y;
        double h_temp = h;
        double e_local = 0.0;
        double y_new;

        do {
            y_new = rk3_step(parser, x, y_temp, h_temp);
            double y_half_step = rk3_step(parser, x, y_temp, h_temp / 2);
            y_half_step = rk3_step(parser, x + h_temp / 2, y_half_step, h_temp / 2);

            e_local = std::abs(y_half_step - y_new);
            if (e_local >= tol) {
                h_temp *= 0.5;
            }
        } while (e_local > tol);

        e_global += e_local;

        if (e_global >= tol) {
            h *= 0.5;
            e_global -= e_local;
            continue;
        }

        x += h_temp;
        y = y_new;
        table.push_back({ x, y, e_local, e_global });
    }

    return table;
}

int main() {
    setlocale(LC_ALL, "rus");

    std::ofstream Xout("X.txt");
    std::ofstream Yout("Y1.txt", std::ios::trunc);

    try {
        // Начальные условия и параметры
        double x0 = 0, y0 = 0, x_end = 0, h = 0, tol = 0;
        std::string f;

        std::cout << "Введите правую часть f: ";
        getline(std::cin, f);
        std::cout << "Введите x0, y0 и x_end: ";
        std::cin >> x0 >> y0 >> x_end;
        std::cout << "Введите точность tol: ";
        std::cin >> tol;
        std::cout << "Введите шаг h: ";
        std::cin >> h;

        // Запуск метода Рунге-Кутты третьего порядка с контролем ошибок
        std::vector<Result> results = rk3_with_error_control(f, x0, y0, x_end, h, tol);

        // Вывод таблицы результатов
        std::cout << std::fixed << std::setprecision(15);
        std::cout << "X[i]\t\t\tY[i]\t\t\tE(лок)\t\t\tE(глобал)" << std::endl;
        for (const auto& result : results) Xout << result.x << std::endl;
        for (const auto& result : results) Yout << result.y << std::endl;

        Xout.close();
        Yout.close();
        // system("main1.py");
        for (const auto& result : results) {
            std::cout << result.x << "\t" << result.y << "\t" << result.e_local << "\t" << result.e_global << std::endl;
        }
    }
    catch (mu::Parser::exception_type e) {
        std::cout << "Ошибка! " << e.GetMsg() << std::endl;
    };
    return 0;
}