#pragma once

#include "../kinematics/kinematics.hpp"
#include "interfaces.hpp"

namespace constitutive_models {

  class NeoHookean: public MatLawInterface<4>
  {
    public:
      double mu;

      NeoHookean () {};
      NeoHookean (double mu);
      ~NeoHookean () {};
      void set_pars(double mu);
      double stress(const kinematics::kinematics<4> &kin, double stress[]);
      void stress(double args[], double stress[]);
  };


  class NeoHookean3D: public MatLawInterface<9>
  {
    public:
      double mu;

      NeoHookean3D () {};
      NeoHookean3D (double mu);
      ~NeoHookean3D () {};
      void set_pars(double mu);
      double stress(const kinematics::kinematics<9> &kin, double stress[]);
      void stress(double args[], double stress[]);
  };

}
