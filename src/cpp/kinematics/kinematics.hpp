#pragma once

namespace kinematics {

    template<int dim>
    class kinematics
    {
    public:
        double det;
        double C[dim];
        double Cinv[dim];
        double I_n;
        double I_1;
        double I_1m3;
        kinematics();
        ~kinematics();
    };


    class deformation2D: public kinematics<4>
    {
    public:
        deformation2D();
        deformation2D(const double vC[4]);
        void precompute(const double vC[4]);
    };


    class deformation_ensemble2D: public kinematics<4>
    {
    public:
        deformation_ensemble2D();
        deformation_ensemble2D(double eb_strain);
        void precompute(double eb_strain);
    };



    class deformation3D: public kinematics<9>
    {
    public:
        deformation3D();
        deformation3D(const double vC[9]);
        void precompute(const double vC[9]);
    };

}
