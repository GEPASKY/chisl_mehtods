//CMatrix.cpp
#include "CMatrix.h"

Matrix::Matrix()
{
}

Matrix::Matrix(const int m, const int n, const std::vector<double>& array)
{
    if (m <= 0 || n <= 0) {
        throw std::invalid_argument("Matrix dimensions must be positive");
    }

    if (!array.empty()) {
        if (array.size() < static_cast<size_t>(m) * n) {
            throw std::invalid_argument("Insufficient data in the array for matrix initialization");
        }

        for (int i = 0; i < m; i++)
        {
            matrix.emplace_back(array.begin() + i * n, array.begin() + (i + 1) * n);
        }
    }
    else
    {
        matrix.resize(m, std::vector<double>(n));
    }
}


Matrix::~Matrix()
{
}

std::string Matrix::toString() const
{

    std::stringstream os;
    for (size_t i = 0; i < matrix.size(); i++)
    {
        for (size_t j = 0; j < matrix[i].size(); j++)
        {
            os << matrix[i][j] << ' ';
        }
        os << std::endl;
    }
    return os.str();
}

std::ostream& operator<<(std::ostream& os, const Matrix& matrix)
{
    for (size_t i = 0; i < matrix.matrix.size(); i++)
    {
        for (size_t j = 0; j < matrix.matrix[i].size(); j++)
        {
            os << matrix.matrix[i][j] << ' ';
        }
        os << std::endl;
    }
    return os;
}

const Matrix& Matrix::transpose() const
{
    Matrix transposed(matrix.size(), matrix[0].size());

    for (size_t i = 0; i < matrix.size(); i++)
    {
        for (size_t j = 0; j < matrix[i].size(); j++)
        {
            transposed.at(j,i) = matrix[i][j];
        }
    }

    return transposed;
}
double& Matrix::at(const size_t& m, const size_t& n)
{
    return matrix[m][n];
}
const double& Matrix::at(const size_t& m, const size_t& n) const
{
    return matrix[m][n];
}

std::vector<double>& Matrix::operator[](const size_t& m)
{
    return matrix[m];
}

const size_t& Matrix::getLength() const
{
    return matrix.size();
}

const size_t& Matrix::getWidth() const
{
    if (!matrix.empty())
    {
        return matrix[0].size();
    }
    return 0;
}
Matrix Matrix::operator*(const Matrix& other) const
{
    size_t m1 = getLength();
    size_t n1 = getWidth();
    size_t m2 = other.getLength();
    size_t n2 = other.getWidth();

    if (n1 != m2)
    {
        throw std::invalid_argument("Invalid matrix dimensions for multiplication");
    }

    Matrix result(m1, n2);

    for (size_t i = 0; i < m1; ++i)
    {
        for (size_t j = 0; j < n2; ++j)
        {
            for (size_t k = 0; k < n1; ++k)
            {
                result.at(i, j) += at(i, k) * other.at(k, j);
            }
        }
    }

    return result;
}
#include "CMatrix.h"

Matrix Matrix::simpleIterationMethod(const Matrix& b, int maxIterations, double tolerance) const {
    size_t n = getWidth();
    Matrix x(n, 1, std::vector<double>(n, 0.0));

    for (int iteration = 0; iteration < maxIterations; ++iteration) {
        Matrix x_new(n, 1, std::vector<double>(n, 0.0));

        for (size_t i = 0; i < n; ++i) {
            double sum = 0.0;
            for (size_t j = 0; j < n; ++j) {
                sum += at(i, j) * x[j][0];
            }
            x_new[i][0] = (b[i][0] - sum) / at(i, i);
        }
        double error = 0.0;
        for (size_t i = 0; i < n; ++i) {
            error += pow(x_new[i][0] - x[i][0], 2);
        }

        if (sqrt(error) < tolerance) {
            std::cout << "Метод простых итераций сошелся после " << iteration + 1 << " итераций.\n";
            return x_new;
        }

        x = x_new;
    }

    std::cout << "Метод простых итераций не сошелся за заданное количество итераций.\n";
    return x;
}
Matrix Matrix::gaussSeidelMethod(const Matrix& b, int maxIterations, double tolerance) const {
    size_t n = getWidth();
    Matrix x(n, 1, std::vector<double>(n, 0.0)); // Начальное приближение

    for (int iteration = 0; iteration < maxIterations; ++iteration) {
        Matrix x_new(n, 1, std::vector<double>(n, 0.0));

        for (size_t i = 0; i < n; ++i) {
            double sum1 = 0.0;
            double sum2 = 0.0;

            for (size_t j = 0; j < i; ++j) {
                sum1 += at(i, j) * x_new[j][0];
            }

            for (size_t j = i + 1; j < n; ++j) {
                sum2 += at(i, j) * x[j][0];
            }

            x_new[i][0] = (b[i][0] - sum1 - sum2) / at(i, i);
        }

        double error = 0.0;
        for (size_t i = 0; i < n; ++i) {
            error += pow(x_new[i][0] - x[i][0], 2);
        }

        if (sqrt(error) < tolerance) {
            std::cout << "Метод Гаусса-Зейделя сошелся после " << iteration + 1 << " итераций.\n";
            return x_new;
        }

        x = x_new;
    }

    std::cout << "Метод Гаусса-Зейделя не сошелся за заданное количество итераций.\n";
    return x;
}

const std::vector<double>& Matrix::operator[](const size_t& m) const
{
    return matrix[m];
}



