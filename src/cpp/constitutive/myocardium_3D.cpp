#define _USE_MATH_DEFINES
#include <cmath>
#include "../kinematics/tensor_algebra.hpp"
#include "../kinematics/kinematics.hpp"
#include "myocardium_3D.hpp"

namespace constitutive_models {

    Myocardium::Myocardium() {};
    Myocardium::~Myocardium() {};
    Myocardium::Myocardium(double b1, double b2, double kff, double kss, double knn, double kfs, double kfn, double ksn, double fiber[])
    {
        this->set_pars(b1, b2, kff, kss, knn, kfs, kfn, knn, fiber);
    };

    void Myocardium::set_pars(double b1, double b2, double kff, double kss, double knn, double kfs, double kfn, double ksn, double fiber[])
    {

        this -> b1 = b1;
        this -> b2 = b2;
        this -> kff = kff;
        this -> kss = kss;
        this -> knn = knn;
        this -> kfs = kfs;
        this -> kfn = kfn;
        this -> ksn = ksn;

        mxm[0] = fiber[0] * fiber[0];
        mxm[1] = fiber[0] * fiber[1];
        mxm[2] = fiber[0] * fiber[2];
        mxm[3] = mxm[1];
        mxm[4] = fiber[1] * fiber[1];
        mxm[5] = fiber[1] * fiber[2];
        mxm[6] = mxm[2];
        mxm[7] = mxm[5];
        mxm[8] = fiber[2] * fiber[2];

        nxn[0] = fiber[3] * fiber[3];
        nxn[1] = fiber[3] * fiber[4];
        nxn[2] = fiber[3] * fiber[5];
        nxn[3] = nxn[1];
        nxn[4] = fiber[4] * fiber[4];
        nxn[5] = fiber[4] * fiber[5];
        nxn[6] = nxn[2];
        nxn[7] = nxn[5];
        nxn[8] = fiber[5] * fiber[5];

        zxz[0] = fiber[6] * fiber[6];
        zxz[1] = fiber[6] * fiber[7];
        zxz[2] = fiber[6] * fiber[8];
        zxz[3] = zxz[1];
        zxz[4] = fiber[7] * fiber[7];
        zxz[5] = fiber[7] * fiber[8];
        zxz[6] = zxz[2];
        zxz[7] = zxz[5];
        zxz[8] = fiber[8] * fiber[8];

        size_t k = 0;
        for (size_t i = 0; i < 3; i++)
        {
            for (size_t j = 3; j < 6; j++)
            {
                mxn[k] = 0.5 * (fiber[i] * fiber[j] + fiber[j] * fiber[i]);
                k++;
            }

        }

        k = 0;
        for (size_t i = 0; i < 3; i++)
        {
            for (size_t j = 6; j < 9; j++)
            {
                mxz[k] = 0.5 * (fiber[i] * fiber[j] + fiber[j] * fiber[i]);
                k++;
            }

        }

        k = 0;
        for (size_t i = 3; i < 6; i++)
        {
            for (size_t j = 6; j < 9; j++)
            {
                nxz[k] = 0.5 * (fiber[i] * fiber[j] + fiber[j] * fiber[i]);
                k++;
            }

        }
    }




    double Myocardium::stress(const kinematics::kinematics<9> &kin, double stress[9]){
        double I_ff = ddot<9>(mxm, kin.C);
        double I_ss = ddot<9>(nxn, kin.C);
        double I_nn = ddot<9>(zxz, kin.C);
        double I_fs = ddot<9>(mxn, kin.C);
        double I_fn = ddot<9>(mxz, kin.C);
        double I_sn = ddot<9>(nxz, kin.C);

        double W1 = exp(b1*kin.I_1m3);
        double W2 = exp(b2*(I_fs*I_fs + I_fn*I_fn + I_sn*I_sn));

        double W1ff = kff * (W1 * I_ff - 1.0);
        double W1ss = kss * (W1 * I_ss - 1.0);
        double W1nn = knn * (W1 * I_nn - 1.0);
        double W2fs = kfs * (W2 * I_fs);
        double W2fn = kfn * (W2 * I_fn);
        double W2sn = ksn * (W2 * I_nn);
        for (int i = 0; i < 9; i++)
        {
            stress[i] = W1ff * mxm[i] + W1ss * nxn[i] + W2fs * mxn[i];
        }
        return 0.0;
    }

    void Myocardium::stress(double args[], double stress[9]){

        kinematics::deformation3D kin(args);
        (void) this->stress(kin, stress);
    }

}