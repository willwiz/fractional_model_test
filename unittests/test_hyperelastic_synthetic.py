#!/usr/bin/env pathon3

import numpy as np
from numpy import zeros, array, linspace, float64 as f64
from numpy.testing import assert_almost_equal
from scipy.interpolate import interp1d
from artery.matlaws.hog20132D import *
from artery.matlaws.caputoD import *
from artery.matlaws.artery_models import (
  NeoHookean2D,
  HOGstruc2D,
  pyHOG2D,
  Femoral_HESimulation,
)
import matplotlib.pyplot as plt
from time import perf_counter
import unittest

__unittest = True


""" ----------------------------------------------------------------------------
C++ simulation functions to be tested

Three forms:
  python
  c++ individual functions
  using c++ simulate function
---------------------------------------------------------------------------- """

def simulate_HE(pars:ndarray, struc:ndarray, args: ndarray):
  model = hog20132D(pars, struc[0], struc[1], struc[2])
  steps, dim = args.shape
  Sv = zeros((steps, dim))
  for i, a in enumerate(args):
    Sv[i] = model.stress(a)
  return Sv

def simulate_cpp(pars:ndarray, struc:ndarray, args: ndarray):
  collagen = HOGstruc2D(pars[1], pars[2], 0.0, struc[0], -struc[0], struc[1], struc[2])
  neo = NeoHookean2D(pars[0])
  elastin = pyHOG2D(pars[3], pars[4], 0.0)
  muscle = pyHOG2D(pars[5], pars[6], 0.5*pi)
  steps, dim = args.shape
  Sv = zeros((steps, dim))
  for i, a in enumerate(args):
    Sv[i] = neo.stress(a) + collagen.stress(a) + elastin.stress(a) + muscle.stress(a)
  return Sv


# ------------------------------------------------------------------------------
# Unit test class
# ------------------------------------------------------------------------------
class hyperelastic_simulations(unittest.TestCase):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    nt = 101
    Tf = 1000
    self.time   = linspace(0, Tf, nt)
    x = array([0, 1,    2, 3,   4, 5,   6,   7,   8,   9,   10], dtype=f64) * Tf/10.0
    y = array([1, 1.25, 1, 1.5, 1, 1.5, 1.5, 1.5, 1.5, 1.0, 1.0], dtype=f64)
    f = interp1d(x,y, 'linear')
    self.dt     = np.hstack((0.0, np.diff(self.time)), dtype=f64)
    self.strain = zeros((nt,4), dtype=float)
    self.strain[:, 0] = f(self.time)
    self.strain[:, 3] = f(self.time)
    self.kip = 0.155
    self.kop = 0.424285714285714
    self.x_HE3 = array([1, 0, 6, 1, 0, 1, 3, 0.3])
    # self.x_HE3 = array([5.37650604, 17.41700370, 1.19482728, 4.62237796, 1.77045881, 0.0, 0.00031839, 0.17641521])
    self.x_HE2 = array([1, 1, 6, 0, 0, 0, 3, 0.3])
    self.x_HE1 = array([1, 0, 4, 0, 0, 0, 2, 0.3])

  def simulate(self, x_HE):
    he       = simulate_HE(x_HE[:7],  array([x_HE[7], self.kip, self.kop]), self.strain)
    cpp      = simulate_cpp(x_HE[:7], array([x_HE[7], self.kip, self.kop]), self.strain)
    pure_cpp = Femoral_HESimulation(x_HE[:7], array([0.0, x_HE[7]]), array([0.1]), 3000.0, array([1.0, 0.0, 0.0, 1.0]), self.strain, self.dt)
    return he[1:], cpp[1:], pure_cpp[1:]

  def plot(self, x_HE, name):
    t1_start = perf_counter()
    he = simulate_HE(x_HE[:7], array([x_HE[7], 0.155, 0.424285714285714]), self.strain)
    t2_start = perf_counter()
    cpp = simulate_cpp(x_HE[:7], array([x_HE[7], 0.155, 0.424285714285714]), self.strain)
    t3_start = perf_counter()
    pure_cpp = Femoral_HESimulation(x_HE[:7], array([0.0, x_HE[7]]), array([0.1]), 3000.0, array([1.0, 0.0, 0.0, 1.0]), self.strain, self.dt)
    t4_start = perf_counter()

    print(f'Python completed in   {t2_start - t1_start} seconds')
    print(f'Cpp completed in      {t3_start - t2_start} seconds and speed gain of {(t2_start - t1_start)/(t3_start - t2_start):.3f}x')
    print(f'Pure Cpp completed in {t4_start - t3_start} secondsand speed gain of {(t2_start - t1_start)/(t4_start - t3_start):.3f}x')

    fig, axs = plt.subplots(4, 1, dpi=300, figsize=(6, 8))
    plt.rcParams['lines.linewidth'] = 1.5
    axs[0].set_title(r'$S_{11}$')
    axs[0].plot(self.time[:], he[:,0],label="python model", color="green")
    axs[0].plot(self.time[:], cpp[:,0],label="cpp model", color="red")
    axs[0].plot(self.time[:], pure_cpp[:,0],label="Pure Cpp model", color="blue")
    axs[1].set_title(r'$S_{12}$')
    axs[1].plot(self.time[:], he[:,1], color="green")
    axs[1].plot(self.time[:], cpp[:,1], color="red")
    axs[1].plot(self.time[:], pure_cpp[:,1], color="blue")
    axs[2].set_title(r'$S_{21}$')
    axs[2].plot(self.time[:], he[:,2], color="green")
    axs[2].plot(self.time[:], cpp[:,2], color="red")
    axs[2].plot(self.time[:], pure_cpp[:,2], color="blue")
    axs[3].set_title(r'$S_{22}$')
    axs[3].plot(self.time[:], he[:,3], color="green")
    axs[3].plot(self.time[:], cpp[:,3], color="red")
    axs[3].plot(self.time[:], pure_cpp[:,3], color="blue")
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='center right',prop={'size': 6})
    fig.tight_layout()
    plt.savefig(f'cpp_test_HE{name}.png', bbox_inches='tight')
    plt.close()

    fig, axs = plt.subplots(4, 1, dpi=300, figsize=(6, 8))
    plt.rcParams['lines.linewidth'] = 1.5
    axs[0].set_title(r'$S_{11}$')
    axs[0].plot(self.time[:], cpp[:,0] - he[:,0],label="cpp model", color="red")
    axs[0].plot(self.time[:], pure_cpp[:,0] - he[:,0],label="Pure Cpp model", color="blue")
    axs[1].set_title(r'$S_{12}$')
    axs[1].plot(self.time[:], cpp[:,1] - he[:,1], color="red")
    axs[1].plot(self.time[:], pure_cpp[:,1] - he[:,1], color="blue")
    axs[2].set_title(r'$S_{21}$')
    axs[2].plot(self.time[:], cpp[:,2] - he[:,2], color="red")
    axs[2].plot(self.time[:], pure_cpp[:,2] - he[:,2], color="blue")
    axs[3].set_title(r'$S_{22}$')
    axs[3].plot(self.time[:], cpp[:,3] - he[:,3], color="red")
    axs[3].plot(self.time[:], pure_cpp[:,3] - he[:,3], color="blue")
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='center right',prop={'size': 6})
    fig.tight_layout()
    plt.savefig(f'cpp_test_HE{name}_res.png', bbox_inches='tight')
    plt.close()
    return he, cpp, pure_cpp
  # The Unit tests
  def test_cpp1(self):
    he, cpp, _ = self.simulate(self.x_HE1)
    assert_almost_equal(he, cpp, decimal=10)
  def test_cpp2(self):
    he, cpp, _ = self.simulate(self.x_HE2)
    assert_almost_equal(he, cpp, decimal=10)
  def test_cpp3(self):
    he, cpp, _ = self.simulate(self.x_HE3)
    assert_almost_equal(he, cpp, decimal=10)
  def test_purecpp1(self):
    he, _, pure_cpp = self.simulate(self.x_HE1)
    assert_almost_equal(he, pure_cpp, decimal=10)
  def test_purecpp2(self):
    he, _, pure_cpp = self.simulate(self.x_HE2)
    assert_almost_equal(he, pure_cpp, decimal=10)
  def test_purecpp3(self):
    he, _, pure_cpp = self.simulate(self.x_HE3)
    assert_almost_equal(he, pure_cpp, decimal=10)


if __name__=="__main__":
  tcase = hyperelastic_simulations()
  tcase.plot(tcase.x_HE3, '3')
  tcase.plot(tcase.x_HE2, '2')
  tcase.plot(tcase.x_HE1, '1')
  unittest.main()
