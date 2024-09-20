//CMatrix.h
#pragma once
#include <cmath>
#include <vector>
#include <string>
#include <sstream>
#include <iostream>
class Matrix
{
public:
    Matrix();
    Matrix(const int m, const int n, const std::vector<double>& array = std::vector<double>(0));
    Matrix(const std::vector<std::vector<double>>& values) : matrix(values) {}
    ~Matrix();

    std::string toString() const;
    const Matrix& transpose() const;
    friend std::ostream& operator<< (std::ostream& os, const Matrix& matrix);
    double& at(const size_t& m, const size_t& n);
    const double& at(const size_t& m, const size_t& n) const;
    
    const size_t& getLength() const;
    const size_t& getWidth() const;
    Matrix operator*(const Matrix& other) const;
    const std::vector<double>& operator[](const size_t& m) const;
    std::vector<double>& operator[](const size_t& m);
    Matrix simpleIterationMethod(const Matrix& b, int maxIterations, double tolerance) const;
    Matrix gaussSeidelMethod(const Matrix& b, int maxIterations, double tolerance) const;
    static Matrix identity(size_t n)
    {
        std::vector<std::vector<double>> values(n, std::vector<double>(n, 0.0));
        for (size_t i = 0; i < n; ++i)
        {
            values[i][i] = 1.0;
        }
        return Matrix(values);
    }
private:
    std::vector<std::vector<double>> matrix;
};

