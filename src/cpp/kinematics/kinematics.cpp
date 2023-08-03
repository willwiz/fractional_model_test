#define _USE_MATH_DEFINES

#include <cmath>
#include <stdio.h>
#include <iostream>
#include "kinematics.hpp"

namespace kinematics {

/*----------------------------------------------------------------------
 |  This file provides the structure for storing the info for deformation
 |  gradient. It is helpful for reducing recomputation.
 |
 |  Author: Will Zhang
 |  Dependencies: None
 -----------------------------------------------------------------------*/
  kinematics2D::kinematics2D():  C{}, Cinv{}, C33Cinv{} {}
  kinematics2D::~kinematics2D() {}

  deformation2D::deformation2D() {}
  deformation2D::deformation2D(const double args[4])
    : kinematics2D()
  {
    this -> precompute(args);
  }



  void deformation2D::precompute(const double args[4]) {

    this -> det = args[0]*args[3] - args[1]*args[2];
    this -> I_n = 1 / det;
    this -> Cinv[0] =  args[3] * I_n;
    this -> Cinv[1] = -args[1] * I_n;
    this -> Cinv[2] = -args[2] * I_n;
    this -> Cinv[3] =  args[0] * I_n;

    for (int i = 0; i < 4; i++)
    {
      this -> C[i] = args[i];
      this -> C33Cinv[i] = I_n*Cinv[i];
    }

    this -> I_1 = args[0] + args[3] + I_n;
    this -> I_1m3 = I_1 - 3.0;
  }

  deformation_ensemble2D::deformation_ensemble2D() {}
  deformation_ensemble2D::deformation_ensemble2D(double eb_strain)
    : kinematics2D()
  {
    this -> precompute(eb_strain);
  }


  void deformation_ensemble2D::precompute(double eb_strain) {


    this -> det = eb_strain*eb_strain;
    this -> I_n = 1 / det;
    this -> C[0] =  eb_strain;
    this -> C[1] =  0;
    this -> C[2] =  0;
    this -> C[3] =  eb_strain;
    this -> Cinv[0] =  1.0 / eb_strain;
    this -> Cinv[1] =  0;
    this -> Cinv[2] =  0;
    this -> Cinv[3] =  1.0 / eb_strain;

    for (int i = 0; i < 4; i++)
    {
      this -> C33Cinv[i] = I_n*Cinv[i];
    }

    this -> I_1 = eb_strain + eb_strain + I_n;
    this -> I_1m3 = I_1 - 3.0;
  }

}