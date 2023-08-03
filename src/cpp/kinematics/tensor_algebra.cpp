#include "tensor_algebra.hpp"

namespace constitutive_models {

/* ------------------------------------------------------------------------------
 |  Small tools, addto is obsolete after code optimization.
 |
 |  Author: Will Zhang
 |  Dependencies: None
 ----------------------------------------------------------------------------- */

  const double id2d[4] = {1,0,0,1};

  template<int dim>
  inline double ddot(const double a[dim], const double b[dim]) {
    double val = 0;
    for (int i = 0; i < dim; i++)
    {
      val = val + a[i]*b[i];
    }
    return val;
  }

  void addto( const double a[], double b[], int dim) {
    for (int i = 0; i < dim; i++)
    {
      b[i] = a[i] + b[i];
    }
  }
}
