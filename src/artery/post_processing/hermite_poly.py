#!/usr/bin/env python3
import numpy as np
from numpy import ascontiguousarray as array
from numpy import ndarray, zeros, empty
from scipy.linalg import lstsq

def unit_hermite(t):
  """
  2t^3 - 3t^2 + 1 = 2t^3 - 2t^2 - t^2 + 1
  t^3 - 2t^2  + t = t^3 - t^2 - t^2  + t
  -2t^3 + 3t^2    = -2t^3 + 2t^2 + t^2
  t^3 - t^2       = t^3 - t^2

  with m1 = t^3 - t^2:
    2*m1 - t^2 + 1
    m1 - t^2 + t
    -2*m1 + t^2
    m1

  with m1 = t^3 - t^2, v0 = m1 - t^2:
    m1 + v0 + 1
    v0 + t
    -m1 - v0
    m1

  with m1 = t^3 - t^2, v0 = m1 - t^2, v1 = m1 + v0:
    v1 + 1
    v0 + t
    -v1
    m1
  """
  if 0.0 <= t <= 1.0:
    t2 = t * t
    m1 = (t2 - t) * t
    v0 = m1 - t2
    v1 = v0 + m1
    return array([v1 + 1.0, v0 + t, -v1, m1])
  else:
    return zeros((4,), dtype=float)


def hermite_interpolation(x:ndarray, pars:ndarray, t0:float, tend:float, n:int):
  check = np.all((x >= t0) & (x <= tend))
  if not check:
    raise ValueError(f'x not in bounds')
  y = empty((x.size), dtype=float)
  delta_t = (tend - t0)/float(n)

  bin, t = np.divmod(x - t0, delta_t)
  bin = bin.astype(int)

  t = t / delta_t

  end = (bin==n)
  bin[end] = n - 1
  t[end] = 1.0
  for i, (b, v) in enumerate(zip(bin, t)):
    y[i] = pars[2*b:2*b+4] @ unit_hermite(v)
    # try:
    #   y[i] = pars[2*b:2*b+4] @ unit_hermite(v)
    # except:
    #   y[i] = pars[2*b:2*b+2] @ unit_hermite(v)[:2]
  return y

def get_hermite_matrix(x:ndarray, t0:float, tend:float, n:int):
  # print(min(x), t0, max(x), tend)
  check = np.all((x >= t0) & (x <= tend))
  if not check:
    raise ValueError(f'x not in bounds')
  A = zeros((x.size, 2*(n+1)), dtype=float)
  # print(A.shape)
  delta_t = (tend - t0)/float(n)
  bin, t = np.divmod(x - t0, delta_t)
  bin = bin.astype(int)
  t = t / delta_t
  end = (bin==n)
  bin[end] = n - 1
  t[end] = 1.0
  _, counts = np.unique(bin, return_counts=True)
  if (counts < 4).all():
    raise ValueError(f">>>ERROR: Attempting to create Hermite elements with less than 4 data points in range, {t0}:{tend}. The problem is singular.")
  for i, (b, v) in enumerate(zip(bin, t)):
    A[i, 2*b:2*b+4] = unit_hermite(v)
    # try:
    #   A[i, 2*b:2*b+4] = unit_hermite(v)
    # except:
    #   A[i, 2*b:2*b+2] = unit_hermite(v)[:2]
  return A


def get_linear_matrix(x:ndarray, t0:float, tend:float):
  # print(min(x), t0, max(x), tend)
  if 0.0 > (tend - t0):
    raise ValueError(f'bounds for curve is not appropriate. tend < t0 at time = {t0} to {tend}, {x}')
  check = np.all((x >= t0) & (x <= tend))
  if not check:
    raise ValueError(f'x not in bounds')
  t = (x - t0) / (tend - t0)
  A = np.c_[1-t, t]
  # A[A>1] = 0.0
  # A[A<0] = 0.0
  return A


def hermite_fit(x:ndarray, v:ndarray, t0:float, tend:float, n:int):
  A = get_hermite_matrix(x, t0, tend, n)
  b, *_ = lstsq(A, v, lapack_driver='gelsy',check_finite=False)
  return b



if __name__=='__main__':

  from time import perf_counter
  import matplotlib.pyplot as plt
  # pars = array([0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10], dtype=float)
  x = np.linspace(0,20,100)
  y = np.exp(-0.2*x)*np.sin(x)
  t1 = perf_counter()
  pars = hermite_fit(x, y, 0, 20, 10)
  v = hermite_interpolation(x, pars, 0, 20, 10)
  t2 = perf_counter()
  print(pars)
  print(t2-t1)
  plt.plot(x, y, 'o', label='data')
  plt.plot(x, v, label='least squares fit, $y = a + bx^2$')
  plt.xlabel('x')
  plt.ylabel('y')
  plt.legend(framealpha=1, shadow=True)
  plt.grid(alpha=0.25)
  plt.show()

