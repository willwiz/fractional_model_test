#pragma once

#include "caputo.hpp"
#include "../kinematics/kinematics.hpp"
#include "../constitutive/interfaces.hpp"


namespace constitutive_models
{
  template<int dim>
  class FractionalVE
  {
  private:
    caputo::caputo_init_vec<dim> store;
    caputo::caputo_init_scl store_p;
  public:
    MatLawInterface *m_law;

    FractionalVE(MatLawInterface &law, const double alpha, const double Tf);

    ~FractionalVE() {}

    double stress(const kinematics::kinematics2D &kin, const double dt, double stress[]);
    void stress(const double args[], const double dt, double stress[]);
  };


}
