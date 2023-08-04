#pragma once

#define _USE_MATH_DEFINES

#include <cmath>
#include "../constitutive/interfaces.hpp"
#include "../constitutive/neohookean.hpp"
#include "../constitutive/myocardium_3D.hpp"
#include "../fractional/fractional.hpp"


namespace sim {

  class MyocardiumHE: public constitutive_models::MatLawTimeInterface<9>
  {
  protected:
    constitutive_models::NeoHookean3D m_matrix;
    constitutive_models::Myocardium m_muscle;

  public:
    MyocardiumHE(double pars[], double fiber[]):
      m_matrix(pars[0]),
      m_muscle(pars[1], pars[2], pars[3], pars[4], pars[5], pars[6], pars[7], pars[8], fiber)
    {}

    ~MyocardiumHE() {}


    void stress(const kinematics::kinematics<9> &kin, const double dt, double stress[]);

  };


  class MyocardiumVE: public MyocardiumHE
  {
  protected:
    constitutive_models::FractionalVE<9> muscle;

  public:
    MyocardiumVE(double pars[], double fiber[], double visco[], double Tf, double Cmax[]):
      MyocardiumHE(pars, fiber),
      muscle(m_muscle, visco[0], Tf)
    {}

    ~MyocardiumVE() {}

    void stress(const kinematics::kinematics<9> &kin, const double dt, double stress[]);

  };



}
