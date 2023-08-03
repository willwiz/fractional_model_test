#pragma once

namespace constitutive_models {

  extern const double id2d[4];

  template<int dim>
  inline double ddot(const double a[dim], const double b[dim]);

  void addto(const double a[], double b[], int dim);

}
