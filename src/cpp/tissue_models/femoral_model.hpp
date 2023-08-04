#pragma once

#define _USE_MATH_DEFINES

#include <cmath>
#include "../CTvalues_optimization.hpp"
#include "../kinematics/kinematics.hpp"
#include "../constitutive/interfaces.hpp"
#include "../constitutive/neohookean.hpp"
#include "../constitutive/hog_2D.hpp"
#include "../constitutive/struc_hog_2D.hpp"
#include "../fractional/fractional.hpp"


namespace sim {

  class Femoral: public constitutive_models::MatLawTimeInterface<4>
  {
  protected:
    constitutive_models::NeoHookean m_matrix;
    constitutive_models::StrucHOG2D m_collagen;
    constitutive_models::Hog2D m_elastin;
    constitutive_models::Hog2D m_muscle;

  public:
    Femoral(double pars[], double fiber[]);
    Femoral(double pars[], double fiber[], double Cmax[]);
    ~Femoral();

    void get_scaled_pars(double pars[]);
    virtual void stress(const kinematics::kinematics<4> &kin, const double dt, double stress[]);

  };


  class FemoralVE: public Femoral
  {
  protected:
    constitutive_models::FractionalVE<4> collagen;
    constitutive_models::FractionalVE<4> muscle;

  public:
    FemoralVE(double pars[], double fiber[], double visco[], double Tf);
    FemoralVE(double pars[], double fiber[], double visco[], double Tf, double Cmax[]);
    ~FemoralVE();
    void stress(const kinematics::kinematics<4> &kin, const double dt, double stress[]);

  };


}
