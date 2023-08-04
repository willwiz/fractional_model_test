#define _USE_MATH_DEFINES

#include <cmath>
#include "myocardium_ve_model.hpp"

/*----------------------------------------------------------------------
 |  This file provides the definitions of the different model forms
 |  which combines the primative constitive model from the other cpp files
 |  in the constitutive_models namespace
 |
 |  These models are mainly used for the collaboration with Alexey Kamenskiy
 |
 |  Author: Will Zhang
 |  Dependencies: None
 -----------------------------------------------------------------------*/


using namespace constitutive_models;

namespace sim {


/*----------------------------------------------------------------------
 |  This provides the main models in the full constitutive model
 -----------------------------------------------------------------------*/
    void MyocardiumHE::stress(const kinematics::kinematics<9> &kin, const double dt, double stress[])
    {
        double p = 0.0;
        double mat[9], smc[9];
        p = m_matrix.stress(kin, mat);
        (void) m_muscle.stress(kin, smc);
        for (int j = 0; j < 9; j++)
        {
            stress[j] = mat[j] + smc[j];
        }
    }


    void MyocardiumVE::stress(const kinematics::kinematics<9> &kin, const double dt, double stress[])
    {
        double p = 0.0;
        double mat[9], smc[9];
        p = m_matrix.stress(kin, mat);
        (void) muscle.stress(kin, dt, smc);
        for (int j = 0; j < 9; j++)
        {
            stress[j] = mat[j] + smc[j];
        }
    }

}