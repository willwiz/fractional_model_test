#include "../kinematics/kinematics.hpp"
#include "fractional.hpp"
#include <cmath>

namespace constitutive_models
{
  template<int dim>
  FractionalVE<dim>::FractionalVE(MatLawInterface& law, const double alpha, const double Tf)
    : store(alpha, Tf, 0.0), store_p(alpha, Tf, 0.0), m_law(&law) {}


  template<int dim>
  double FractionalVE<dim>::stress(const kinematics::kinematics2D &kin, const double dt, double stress[])
  {
    double p;
    double frac[4];

    p = m_law->stress(kin, frac);
    store.caputo_iter(frac, dt, stress);
    p = store_p.caputo_iter(p, dt);
    return p;
  }

  template<int dim>
  void FractionalVE<dim>::stress(const double args[], const double dt, double stress[])
  {
    kinematics::deformation2D kin(args);
    double p = this->stress(kin, dt, stress);
    for (int i = 0; i < 4; i++)
    {
      stress[i] = stress[i] - p*kin.C33Cinv[i];
    }
  }


} // namespace constitutive