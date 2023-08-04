import numpy as np
from numpy.typing import NDArray as Arr
from numpy import float64 as dbl
from numpy import int32 as spi
try:
    from ._artery import (
        NeoHookean2D,
        HOGstruc2D,
        pyHOG2D,
        Femoral_HESimulation_cpp,
        Femoral_VESimulation_cpp,

        Femoral_ResidualFun_HE_cpp,
        Femoral_ResidualFun_VE_cpp,

    )
except ImportError:
    print(">>>ERROR: _artery module has not been compiled")
    raise



def Femoral_HESimulation(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], args:Arr[dbl], dt:Arr[dbl]) -> Arr[dbl]:
    return Femoral_HESimulation_cpp(pars, fiber, visco, Tf, Cmax, args, dt)

def Femoral_VESimulation(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], args:Arr[dbl], dt:Arr[dbl]) -> Arr[dbl]:
    return Femoral_VESimulation_cpp(pars, fiber, visco, Tf, Cmax, args, dt)

def Femoral_ResidualFun_HE(pars:Arr[dbl], fiber:Arr[dbl], visco:Arr[dbl], Tf:dbl, Cmax:Arr[dbl], strain:Arr[dbl], stress:Arr[dbl], dt:Arr[dbl], weights:Arr[dbl], deltaCG:Arr[dbl], hysteresis:Arr[dbl], alphas:Arr[dbl], index:Arr[spi], select:Arr[spi], skip:spi=1) -> float:
    return Femoral_ResidualFun_HE_cpp(pars, fiber, visco, Tf, Cmax, strain, stress, dt, weights, deltaCG, hysteresis, alphas, index, select, skip)

