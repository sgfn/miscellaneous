#pragma once

#include <functional>


using f_1d = std::function<double(double)>;

class FEMheatEq {
private:
    // Element amount constraints
    static constexpr int kMinAllowedN = 3;
    static constexpr int kMaxAllowedN = 10000;

    // Gauss-Legendre quadrature point (1/sqrt(3))
    static constexpr double g2p_pt = 0.57735026918962576451;

    // Problem-specific constants & functions
    static constexpr double l = 2.0;
    static constexpr double u_l = 0.0;
    static constexpr double bet_0 = -1.0;
    static constexpr double gam_0 = -20.0;
    static inline double k(double x) { return (x < 0.0 || x > 2.0) ? 0.0 : (x <= 1.0) ? 1.0 : 2.0; };

    /**
     * Integrate a given function using Gaussian two-point quadrature
     * @param x1 left endpoint
     * @param x2 right endpoint
     * @param f integrand
     * @return approximation to integral of f from x1 to x2
     */
    static double int_gauss_2p(double x1, double x2, f_1d& f);

    // Amount of elements used
    int N;

    bool done = false;
    bool fail = false;

    // Basis (test) functions and their derivatives
    std::vector<f_1d> basis_funs {};
    std::vector<f_1d> basis_fun_derivatives {};
    std::vector<std::string> basis_fun_strs {};
    // Computed solution
    std::vector<double> basis_fun_weights {};

    /**
     * Create the appropriate basis function for a given index
     * @param i
     */
    f_1d basis_fun(int i);

    /**
     * Create the derivative of the appropriate basis function for a given index
     * @param i
     */
    f_1d basis_fun_derivative(int i);

    /**
     * Get string representation of the basis function for a given index
     * @param i
     */
    std::string basis_fun_str(int i);

    /**
     * Generate and store basis functions, their derivatives and string representations
     * for later use
     */
    void generate_basis_funs();


    /**
     * Compute B(u, v) for basis functions at indices i, j
     * @param i
     * @param j
     */
    double B(int i, int j);

    /**
     * Compute L(v) for basis function at index i
     * @param i
     */
    double L(int i);

public:
    /**
     * Construct a FEMheatEq object with n elems
     * @param n
     */
    FEMheatEq(int n);

    /**
     * Construct a FEMheatEq object with minimal allowed amount of elems
     */
    FEMheatEq() : FEMheatEq(kMinAllowedN) {};

    /**
     * Attempt to solve the equation
     * @return true if solve was successful, false otherwise
     */
    bool solve();

    /**
     * Get string representation of computed solution, to be used in gnuplot.
     * Returns empty string if solve failed/not yet attempted
     * @return gnuplot command string
    */
    std::string to_gnuplot_str();
};
