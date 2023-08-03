#pragma once

#include "../kinematics/kinematics.hpp"
#include "interfaces.hpp"

namespace constitutive_models {

  class NeoHookean: public MatLawInterface
  {
    public:
      double mu;

      NeoHookean () {};
      NeoHookean (double mu);
      ~NeoHookean () {};
      void set_pars(double mu);
      double stress(const kinematics::kinematics2D &kin, double stress[]);
      void stress(double args[], double stress[]);
  };

}
