#!/usr/bin/env python3
import os, sys
import enum
import typing as tp
import numpy as np
from numpy.typing import NDArray
from numpy import empty, ascontiguousarray, mean, empty_like, sqrt, zeros_like, absolute
from scipy import interpolate, stats, linalg
from .hermite_poly import get_linear_matrix, hermite_interpolation, get_hermite_matrix
from time import perf_counter
# import opt_einsum.contract as einsum
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import lsqr

import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(
  prog='Python Cheart Pfile Interface',
  description=
"""
Description to be added
""", formatter_class=RawTextHelpFormatter)
parser.add_argument('file', type=str,
  help='File name of data to be processed')


class ElemType(enum.IntEnum):
  POINT = 0
  LINEAR = 1
  HERMITE = 2


def get_elem_type(pt:int) -> ElemType:
  if pt < 6:
    return ElemType.LINEAR
  else:
    return ElemType.HERMITE


def get_n_data(index:NDArray[np.int32], nelem:tp.Optional[int]=None, div=12) -> tp.Tuple[NDArray[np.int32], tp.List[ElemType]]:
  npoints = ascontiguousarray([(j-i) for (i,j) in zip(index, index[1:] + 1)])
  elem_types = [get_elem_type(i) for i in npoints]
  if npoints[0] == 1:
    elem_types[0] = ElemType.POINT
  # if (npoints < 4).all():
  #   raise ValueError(">>>ERROR: Attempting to create Hermite elements with less than 4 data points in range. The problem is singular.")
  ne = (npoints//div).astype(int)
  ne = ascontiguousarray([max(n, 1) for n in ne])
  if nelem is not None:
    ne = ascontiguousarray([min(n, nelem) for n in ne])
  return ne, elem_types


def make_joint_map(protocols:NDArray[np.int32], etypes:tp.List[ElemType]) -> tp.Tuple[tp.List[NDArray[np.int32]], tp.List[int]]:
  n = 0
  map = list()
  joints = list()
  nodes = [0]
  for p, k in zip(protocols, etypes):
    if k is ElemType.HERMITE:
      for _ in range(1, 2*(p+1)):
        n = n + 1
        nodes.append(n)
    elif k is ElemType.LINEAR:
      n = n + 1
      nodes.append(n)
    elif k is ElemType.POINT:
      pass
    else:
      raise ValueError(">>>ERROR: Invalid element type found.")
    map.append(ascontiguousarray(nodes))
    if k is ElemType.HERMITE:
      nodes = [n-1]
    elif k is ElemType.LINEAR:
      nodes = [n]
    elif k is ElemType.POINT:
      nodes = [n]
    joints.append(nodes[0])
  return map, joints


def assemble_hermite_mat(time:NDArray[np.float64], index:NDArray[np.int32], nelem:tp.Optional[int]=None, div=16):
  # nt = len(time)
  ne, etypes = get_n_data(index, nelem, div)

  nnode = np.sum([t.value * (i + 1) - (min(t.value, 1)) for (i, t) in zip(ne, etypes)]) + 1

  map, joints = make_joint_map(ne, etypes)
  # print(map)
  # print('\n\n\n')
  # print(joints)
  a     = np.zeros((time.size, nnode), dtype=float)
  Ainv  = np.zeros_like(a.T, dtype=float)
  for k, (t, i, j) in enumerate(zip(etypes, index, index[1:] + 1)):
    if t is ElemType.HERMITE:
      mat = get_hermite_matrix(x=time[i:j], t0=time[i], tend=time[j - 1], n=ne[k])
    elif t is ElemType.LINEAR:
      mat = get_linear_matrix(x=time[i:j], t0=time[i], tend=time[j - 1])
    elif t is ElemType.POINT:
      mat = np.ones((1,1), dtype=np.float64)
    else:
      raise ValueError(">>>ERROR: Invalid element type found.")
    try:
      a[i:j, map[k]] = a[i:j, map[k]] + mat
    except:
      print("Error caused by ", k, map[k], t, i, j)
      raise
    Ainv[map[k], i:j] = Ainv[map[k], i:j] + linalg.pinv(mat)
  for j in index[1:-1]:
    a[j,:] = 0.5 * a[j,:]
  for k in joints[:-1]:
    Ainv[k,:] = 0.5 * Ainv[k, :]
  return ne, map, csr_matrix(a), csr_matrix(Ainv)


class HermiteFilter:

  def __init__(self, time:NDArray[np.float64], index:NDArray[np.int32], nelem:tp.Optional[int]=None, div:int=16) -> None:
    nt = len(time)
    self.time  = time
    self.index = index
    self.end   = nt - 1
    self.nelems, self.map, self.A, self.Ainv = assemble_hermite_mat(time, index, nelem, div)
    self.nonzero = self.Ainv.count_nonzero()
    self.size    = self.Ainv.shape[0] * self.Ainv.shape[1]
    self.sparsity = self.nonzero/self.size
    # self.Ainv  = linalg.pinv(A)
    self.intervals = list(zip(index, index[1:] + 1))
    self.dof   = time.size - 2*self.nelems.size
    self.all_vals = np.arange(0, nt)
    # print(self.map)
    # print(self.elems)
    # print(self.index[:-1])
    # print(self.index[1:])


  def interp2(self, data:NDArray[np.float64]):
    # pars = np.einsum("ij,j->i", self.Ainv, data)
    pars = self.Ainv.dot(data)
    # pars = lsqr(self.A, data)[0]
    filtered = empty_like(data)
    for m, k, i, j in zip(self.map, self.nelems, self.index, self.index[1:] + 1):
      # print(min(self.time[i:j]), max(self.time[i:j]))
      filtered[i:j] = hermite_interpolation(self.time[i:j], pars[m], self.time[i], self.time[j - 1], n=k)
    return filtered

  def interp(self, data:NDArray[np.float64]):
    pars = self.Ainv.dot(data)
    return self.A.dot(pars)

  def filter(self, data:NDArray[np.float64], eps_base:float=0.15):
    filtered = self.interp(data)
    eps = filtered - data
    eps = 2.1 * sqrt(np.einsum('i,i->', eps, eps) / self.dof) + eps_base
    bad_list = list()
    for i, j in zip(self.index, self.index[1:] + 1):
      for m in range(i+1,j-1):
        if abs(data[m] - filtered[m]) > eps:
          # print(abs(data[m] - filtered[m]), ' > ', eps)
          for n in range(m-1, m+1):
            if (i < n < j-1):
              bad_list.append(n)
    nodes = np.setdiff1d(self.all_vals, bad_list)
    # print(len(bad_list), ' and ', len(nodes),' of ', self.end)
    f = interpolate.interp1d(self.time[nodes], data[nodes])
    return f(self.time)

  def nested_filter(self, data:NDArray[np.float64], eps_base:float=0.15, nest=5):
    fixed = data.copy()
    for _ in range(nest):
      fixed = self.filter(fixed, eps_base=eps_base)
    return fixed




if __name__=='__main__':

  from time import perf_counter
  import matplotlib.pyplot as plt
  # pars = array([0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10], dtype=float)
  x = np.linspace(0,20,101)
  y = np.exp(-0.2*x)*np.sin(x) + 10
  t1 = perf_counter()
  filter = HermiteFilter(time=x, index=np.array([0, 20, 50, 100]), nelem=4, div=8)
  v2 = filter.interp2(y)
  v = filter.interp(y)
  print(np.linalg.norm(v - v2))
  t2 = perf_counter()
  # print(t2-t1)
  plt.plot(x, y, 'o', label='data')
  plt.plot(x, v, label='least squares fit, $y = a + bx^2$')
  plt.plot(x, v2, label='matrix squares fit, $y = a + bx^2$')
  plt.xlabel('x')
  plt.ylabel('y')
  plt.legend(framealpha=1, shadow=True)
  plt.grid(alpha=0.25)
  plt.show()

