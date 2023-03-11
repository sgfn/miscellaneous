#include <chrono>
#include <functional>
#include <fstream>

#include <armadillo>

#include "heateq.hh"


FEMheatEq::FEMheatEq(int n) {
    if (n < kMinAllowedN) {
        fprintf(stderr, "Warning: n=%d too small, will use n=%d\n", n, kMinAllowedN);
        n = kMinAllowedN;
    } else if (n > kMaxAllowedN) {
        fprintf(stderr, "Warning: n=%d too big, will use n=%d\n", n, kMaxAllowedN);
        n = kMaxAllowedN;
    }
    this->N = n;
}

double FEMheatEq::int_gauss_2p(double x1, double x2, f_1d& f) {
    const double d = (x2-x1)/2.0;
    const double e = (x1+x2)/2.0;
    return d * (f(d*(-g2p_pt) + e) + f(d*g2p_pt + e));
}

std::string FEMheatEq::basis_fun_str(int i) {
    std::ostringstream oss {};
    const double x_step = l/(this->N-1);
    const double x_i = i*x_step;
    double x_ip1 = x_i + x_step;
    double x_im1 = x_i - x_step;
    if (x_im1 < 0) {
        x_im1 = 0.0;
    }
    if (x_ip1 > l) {
        x_ip1 = l;
    }

    oss << "x<" << x_im1 << "||x>" << x_ip1 << "?0:";
    oss << "x<" << x_i << "?(x-" << x_im1 << ")/" << x_step << ":";
    oss << "(" << x_ip1 << "-x)/" << x_step;
    return oss.str();
}

f_1d FEMheatEq::basis_fun(int i) {
    const double x_step = l/(this->N-1);
    const double x_i = i*x_step;
    double x_ip1 = x_i + x_step;
    double x_im1 = x_i - x_step;
    if (x_im1 < 0) {
        x_im1 = 0.0;
    }
    if (x_ip1 > l) {
        x_ip1 = l;
    }

    return [x_i, x_im1, x_ip1, x_step](double x) {
        if (x < x_im1 || x > x_ip1) {
            return 0.0;
        }

        if (x < x_i) {
            return (x - x_im1) / x_step;
        } else {
            return (x_ip1 - x) / x_step;
        }
    };
}

f_1d FEMheatEq::basis_fun_derivative(int i) {
    const double x_step = l/(this->N-1);
    const double x_i = i*x_step;
    double x_ip1 = x_i + x_step;
    double x_im1 = x_i - x_step;
    if (x_im1 < 0) {
        x_im1 = 0.0;
    }
    if (x_ip1 > l) {
        x_ip1 = l;
    }

    return [x_i, x_im1, x_ip1, x_step](double x) {
        if (x < x_im1 || x > x_ip1) {
            return 0.0;
        }

        if (x < x_i) {
           return 1.0 / x_step;
        } else {
            return -1.0 / x_step;
        }
    };
}

void FEMheatEq::generate_basis_funs() {
    this->basis_funs.reserve(this->N);
    this->basis_fun_derivatives.reserve(this->N);
    this->basis_fun_strs.reserve(this->N);
    this->basis_fun_weights.reserve(this->N);

    for (int i=0; i<this->N; ++i) {
        this->basis_funs.push_back(this->basis_fun(i));
        this->basis_fun_derivatives.push_back(this->basis_fun_derivative(i));
        this->basis_fun_strs.push_back(this->basis_fun_str(i));
    }
}

double FEMheatEq::B(int i, int j) {
    const double x_step = l/(this->N-1);
    const double x_i = i*x_step;
    const double x_j = j*x_step;
    double x_ip1 = x_i + x_step;
    double x_im1 = x_i - x_step;
    if (x_im1 < 0) {
        x_im1 = 0.0;
    }
    if (x_ip1 > l) {
        x_ip1 = l;
    }

    const f_1d& f1 = this->basis_fun_derivatives.at(i);
    const f_1d& f2 = this->basis_fun_derivatives.at(j);
    f_1d integrand = [&f1, &f2](double x) { return f1(x) * f2(x); };

    double int_res = 0;
    if (i == j) {
        int_res = int_gauss_2p(x_im1, x_ip1, integrand);
    } else if (i == j-1) {
        int_res = int_gauss_2p(x_i, x_j, integrand);
    } else if (i-1 == j) {
        int_res = int_gauss_2p(x_j, x_i, integrand);
    }
    return int_res + bet_0 * this->basis_funs.at(i)(0) * this->basis_funs.at(j)(0);
}

double FEMheatEq::L(int i) {
    return gam_0 * this->basis_funs.at(i)(0);
}

bool FEMheatEq::solve() {
    generate_basis_funs();

    const arma::uword n = static_cast<arma::uword>(this->N);
    arma::sp_mat mA(n, n);
    arma::mat mB(n, 1);
    arma::mat mX(n, 1);

    // enforce Dirichlet constraint on right edge
    mA(n-1, n-1) = 1;

    for (int i=0; i<this->N-1; ++i) {
        for (int j=0; j<=i; ++j) {
            mA(j, i) = mA(i, j) = this->B(i, j);
        }
        mB(i, 0) = this->L(i);
    }

    const bool rv = arma::spsolve(mX, mA, mB);
    if (rv) {
        for (int i=0; i<this->N; ++i) {
            this->basis_fun_weights.push_back(mX(i, 0));
        }
    }

    this->done = true;
    this->fail = !rv;
    return rv;
}

std::string FEMheatEq::to_gnuplot_str() {
    if (!this->done || this->fail) {
        fprintf(stderr, "Error: Unable to plot solution\n");
        return std::string {};
    }

    std::ostringstream oss {};
    // initial settings
    oss << "set xrange [-0.1:2.1];";
    oss << "set yrange [-3:43];";
    oss << "set xzeroaxis;set yzeroaxis;";
    oss << "set samples 9001;";

    oss << "u(x)=";
    for (int i=0; i<this->N; ++i) {
        oss << this->basis_fun_weights.at(i);
        oss << "*(" << this->basis_fun_str(i) << ")";
        if (i != this->N-1) {
            oss << "+";
        }
    }
    oss << ";plot u(x) title 'u(x) for n=" << this->N << "'";
    return oss.str();
}

static constexpr auto kDumpFilename { "plot.txt" };

void plot(std::string plot_str) {
    std::string cmd { "gnuplot -p -e \"" + plot_str + "\"" };
    int rc = system(cmd.c_str());
    if (rc != 0) {
        fprintf(stderr, "Warning: gnuplot exited with code %d\n", rc);
        std::ofstream os;
        os.open(kDumpFilename);
        os << plot_str << "\n";
        os.close();
        fprintf(stderr, "Attempting run from dump...\n");
        cmd = std::string { "gnuplot -p " + std::string { kDumpFilename } };
        rc = system(cmd.c_str());
    }
}

int main(int argc, char** argv) {
    const auto t_s = std::chrono::high_resolution_clock::now();

    FEMheatEq fem {};
    if (argc > 1) {
        fem = FEMheatEq { atoi(argv[1]) };
    }

    const bool rv = fem.solve();
    const auto t_e = std::chrono::high_resolution_clock::now();
    const std::chrono::duration<double> t = t_e - t_s;
    printf("Solve %s, took %f s\n", rv ? "successful" : "failed", t.count());
    if (rv) {
        plot(fem.to_gnuplot_str());
    }

    return 0;
}
