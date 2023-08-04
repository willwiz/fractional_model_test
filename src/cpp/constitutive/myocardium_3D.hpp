#pragma once

#include "../kinematics/kinematics.hpp"
#include "interfaces.hpp"

namespace constitutive_models {
  class Myocardium: public MatLawInterface<9>
  {
    protected:
      double b1, b2;
      double kff, kss, knn;
      double kfs, kfn, ksn;
    public:

      double mxm[9], nxn[9], zxz[9], mxn[9], mxz[9], nxz[9];

      Myocardium();
      Myocardium(double b1, double b2, double kff, double kss, double knn, double kfs, double kfn, double ksn, double fiber[]);
      ~Myocardium();

      void set_pars(double b1, double b2, double kff, double kss, double knn, double kfs, double kfn, double ksn, double fiber[]);
      double stress(const kinematics::kinematics<9> &kin, double stress[9]);
      void stress(double args[], double stress[9]);
  };

}