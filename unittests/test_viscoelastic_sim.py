#!/usr/bin/env pathon3

import numpy as np
from numpy import zeros, array
from numpy.testing import assert_almost_equal
from artery.matlaws.hog20132D import *
from artery.matlaws.caputoD import *
from artery.matlaws.artery_models import (Femoral_VESimulation, Femoral_VESimulation_Scaled)
import matplotlib.pyplot as plt
from time import perf_counter
import unittest

__unittest = True

def simulate_frac(pars:ndarray, struc:ndarray, args: ndarray, dt: ndarray, alpha = 0.1):
  model      = hog20132D(pars, struc[0], struc[1], struc[2])
  steps, dim = args.shape
  matrix   = zeros((steps, dim))
  collagen = zeros((steps, dim))
  elastin  = zeros((steps, dim))
  smc      = zeros((steps, dim))
  pg       = zeros((steps, 1))
  pc       = zeros((steps, 1))
  cinv     = zeros((steps, dim))
  for i, a in enumerate(args):
    matrix[i], collagen[i], elastin[i], smc[i], pg[i], pc[i], cinv[i] = model.stress_parts(a)
  carpC0 = caputo_init(alpha, 3000.0, 9, dim=1)
  carpC  = caputo_init(alpha, 3000.0, 9, dim=4)
  carpM  = caputo_init(alpha, 3000.0, 9, dim=4)
  Sc = zeros((steps, dim))
  Sm = zeros((steps, dim))
  Sp = zeros((steps, 1))
  Sr = zeros((steps, dim))
  for i, (d, v) in enumerate(zip(dt[1:], collagen[1:]), start=1):
    Sc[i], carpC = caputo_derivative1_iter(v, d, carpC)
  for i, (d, v) in enumerate(zip(dt[1:], smc[1:]), start=1):
    Sm[i], carpM = caputo_derivative1_iter(v, d, carpM)
  for i, (d, v) in enumerate(zip(dt[1:], pc[1:]), start=1):
    Sp[i], carpC0 = caputo_derivative1_iter(v, d, carpC0)
    Sr[i] = matrix[i] + Sc[i] + elastin[i] + Sm[i] - (pg[i,0] + Sp[i,0]) * cinv[i]
  return Sr


class viscoelastic_simulations(unittest.TestCase):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    file_name = 'unittests/test_data'
    datazip = np.load(f'{file_name}.npz')
    index  = datazip['index']
    self.time   = datazip['time']
    self.dt     = datazip['dt']
    self.strain = datazip['strain']
    self.pos = index[1]
    self.x_HE3 = array([5.37650604, 17.41700370, 1.19482728, 4.62237796, 1.77045881, 11.70175783, 0.00031839, 0.17641521])
    # self.x_HE3 = array([5.37650604, 17.41700370, 1.19482728, 4.62237796, 1.77045881, 0.0, 0.00031839, 0.17641521])
    self.x_HE2 = array([5.37650604, 17.41700370, 1.19482728, 0, 1.77045881, 0, 0.00031839, 0.17641521])
    self.x_HE1 = array([5.37650604, 0.0, 1.19482728, 0, 1.77045881, 0, 0.00031839, 0.17641521])

  def simulate(self, x_HE):
    frac      = simulate_frac(x_HE[:7], array([x_HE[7], 0.155, 0.424285714285714]), self.strain, self.dt, alpha=0.1)
    pure_frac = Femoral_VESimulation(x_HE[:7], array([0.0, x_HE[7]]), array([0.1, 0.1]), 3000.0, array([1.0, 0.0, 0.0, 1.0]), self.strain, self.dt)
    return frac[1:], pure_frac[1:]

  def plot(self, x_HE, name):
    t1_start  = perf_counter()
    frac      = simulate_frac(x_HE[:7], array([x_HE[7], 0.155, 0.424285714285714]), self.strain, self.dt, alpha=0.1)
    t2_start  = perf_counter()
    pure_frac = Femoral_VESimulation(x_HE[:7], array([0.0, x_HE[7]]), array([0.1, 0.1]), 3000.0, array([1.0, 0.0, 0.0, 1.0]), self.strain, self.dt)
    t3_start  = perf_counter()
    print(f'Python completed in {t2_start - t1_start} seconds')
    print(f'Cpp completed in {t3_start - t2_start} seconds and speed gain of {(t2_start - t1_start)/(t3_start - t2_start):.3f}x')

    fig, axs = plt.subplots(4, 1, dpi=300, figsize=(120, 8))
    plt.rcParams['lines.linewidth'] = 1.5
    axs[0].set_title(r'$S_{11}$')
    axs[0].plot(self.time[self.pos:], frac[self.pos:,0],label="python model", color="green")
    axs[0].plot(self.time[self.pos:], pure_frac[self.pos:,0],label="Pure Cpp model", color="blue")
    axs[1].set_title(r'$S_{12}$')
    axs[1].plot(self.time[self.pos:], frac[self.pos:,1], color="green")
    axs[1].plot(self.time[self.pos:], pure_frac[self.pos:,1], color="blue")
    axs[2].set_title(r'$S_{21}$')
    axs[2].plot(self.time[self.pos:], frac[self.pos:,2], color="green")
    axs[2].plot(self.time[self.pos:], pure_frac[self.pos:,2], color="blue")
    axs[3].set_title(r'$S_{22}$')
    axs[3].plot(self.time[self.pos:], frac[self.pos:,3], color="green")
    axs[3].plot(self.time[self.pos:], pure_frac[self.pos:,3], color="blue")
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='center right',prop={'size': 6})
    fig.tight_layout()
    plt.savefig(f'cpp_frac{name}_test.png', bbox_inches='tight')
    plt.close()

    fig, axs = plt.subplots(4, 1, dpi=300, figsize=(6, 8))
    plt.rcParams['lines.linewidth'] = 1.5
    axs[0].set_title(r'$S_{11}$')
    axs[0].plot(self.time[self.pos:], pure_frac[self.pos:,0] - frac[self.pos:,0], label="Pure Cpp model", color="blue")
    axs[1].set_title(r'$S_{12}$')
    axs[1].plot(self.time[self.pos:], pure_frac[self.pos:,1] - frac[self.pos:,1], color="blue")
    axs[2].set_title(r'$S_{21}$')
    axs[2].plot(self.time[self.pos:], pure_frac[self.pos:,2] - frac[self.pos:,2], color="blue")
    axs[3].set_title(r'$S_{22}$')
    axs[3].plot(self.time[self.pos:], pure_frac[self.pos:,3] - frac[self.pos:,3], color="blue")
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='center right',prop={'size': 6})
    fig.tight_layout()
    plt.savefig(f'cpp_frac{name}_test_res.png', bbox_inches='tight')
    plt.close()

  def test_cpp1(self):
    ve, cpp, = self.simulate(self.x_HE1)
    assert_almost_equal(ve, cpp, decimal=12)
  def test_cpp2(self):
    ve, cpp, = self.simulate(self.x_HE2)
    assert_almost_equal(ve, cpp, decimal=12)
  def test_cpp3(self):
    ve, cpp, = self.simulate(self.x_HE3)
    assert_almost_equal(ve, cpp, decimal=12)



if __name__=="__main__":

  tcase = viscoelastic_simulations()
  tcase.plot(tcase.x_HE3, '3')
  tcase.plot(tcase.x_HE2, '2')
  tcase.plot(tcase.x_HE1, '1')
  unittest.main()
