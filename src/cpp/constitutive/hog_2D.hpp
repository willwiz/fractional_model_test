#pragma once

#include "../kinematics/kinematics.hpp"
#include "interfaces.hpp"

namespace constitutive_models {

  class Hog2D: public MatLawInterface<4>
  {
  public:
    double k1, k2;
    double m[4];
    double E1;
    double E2;

    Hog2D();
    ~Hog2D();
    Hog2D(double k1, double k2, double theta);
    Hog2D(double k1, double k2, double theta, double Cmax[]);

    void set_pars(double k1, double k2, double theta);
    void set_pars(double k1, double k2, double theta, double Cmax[]);
    double get_scaled_modulus();
    double stress(const kinematics::kinematics<4> &kin, double stress[4]);
    void stress(double args[4], double stress[4]);
  };

}
