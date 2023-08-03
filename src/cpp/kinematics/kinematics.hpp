#pragma once

namespace kinematics {

    class kinematics2D
    {
    public:
        double det;
        double I_n;
        double I_1;
        double I_1m3;
        double C[4];
        double Cinv[4];
        double C33Cinv[4];
        kinematics2D();
        ~kinematics2D();
    };

    class deformation2D: public kinematics2D
    {
    public:
        deformation2D();
        deformation2D(const double vC[4]);
        void precompute(const double vC[4]);
    };


    class deformation_ensemble2D: public kinematics2D
    {
    public:
        deformation_ensemble2D();
        deformation_ensemble2D(double eb_strain);
        void precompute(double eb_strain);
    };

    class kinematics3D
    {
    public:
        double det;
        double I_1;
        double I_1m3;
        double C[9];
        double Cinv[9];
        kinematics3D();
        ~kinematics3D();
    };


    class deformation3D: public kinematics3D
    {
    public:
        deformation3D();
        deformation3D(const double vC[9]);
        void precompute(const double vC[9]);
    };

}
