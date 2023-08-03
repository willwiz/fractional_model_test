import numpy as np
from numpy.typing import NDArray as Arr
from numpy import float64 as dbl
from numpy import int32 as spi
try:
    from ._HModels import (
        caputo_initialize,
        NeoHookean2D,
        HOGstruc2D,
        pyHOGDouble2D,
        pyHOG2D,
        GetParameters_cpp,
        GetParametersScaled_cpp,
        HESimulation_cpp,
        HESimulation_Scaled_cpp,
        CaputoSimulation_C_M_cpp,
        CaputoSimulation_C_M_Scaled_cpp,
        ResidualFun_HE_cpp,
        ResidualFun_HE_Scaled_cpp,
        ResidualFun_VE_C_M_cpp,
        ResidualFun_VE_C_M_hyst_cpp,
        ResidualFun_VE_C_M_hyst_relax_cpp,
        ResidualFun_VE_C_M_scaled_hyst_cpp,
        ResidualFun_VE_C_M_scaled_hyst_relax_cpp,
    )
except ImportError:
    print(">>>ERROR: HModel model module has not been compiled")
    raise


def GetParameters(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl) -> Arr[dbl]:
    return GetParameters_cpp(pars, fiber, visco, Tf)


def GetParametersScaled(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl]) -> Arr[dbl]:
    return GetParametersScaled_cpp(pars, fiber, visco, Tf, Cmax)


def HESimulation(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], args:Arr[dbl], dt:Arr[dbl]) -> Arr[dbl]:
    return HESimulation_cpp(pars, fiber, visco, Tf, Cmax, args, dt)


def HESimulation_Scaled(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], args:Arr[dbl], dt:Arr[dbl]) -> Arr[dbl]:
    return HESimulation_Scaled_cpp(pars, fiber, visco, Tf, Cmax, args, dt)


def CaputoSimulation_C_M(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], args:Arr[dbl], dt:Arr[dbl]) -> Arr[dbl]:
    return CaputoSimulation_C_M_cpp(pars, fiber, visco, Tf, Cmax, args, dt)


def CaputoSimulation_C_M_Scaled(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], args:Arr[dbl], dt:Arr[dbl]) -> Arr[dbl]:
    return CaputoSimulation_C_M_Scaled_cpp(pars, fiber, visco, Tf, Cmax, args, dt)


def ResidualFun_HE(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], strain:Arr[dbl], stress:Arr[dbl], dt:Arr[dbl], weights:Arr[dbl], deltaCG:Arr[dbl], hysteresis:Arr[dbl], alphas:Arr[dbl], index:Arr[spi], select:Arr[spi], skip:spi=1) -> float:
    return ResidualFun_HE_cpp(pars, fiber, visco, Tf, Cmax, strain, stress, dt, weights, deltaCG, hysteresis, alphas, index, select, skip)


def ResidualFun_HE_Scaled(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], strain:Arr[dbl], stress:Arr[dbl], dt:Arr[dbl], weights:Arr[dbl], deltaCG:Arr[dbl], hysteresis:Arr[dbl], alphas:Arr[dbl], index:Arr[spi], select:Arr[spi], skip:spi=1) -> float:
    return ResidualFun_HE_Scaled_cpp(pars, fiber, visco, Tf, Cmax, strain, stress, dt, weights, deltaCG, hysteresis, alphas, index, select, skip)


def ResidualFun_VE_C_M(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], strain:Arr[dbl], stress:Arr[dbl], dt:Arr[dbl], weights:Arr[dbl], deltaCG:Arr[dbl], hysteresis:Arr[dbl], alphas:Arr[dbl], index:Arr[spi], select:Arr[spi], skip:spi=1) -> float:
    return ResidualFun_VE_C_M_cpp(pars, fiber, visco, Tf, Cmax, strain, stress, dt, weights, deltaCG, hysteresis, alphas, index, select, skip)


def ResidualFun_VE_C_M_hyst(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], strain:Arr[dbl], stress:Arr[dbl], dt:Arr[dbl], weights:Arr[dbl], deltaCG:Arr[dbl], hysteresis:Arr[dbl], alphas:Arr[dbl], index:Arr[spi], select:Arr[spi], skip:spi=1) -> float:
    return ResidualFun_VE_C_M_hyst_cpp(pars, fiber, visco, Tf, Cmax, strain, stress, dt, weights, deltaCG, hysteresis, alphas, index, select, skip)


def ResidualFun_VE_C_M_hyst_relax(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], strain:Arr[dbl], stress:Arr[dbl], dt:Arr[dbl], weights:Arr[dbl], deltaCG:Arr[dbl], hysteresis:Arr[dbl], alphas:Arr[dbl], index:Arr[spi], select:Arr[spi], skip:spi=1) -> float:
    return ResidualFun_VE_C_M_hyst_relax_cpp(pars, fiber, visco, Tf, Cmax, strain, stress, dt, weights, deltaCG, hysteresis, alphas, index, select, skip)


def ResidualFun_VE_C_M_scaled_hyst(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], strain:Arr[dbl], stress:Arr[dbl], dt:Arr[dbl], weights:Arr[dbl], deltaCG:Arr[dbl], hysteresis:Arr[dbl], alphas:Arr[dbl], index:Arr[spi], select:Arr[spi], skip:spi=1) -> float:
    return ResidualFun_VE_C_M_scaled_hyst_cpp(pars, fiber, visco, Tf, Cmax, strain, stress, dt, weights, deltaCG, hysteresis, alphas, index, select, skip)


def ResidualFun_VE_C_M_scaled_hyst_relax(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], strain:Arr[dbl], stress:Arr[dbl], dt:Arr[dbl], weights:Arr[dbl], deltaCG:Arr[dbl], hysteresis:Arr[dbl], alphas:Arr[dbl], index:Arr[spi], select:Arr[spi], skip:spi=1) -> float:
    return ResidualFun_VE_C_M_scaled_hyst_relax_cpp(pars, fiber, visco, Tf, Cmax, strain, stress, dt, weights, deltaCG, hysteresis, alphas, index, select, skip)


