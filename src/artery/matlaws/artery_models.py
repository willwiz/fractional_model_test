import numpy as np
from numpy.typing import NDArray as Arr
from numpy import float64 as dbl
from numpy import int32 as spi
try:
    from ._artery_models import (
        caputo_initialize,
        NeoHookean2D,
        HOGstruc2D,
        pyHOGDouble2D,
        pyHOG2D,
        Femoral_GetParameters_cpp,
        Femoral_GetParametersScaled_cpp,
        Femoral_HESimulation_cpp,
        Femoral_HESimulation_Scaled_cpp,
        Femoral_VESimulation_cpp,
        Femoral_VESimulation_Scaled_cpp,
        Femoral_ResidualFun_HE_cpp,
        Femoral_ResidualFun_HE_Scaled_cpp,
        Femoral_ResidualFun_VE_cpp,
        Femoral_ResidualFun_VE_hyst_cpp,
        Femoral_ResidualFun_VE_hyst_relax_cpp,
        Femoral_ResidualFun_VE_scaled_hyst_cpp,
        Femoral_ResidualFun_VE_scaled_hyst_relax_cpp,

        ThoracicIso_GetParametersScaled_cpp,
        ThoracicLin_GetParametersScaled_cpp,
        ThoracicIso_ResidualFun_VE_scaled_hyst_relax_cpp,
        ThoracicLin_ResidualFun_VE_scaled_hyst_relax_cpp,
    )
except ImportError:
    print(">>>ERROR: _artery_models module has not been compiled")
    raise


def Femoral_GetParameters(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl) -> Arr[dbl]:
    return Femoral_GetParameters_cpp(pars, fiber, visco, Tf)


def Femoral_GetParametersScaled(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl]) -> Arr[dbl]:
    return Femoral_GetParametersScaled_cpp(pars, fiber, visco, Tf, Cmax)


def Femoral_HESimulation(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], args:Arr[dbl], dt:Arr[dbl]) -> Arr[dbl]:
    return Femoral_HESimulation_cpp(pars, fiber, visco, Tf, Cmax, args, dt)


def Femoral_HESimulation_Scaled(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], args:Arr[dbl], dt:Arr[dbl]) -> Arr[dbl]:
    return Femoral_HESimulation_Scaled_cpp(pars, fiber, visco, Tf, Cmax, args, dt)


def Femoral_VESimulation(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], args:Arr[dbl], dt:Arr[dbl]) -> Arr[dbl]:
    return Femoral_VESimulation_cpp(pars, fiber, visco, Tf, Cmax, args, dt)


def Femoral_VESimulation_Scaled(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], args:Arr[dbl], dt:Arr[dbl]) -> Arr[dbl]:
    return Femoral_VESimulation_Scaled_cpp(pars, fiber, visco, Tf, Cmax, args, dt)


def Femoral_ResidualFun_HE(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], strain:Arr[dbl], stress:Arr[dbl], dt:Arr[dbl], weights:Arr[dbl], deltaCG:Arr[dbl], hysteresis:Arr[dbl], alphas:Arr[dbl], index:Arr[spi], select:Arr[spi], skip:spi=1) -> float:
    return Femoral_ResidualFun_HE_cpp(pars, fiber, visco, Tf, Cmax, strain, stress, dt, weights, deltaCG, hysteresis, alphas, index, select, skip)


def Femoral_ResidualFun_HE_Scaled(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], strain:Arr[dbl], stress:Arr[dbl], dt:Arr[dbl], weights:Arr[dbl], deltaCG:Arr[dbl], hysteresis:Arr[dbl], alphas:Arr[dbl], index:Arr[spi], select:Arr[spi], skip:spi=1) -> float:
    return Femoral_ResidualFun_HE_Scaled_cpp(pars, fiber, visco, Tf, Cmax, strain, stress, dt, weights, deltaCG, hysteresis, alphas, index, select, skip)


def Femoral_ResidualFun_VE(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], strain:Arr[dbl], stress:Arr[dbl], dt:Arr[dbl], weights:Arr[dbl], deltaCG:Arr[dbl], hysteresis:Arr[dbl], alphas:Arr[dbl], index:Arr[spi], select:Arr[spi], skip:spi=1) -> float:
    return Femoral_ResidualFun_VE_cpp(pars, fiber, visco, Tf, Cmax, strain, stress, dt, weights, deltaCG, hysteresis, alphas, index, select, skip)


def Femoral_ResidualFun_VE_hyst(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], strain:Arr[dbl], stress:Arr[dbl], dt:Arr[dbl], weights:Arr[dbl], deltaCG:Arr[dbl], hysteresis:Arr[dbl], alphas:Arr[dbl], index:Arr[spi], select:Arr[spi], skip:spi=1) -> float:
    return Femoral_ResidualFun_VE_hyst_cpp(pars, fiber, visco, Tf, Cmax, strain, stress, dt, weights, deltaCG, hysteresis, alphas, index, select, skip)


def Femoral_ResidualFun_VE_hyst_relax(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], strain:Arr[dbl], stress:Arr[dbl], dt:Arr[dbl], weights:Arr[dbl], deltaCG:Arr[dbl], hysteresis:Arr[dbl], alphas:Arr[dbl], index:Arr[spi], select:Arr[spi], skip:spi=1) -> float:
    return Femoral_ResidualFun_VE_hyst_relax_cpp(pars, fiber, visco, Tf, Cmax, strain, stress, dt, weights, deltaCG, hysteresis, alphas, index, select, skip)


def Femoral_ResidualFun_VE_scaled_hyst(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], strain:Arr[dbl], stress:Arr[dbl], dt:Arr[dbl], weights:Arr[dbl], deltaCG:Arr[dbl], hysteresis:Arr[dbl], alphas:Arr[dbl], index:Arr[spi], select:Arr[spi], skip:spi=1) -> float:
    return Femoral_ResidualFun_VE_scaled_hyst_cpp(pars, fiber, visco, Tf, Cmax, strain, stress, dt, weights, deltaCG, hysteresis, alphas, index, select, skip)


def Femoral_ResidualFun_VE_scaled_hyst_relax(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], strain:Arr[dbl], stress:Arr[dbl], dt:Arr[dbl], weights:Arr[dbl], deltaCG:Arr[dbl], hysteresis:Arr[dbl], alphas:Arr[dbl], index:Arr[spi], select:Arr[spi], skip:spi=1) -> float:
    return Femoral_ResidualFun_VE_scaled_hyst_relax_cpp(pars, fiber, visco, Tf, Cmax, strain, stress, dt, weights, deltaCG, hysteresis, alphas, index, select, skip)




def ThoracicIso_GetParametersScaled(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl]) -> Arr[dbl]:
    return ThoracicIso_GetParametersScaled_cpp(pars, fiber, visco, Tf, Cmax)

def ThoracicLin_GetParametersScaled(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl]) -> Arr[dbl]:
    return ThoracicLin_GetParametersScaled_cpp(pars, fiber, visco, Tf, Cmax)

def ThoracicIso_ResidualFun_VE_scaled_hyst_relax(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], strain:Arr[dbl], stress:Arr[dbl], dt:Arr[dbl], weights:Arr[dbl], deltaCG:Arr[dbl], hysteresis:Arr[dbl], alphas:Arr[dbl], index:Arr[spi], select:Arr[spi], skip:spi=1) -> float:
    return ThoracicIso_ResidualFun_VE_scaled_hyst_relax_cpp(pars, fiber, visco, Tf, Cmax, strain, stress, dt, weights, deltaCG, hysteresis, alphas, index, select, skip)

def ThoracicLin_ResidualFun_VE_scaled_hyst_relax(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], strain:Arr[dbl], stress:Arr[dbl], dt:Arr[dbl], weights:Arr[dbl], deltaCG:Arr[dbl], hysteresis:Arr[dbl], alphas:Arr[dbl], index:Arr[spi], select:Arr[spi], skip:spi=1) -> float:
    return ThoracicLin_ResidualFun_VE_scaled_hyst_relax_cpp(pars, fiber, visco, Tf, Cmax, strain, stress, dt, weights, deltaCG, hysteresis, alphas, index, select, skip)
