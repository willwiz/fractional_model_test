#!/usr/bin/env python3
import abc
import enum
import dataclasses
import numpy as np
from numpy.typing import NDArray as Arr
from numpy import (
  float64 as f64,
  int32 as i32,
)
from scipy.optimize import LinearConstraint
from typing import Callable


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
  ThoracicDefault_GetParametersScaled_cpp,
  ThoracicDefaultFung_GetParametersScaled_cpp,
  ThoracicIso_GetParametersScaled_cpp,
  ThoracicLin_GetParametersScaled_cpp,
  ThoracicQuad_GetParametersScaled_cpp,
  ThoracicCirc_GetParametersScaled_cpp,
  ThoracicDefault_VESimulation_Scaled_cpp,
  ThoracicDefaultFung_VESimulation_Scaled_cpp,
  ThoracicIso_VESimulation_Scaled_cpp,
  ThoracicLin_VESimulation_Scaled_cpp,
  ThoracicQuad_VESimulation_Scaled_cpp,
  ThoracicCirc_VESimulation_Scaled_cpp,
  ThoracicDefault_ResidualFun_VE_scaled_hyst_relax_cpp,
  ThoracicDefaultFung_ResidualFun_VE_scaled_hyst_relax_cpp,
  ThoracicIso_ResidualFun_VE_scaled_hyst_relax_cpp,
  ThoracicLin_ResidualFun_VE_scaled_hyst_relax_cpp,
  ThoracicQuad_ResidualFun_VE_scaled_hyst_relax_cpp,
  ThoracicCirc_ResidualFun_VE_scaled_hyst_relax_cpp,
)



class ModelList(enum.StrEnum):
  F_VE_HR = enum.auto()
  F_VE_S_H = enum.auto()
  F_VE_S_HR = enum.auto()
  TDEFAULT_VE_S_HR = enum.auto()
  TDEFUNG_VE_S_HR = enum.auto()
  TISO_VE_S_HR = enum.auto()
  TLIN_VE_S_HR = enum.auto()
  TQUAD_VE_S_HR = enum.auto()
  TCIRC_VE_S_HR = enum.auto()


class ParameterDataclass:
  pass

@dataclasses.dataclass
class DC_FemoralParameters(ParameterDataclass):
  Kg:    float
  Kc:    float
  bc:    float
  Ke:    float
  be:    float
  Ks:    float
  bs:    float
  theta: float
  alpha: float
  vc:    float
  vs:    float



@dataclasses.dataclass
class DC_ThoracicDefaultParameters(ParameterDataclass):
  Ke:    float
  Kc:    float
  bc:    float
  theta: float
  alpha: float
  vc:    float


@dataclasses.dataclass
class DC_ThoracicIsoParameters(ParameterDataclass):
  Ke:    float
  Ks:    float
  Kc:    float
  bc:    float
  theta: float
  alpha: float
  vc:    float
  vs:    float


@dataclasses.dataclass
class DC_ThoracicLinParameters(ParameterDataclass):
  Ke:    float
  Ks:    float
  Kc:    float
  bc:    float
  theta: float
  alpha: float
  vc:    float
  vs:    float


@dataclasses.dataclass
class DC_ThoracicQuadParameters(ParameterDataclass):
  Ke:    float
  Ks:    float
  Kc:    float
  bc:    float
  theta: float
  alpha: float
  vc:    float
  vs:    float


@dataclasses.dataclass
class DC_ThoracicCircParameters(ParameterDataclass):
  Ke:    float
  Ks:    float
  bs:    float
  Kc:    float
  bc:    float
  theta: float
  alpha: float
  vc:    float
  vs:    float



double1D = lambda : np.zeros((1,), dtype=f64)
double2D = lambda : np.zeros((2,2), dtype=f64)
int1D = lambda : np.zeros((1,), dtype=i32)

def femoral_par_split(par):
  return par[:7], par[7:9], par[9:]

def femoral_par_split_he(par):
  return par[:7], par[7:9], double1D()

def thoracic_default_par_split(par):
  return par[:3], par[3:5], par[5:]

def thoracic_iso_par_split(par):
  return par[:4], par[4:6], par[6:]

def thoracic_lin_par_split(par):
  return par[:4], par[4:6], par[6:]

def thoracic_quad_par_split(par):
  return par[:4], par[4:6], par[6:]

def thoracic_circ_par_split(par):
  return par[:5], par[5:7], par[7:]



def femoral_partial_pars(pars, pos):
  temp = np.copy(pars)
  for i in [0, 1, 3, 5]:
    if i != pos:
      temp[i] = 0
  return temp


def thoracic_default_partial_pars(pars, pos):
  temp = np.copy(pars)
  for i in [1, 0]:
    if i != pos:
      temp[i] = 0
  return temp

def thoracic_iso_partial_pars(pars, pos):
  temp = np.copy(pars)
  for i in [2, 1, 0]:
    if i != pos:
      temp[i] = 0
  return temp


def thoracic_lin_partial_pars(pars, pos):
  temp = np.copy(pars)
  for i in [2, 1, 0]:
    if i != pos:
      temp[i] = 0
  return temp


def thoracic_quad_partial_pars(pars, pos):
  temp = np.copy(pars)
  for i in [2, 1, 0]:
    if i != pos:
      temp[i] = 0
  return temp


def thoracic_circ_partial_pars(pars, pos):
  temp = np.copy(pars)
  for i in [3, 1, 0]:
    if i != pos:
      temp[i] = 0
  return temp


@dataclasses.dataclass
class objective(abc.ABC):
  time : float = 3000.0
  strain:  Arr[f64] = dataclasses.field(default_factory=double2D)
  stress:  Arr[f64] = dataclasses.field(default_factory=double2D)
  dt:      Arr[f64] = dataclasses.field(default_factory=double1D)
  index:   Arr[i32] = dataclasses.field(default_factory=int1D)
  weights: Arr[f64] = dataclasses.field(default_factory=double2D)
  select:  Arr[i32] = dataclasses.field(default_factory=int1D)
  deltaCG: Arr[f64] = dataclasses.field(default_factory=double2D)
  hyst:    Arr[f64] = dataclasses.field(default_factory=double2D)
  alphas:  Arr[f64] = dataclasses.field(default_factory=double1D)
  Cmax:    Arr[f64] = dataclasses.field(default_factory=double1D)
  @abc.abstractmethod
  def get_scaled_parameters(self, x): pass
  @abc.abstractmethod
  def sim(self, x): pass
  @abc.abstractmethod
  def sim_partials(self, x): pass
  @abc.abstractmethod
  def func(self, x): pass

class ObjFemoral_HE(objective):
  def get_scaled_parameters(self, x):
    pars, fiber, frac = femoral_par_split(x)
    return Femoral_GetParameters_cpp(pars, fiber, frac, self.time)
  def sim(self, x):
    pars, fiber, frac = femoral_par_split_he(x)
    return Femoral_HESimulation_cpp(pars, fiber, frac, self.time, self.Cmax, self.strain, self.dt)
  def sim_partials(self, x):
    return tuple(self.sim(femoral_partial_pars(x, i)) for i in [1, 3, 5, 0])
  def func(self, x):
    pars, fiber, frac = femoral_par_split_he(x)
    return Femoral_ResidualFun_HE_cpp(pars, fiber, frac, self.time, self.Cmax,
      self.strain, self.stress,
      self.dt, self.weights, self.deltaCG, self.hyst, self.alphas,
      self.index, self.select, skip=1)


class ObjFemoral_HEscaled(objective):
  def get_scaled_parameters(self, x):
    pars, fiber, frac = femoral_par_split(x)
    return Femoral_GetParametersScaled_cpp(pars, fiber, frac, self.time, self.Cmax)
  def sim(self, x):
    pars, fiber, frac = femoral_par_split_he(x)
    return Femoral_HESimulation_Scaled_cpp(pars, fiber, frac, self.time, self.Cmax, self.strain, self.dt)
  def sim_partials(self, x):
    return tuple(self.sim(femoral_partial_pars(x, i)) for i in [1, 3, 5, 0])
  def func(self, x):
    pars, fiber, frac = femoral_par_split_he(x)
    return Femoral_ResidualFun_HE_Scaled_cpp(pars, fiber, frac, self.time, self.Cmax,
      self.strain, self.stress,
      self.dt, self.weights, self.deltaCG, self.hyst, self.alphas,
      self.index, self.select, skip=1)


class ObjFemoral_VE(objective):
  def get_scaled_parameters(self, x):
    pars, fiber, frac = femoral_par_split(x)
    return Femoral_GetParameters_cpp(pars, fiber, frac, self.time)
  def sim(self, x):
    pars, fiber, frac = femoral_par_split(x)
    return Femoral_VESimulation_cpp(pars, fiber, frac, self.time, self.Cmax, self.strain, self.dt)
  def sim_partials(self, x):
    return tuple(self.sim(femoral_partial_pars(x, i)) for i in [1, 3, 5, 0])
  def func(self, x):
    pars, fiber, frac = femoral_par_split(x)
    return Femoral_ResidualFun_VE_hyst_cpp(pars, fiber, frac, self.time, self.Cmax,
      self.strain, self.stress,
      self.dt, self.weights, self.deltaCG, self.hyst, self.alphas,
      self.index, self.select, skip=1)


class ObjFemoral_VE_hyst(objective):
  def get_scaled_parameters(self, x):
    pars, fiber, frac = femoral_par_split(x)
    return Femoral_GetParameters_cpp(pars, fiber, frac, self.time)
  def sim(self, x):
    pars, fiber, frac = femoral_par_split(x)
    return Femoral_VESimulation_cpp(pars, fiber, frac, self.time, self.Cmax, self.strain, self.dt)
  def sim_partials(self, x):
    return tuple(self.sim(femoral_partial_pars(x, i)) for i in [1, 3, 5, 0])
  def func(self, x):
    pars, fiber, frac = femoral_par_split(x)
    return Femoral_ResidualFun_VE_hyst_cpp(pars, fiber, frac, self.time, self.Cmax,
      self.strain, self.stress,
      self.dt, self.weights, self.deltaCG, self.hyst, self.alphas,
      self.index, self.select, skip=1)


class ObjFemoral_VE_hyst_relax(objective):
  def get_scaled_parameters(self, x):
    pars, fiber, frac = femoral_par_split(x)
    return Femoral_GetParameters_cpp(pars, fiber, frac, self.time)
  def sim(self, x):
    pars, fiber, frac = femoral_par_split(x)
    return Femoral_VESimulation_cpp(pars, fiber, frac, self.time, self.Cmax, self.strain, self.dt)
  def sim_partials(self, x):
    return tuple(self.sim(femoral_partial_pars(x, i)) for i in [1, 3, 5, 0])
  def func(self, x):
    pars, fiber, frac = femoral_par_split(x)
    return Femoral_ResidualFun_VE_hyst_relax_cpp(pars, fiber, frac, self.time, self.Cmax,
      self.strain, self.stress,
      self.dt, self.weights, self.deltaCG, self.hyst, self.alphas,
      self.index, self.select, skip=1)


class ObjFemoral_VEscaled_hyst(objective):
  def get_scaled_parameters(self, x):
    pars, fiber, frac = femoral_par_split(x)
    return Femoral_GetParametersScaled_cpp(pars, fiber, frac, self.time, self.Cmax)
  def sim(self, x):
    pars, fiber, frac = femoral_par_split(x)
    return Femoral_VESimulation_Scaled_cpp(pars, fiber, frac, self.time, self.Cmax, self.strain, self.dt)
  def sim_partials(self, x):
    return tuple(self.sim(femoral_partial_pars(x, i)) for i in [1, 3, 5, 0])
  def func(self, x):
    pars, fiber, frac = femoral_par_split(x)
    return Femoral_ResidualFun_VE_scaled_hyst_cpp(pars, fiber, frac, self.time, self.Cmax,
      self.strain, self.stress,
      self.dt, self.weights, self.deltaCG, self.hyst, self.alphas,
      self.index, self.select, skip=1)


class ObjFemoral_VEscaled_hyst_relax(objective):
  def get_scaled_parameters(self, x):
    pars, fiber, frac = femoral_par_split(x)
    return Femoral_GetParametersScaled_cpp(pars, fiber, frac, self.time, self.Cmax)
  def sim(self, x):
    pars, fiber, frac = femoral_par_split(x)
    return Femoral_VESimulation_Scaled_cpp(pars, fiber, frac, self.time, self.Cmax, self.strain, self.dt)
  def sim_partials(self, x):
    return tuple(self.sim(femoral_partial_pars(x, i)) for i in [1, 3, 5, 0])
  def func(self, x):
    pars, fiber, frac = femoral_par_split(x)
    return Femoral_ResidualFun_VE_scaled_hyst_relax_cpp(pars, fiber, frac, self.time, self.Cmax,
      self.strain, self.stress,
      self.dt, self.weights, self.deltaCG, self.hyst, self.alphas,
      self.index, self.select, skip=1)


class ObjThoracicDefault_VEscaled_hyst_relax(objective):
  def get_scaled_parameters(self, x):
    pars, fiber, frac = thoracic_default_par_split(x)
    return ThoracicDefault_GetParametersScaled_cpp(pars, fiber, frac, self.time, self.Cmax)
  def sim(self, x):
    pars, fiber, frac = thoracic_default_par_split(x)
    return ThoracicDefault_VESimulation_Scaled_cpp(pars, fiber, frac, self.time, self.Cmax, self.strain, self.dt)
  def sim_partials(self, x):
    return tuple(self.sim(thoracic_default_partial_pars(x, i)) for i in [1, 0])
  def func(self, x):
    pars, fiber, frac = thoracic_default_par_split(x)
    return ThoracicDefault_ResidualFun_VE_scaled_hyst_relax_cpp(pars, fiber, frac, self.time, self.Cmax,
      self.strain, self.stress,
      self.dt, self.weights, self.deltaCG, self.hyst, self.alphas,
      self.index, self.select, skip=1)


class ObjThoracicDefaultFung_VEscaled_hyst_relax(objective):
  def get_scaled_parameters(self, x):
    pars, fiber, frac = thoracic_default_par_split(x)
    return ThoracicDefaultFung_GetParametersScaled_cpp(pars, fiber, frac, self.time, self.Cmax)
  def sim(self, x):
    pars, fiber, frac = thoracic_default_par_split(x)
    return ThoracicDefaultFung_VESimulation_Scaled_cpp(pars, fiber, frac, self.time, self.Cmax, self.strain, self.dt)
  def sim_partials(self, x):
    return tuple(self.sim(thoracic_default_partial_pars(x, i)) for i in [1, 0])
  def func(self, x):
    pars, fiber, frac = thoracic_default_par_split(x)
    return ThoracicDefaultFung_ResidualFun_VE_scaled_hyst_relax_cpp(pars, fiber, frac, self.time, self.Cmax,
      self.strain, self.stress,
      self.dt, self.weights, self.deltaCG, self.hyst, self.alphas,
      self.index, self.select, skip=1)


class ObjThoracicIso_VEscaled_hyst_relax(objective):
  def get_scaled_parameters(self, x):
    pars, fiber, frac = thoracic_iso_par_split(x)
    return ThoracicIso_GetParametersScaled_cpp(pars, fiber, frac, self.time, self.Cmax)
  def sim(self, x):
    pars, fiber, frac = thoracic_iso_par_split(x)
    return ThoracicIso_VESimulation_Scaled_cpp(pars, fiber, frac, self.time, self.Cmax, self.strain, self.dt)
  def sim_partials(self, x):
    return tuple(self.sim(thoracic_iso_partial_pars(x, i)) for i in [2, 0, 1])
  def func(self, x):
    pars, fiber, frac = thoracic_iso_par_split(x)
    return ThoracicIso_ResidualFun_VE_scaled_hyst_relax_cpp(pars, fiber, frac, self.time, self.Cmax,
      self.strain, self.stress,
      self.dt, self.weights, self.deltaCG, self.hyst, self.alphas,
      self.index, self.select, skip=1)


class ObjThoracicLin_VEscaled_hyst_relax(objective):
  def get_scaled_parameters(self, x):
    pars, fiber, frac = thoracic_lin_par_split(x)
    return ThoracicLin_GetParametersScaled_cpp(pars, fiber, frac, self.time, self.Cmax)
  def sim(self, x):
    pars, fiber, frac = thoracic_lin_par_split(x)
    return ThoracicLin_VESimulation_Scaled_cpp(pars, fiber, frac, self.time, self.Cmax, self.strain, self.dt)
  def sim_partials(self, x):
    return tuple(self.sim(thoracic_lin_partial_pars(x, i)) for i in [2, 0, 1])
  def func(self, x):
    pars, fiber, frac = thoracic_lin_par_split(x)
    return ThoracicLin_ResidualFun_VE_scaled_hyst_relax_cpp(pars, fiber, frac, self.time, self.Cmax,
      self.strain, self.stress,
      self.dt, self.weights, self.deltaCG, self.hyst, self.alphas,
      self.index, self.select, skip=1)


class ObjThoracicQuad_VEscaled_hyst_relax(objective):
  def get_scaled_parameters(self, x):
    pars, fiber, frac = thoracic_quad_par_split(x)
    return ThoracicQuad_GetParametersScaled_cpp(pars, fiber, frac, self.time, self.Cmax)
  def sim(self, x):
    pars, fiber, frac = thoracic_quad_par_split(x)
    return ThoracicQuad_VESimulation_Scaled_cpp(pars, fiber, frac, self.time, self.Cmax, self.strain, self.dt)
  def sim_partials(self, x):
    return tuple(self.sim(thoracic_quad_partial_pars(x, i)) for i in [2, 0, 1])
  def func(self, x):
    pars, fiber, frac = thoracic_quad_par_split(x)
    return ThoracicQuad_ResidualFun_VE_scaled_hyst_relax_cpp(pars, fiber, frac, self.time, self.Cmax,
      self.strain, self.stress,
      self.dt, self.weights, self.deltaCG, self.hyst, self.alphas,
      self.index, self.select, skip=1)


class ObjThoracicCirc_VEscaled_hyst_relax(objective):
  def get_scaled_parameters(self, x):
    pars, fiber, frac = thoracic_circ_par_split(x)
    return ThoracicCirc_GetParametersScaled_cpp(pars, fiber, frac, self.time, self.Cmax)
  def sim(self, x):
    pars, fiber, frac = thoracic_circ_par_split(x)
    return ThoracicCirc_VESimulation_Scaled_cpp(pars, fiber, frac, self.time, self.Cmax, self.strain, self.dt)
  def sim_partials(self, x):
    return tuple(self.sim(thoracic_circ_partial_pars(x, i)) for i in [3, 0, 1])
  def func(self, x):
    pars, fiber, frac = thoracic_circ_par_split(x)
    return ThoracicCirc_ResidualFun_VE_scaled_hyst_relax_cpp(pars, fiber, frac, self.time, self.Cmax,
      self.strain, self.stress,
      self.dt, self.weights, self.deltaCG, self.hyst, self.alphas,
      self.index, self.select, skip=1)



def get_model(name:ModelList, time:Arr[f64], strain:Arr[f64],
              stress:Arr[f64], dt:Arr[f64], index:Arr[i32],
              weights:Arr[f64], select:Arr[i32], deltaCG:Arr[f64],
              hyst:Arr[f64], alphas:Arr[f64], Cmax:Arr[f64]
              ) -> objective:
  match name:
    case ModelList.F_VE_HR:
      return ObjFemoral_VE_hyst_relax(time, strain, stress, dt, index,
        weights, select, deltaCG, hyst, alphas)
    case ModelList.F_VE_S_H:
      return ObjFemoral_VEscaled_hyst(time, strain, stress, dt, index,
        weights, select, deltaCG, hyst, Cmax=Cmax)
    case ModelList.F_VE_S_HR:
      return ObjFemoral_VEscaled_hyst_relax(time, strain, stress, dt, index,
        weights, select, deltaCG, hyst, alphas, Cmax)
    case ModelList.TDEFAULT_VE_S_HR:
      return ObjThoracicDefault_VEscaled_hyst_relax(time, strain, stress, dt, index,
        weights, select, deltaCG, hyst, alphas, Cmax)
    case ModelList.TDEFUNG_VE_S_HR:
      return ObjThoracicDefaultFung_VEscaled_hyst_relax(time, strain, stress, dt, index,
        weights, select, deltaCG, hyst, alphas, Cmax)
    case ModelList.TISO_VE_S_HR:
      return ObjThoracicIso_VEscaled_hyst_relax(time, strain, stress, dt, index,
        weights, select, deltaCG, hyst, alphas, Cmax)
    case ModelList.TLIN_VE_S_HR:
      return ObjThoracicLin_VEscaled_hyst_relax(time, strain, stress, dt, index,
        weights, select, deltaCG, hyst, alphas, Cmax)
    case ModelList.TQUAD_VE_S_HR:
      return ObjThoracicQuad_VEscaled_hyst_relax(time, strain, stress, dt, index,
        weights, select, deltaCG, hyst, alphas, Cmax)
    case ModelList.TCIRC_VE_S_HR:
      return ObjThoracicCirc_VEscaled_hyst_relax(time, strain, stress, dt, index,
        weights, select, deltaCG, hyst, alphas, Cmax)

def get_parameter_dataclass(name:ModelList) -> ParameterDataclass:
  match name:
    case ModelList.F_VE_HR:
      return DC_FemoralParameters
    case ModelList.F_VE_S_H:
      return DC_FemoralParameters
    case ModelList.F_VE_S_HR:
      return DC_FemoralParameters
    case ModelList.TDEFAULT_VE_S_HR:
      return DC_ThoracicDefaultParameters
    case ModelList.TDEFUNG_VE_S_HR:
      return DC_ThoracicDefaultParameters
    case ModelList.TISO_VE_S_HR:
      return DC_ThoracicIsoParameters
    case ModelList.TLIN_VE_S_HR:
      return DC_ThoracicLinParameters
    case ModelList.TQUAD_VE_S_HR:
      return DC_ThoracicQuadParameters
    case ModelList.TCIRC_VE_S_HR:
      return DC_ThoracicCircParameters


def get_boundary_conditions(name:ModelList, strain:Arr[f64]):
  lb = np.array([1e-8, 1e-8], dtype=f64)
  ub = np.array([np.inf, np.inf], dtype=f64)
  bnds_struc = [(-0.78539816339, 0.78539816339), (0.0, 1.57079632679)]
  bnds_frac  = [(0.01, 0.25), (0.01, 0.25)]
  match name:
    case ModelList.F_VE_HR:
      A = np.zeros((2, 11), dtype=f64)
      A[0,2] = 1
      A[0,4] = -1
      A[1,2] = 1
      A[1,6] = -1
      bnds_par = [(0.0, 100.0),
                  (1.0e-3, 200.0), (0.0, round(30.0/(strain.max() - 1.0))),
                  (1.0e-3, 200.0), (0.0, round(15.0/(strain.max() - 1.0))),
                  (1.0e-3, 200.0), (0.0, round(15.0/(strain.max() - 1.0)))
                  ]
      lcs = LinearConstraint(A, lb, ub)
    case ModelList.F_VE_S_H:
      A = np.zeros((2, 11), dtype=f64)
      A[0,2] = 1
      A[0,4] = -1
      A[1,2] = 1
      A[1,6] = -1
      bnds_par = [(0.0, 100.0),
                  (1.0e-3, 200.0), (0.0, round(30.0/(strain.max() - 1.0))),
                  (1.0e-3, 200.0), (0.0, round(15.0/(strain.max() - 1.0))),
                  (1.0e-3, 200.0), (0.0, round(15.0/(strain.max() - 1.0)))
                  ]
      lcs = LinearConstraint(A, lb, ub)
    case ModelList.F_VE_S_HR:
      A = np.zeros((2, 11), dtype=f64)
      A[0,2] = 1
      A[0,4] = -1
      A[1,2] = 1
      A[1,6] = -1
      bnds_par = [(0.0, 100.0),
                  (1.0e-3, 200.0), (0.0, round(30.0/(strain.max() - 1.0))),
                  (1.0e-3, 200.0), (0.0, round(15.0/(strain.max() - 1.0))),
                  (1.0e-3, 200.0), (0.0, round(15.0/(strain.max() - 1.0)))
                  ]
      lcs = LinearConstraint(A, lb, ub)
    case ModelList.TDEFAULT_VE_S_HR:
      bnds_par = [(0.0, 100.0),
                  (1.0e-3, 200.0), (0.5, round(30.0/(strain.max() - 1.0))),
                  ]
      bnds_frac  = [(0.01, 0.25)]
      lcs = None
    case ModelList.TDEFUNG_VE_S_HR:
      bnds_par = [(1, 1000.0),
                  (1.0e-3, 200.0), (0.5, round(30.0/(strain.max() - 1.0))),
                  ]
      bnds_frac  = [(0.01, 0.25)]
      lcs = None
    case ModelList.TISO_VE_S_HR:
      bnds_par = [(0.0, 100.0),
                  (1.0e-3, 200.0),
                  (1.0e-3, 200.0), (0.5, round(30.0/(strain.max() - 1.0))),
                  ]
      lcs = None
    case ModelList.TLIN_VE_S_HR:
      bnds_par = [(0.0, 100.0),
                  (1.0e-3, 200.0),
                  (1.0e-3, 200.0), (0.5, round(30.0/(strain.max() - 1.0))),
                  ]
      lcs = None
    case ModelList.TQUAD_VE_S_HR:
      bnds_par = [(0.0, 100.0),
                  (1.0e-3, 200.0),
                  (1.0e-3, 200.0), (0.5, round(30.0/(strain.max() - 1.0))),
                  ]
      lcs = None
    case ModelList.TCIRC_VE_S_HR:
      A = np.zeros((1, 9), dtype=f64)
      A[0,2] = -1
      A[0,4] = 1
      lb = np.array([1e-8], dtype=f64)
      ub = np.array([np.inf], dtype=f64)
      bnds_par = [(0.0, 100.0),
                  (1.0e-3, 200.0), (0.0, round(15.0/(strain.max() - 1.0))),
                  (1.0e-3, 200.0), (0.0, round(30.0/(strain.max() - 1.0))),
                  ]
      lcs = LinearConstraint(A, lb, ub)
    case _:
      raise ValueError("Model not found")
  return bnds_par + bnds_struc + bnds_frac, lcs
# Some Inital Guess

# VE_objs: Dict[str, objective] = { 'VE_HR': objectiveV_hyst_relax,
#                 'VE_S_H': objectiveV_scaled_hyst,
#                 'VE_S_HR': objectiveV_scaled_hyst_relax,}
# lcs        = ( NonlinearConstraint(lambda x: x[2] - x[4], 0, np.inf),
#                 NonlinearConstraint(lambda x: x[2] - x[6], 0, np.inf))
