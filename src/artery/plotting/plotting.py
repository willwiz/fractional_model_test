#!/usr/bin/env python3
from cycler import cycler
import matplotlib.pyplot as plt
import typing as tp
from itertools import cycle
from numpy.typing import NDArray as Arr
from numpy import float64 as dbl

plt.rc('lines', linewidth=0.75)
# plt.rc('axes', prop_cycle=(cycler('color', ['k', 'r', 'b', 'g', 'm', 'k']) +
#                            cycler('mec', ['k', 'r', 'b', 'g', 'm', 'k'])))
# plt.rc('axes', prop_cycle=(cycler('color', ['k', 'r']) +
#                            cycler('linestyle', ['None', '-'])+
#                            cycler('marker', ['o','None'])+
#                            cycler('mec', ['k', 'r'])))
# plt.rc('axes', prop_cycle=(cycler('color', ['k', 'r', 'b', 'g', 'm', 'k']) +
#                            cycler('linestyle', ['None', '-', '-', '-', '-', '-'])+
#                            cycler('marker', ['o','None', 'None', 'None', 'None', 'None'])+
#                            cycler('mec', ['k', 'r', 'b', 'g', 'm', 'k'])))

def get_plotsize(row:bool, n:int, width:tp.Optional[int] = None, height:tp.Optional[int] = None):
  if row:
    nr = 1
    nc = n
    if width is None:
      width = n*4
    if height is None:
      height = 3
  else:
    nr = n
    nc = 1
    if width is None:
      width = 4
    if height is None:
      height = n*3
  return nr, nc, width, height


class BasePlot:
  def __init__(self, row:bool=True, width:tp.Optional[float] = 4, height:tp.Optional[float] = 3,
               dpi:int = 300, transparency:bool=False,
               skip:int = 1, msize:int = 3, fillstyle:str='none', mew:float=.2,
               labelx:tp.Optional[tp.Union[tp.List[str], str]]=None,
               labely:tp.Optional[tp.Union[tp.List[str], str]]=None,
               color_list:tp.List[str] = ['k', 'r', 'b', 'g', 'm', 'c', 'y'],
               lines_list:tp.List[str] = ['None', '-', '-', '-', '-', '-', '-'],
               marker_list:tp.List[str] = ['o', 'None', 'None', 'None', 'None', 'None', 'None'],
               left:float|None=0.15, right:float|None=0.98, top:float|None=0.98, bottom:float|None=0.1,
               wspace:float|None=None, hspace:float|None=None
               ) -> None:
    self.dpi = dpi
    self.transparency = transparency
    self.style = {'markersize': msize, 'markevery': skip, 'fillstyle': fillstyle, 'markeredgewidth': mew}
    self.cyclers = (cycler('color', color_list) +
                    cycler('linestyle', lines_list) +
                    cycler('marker', marker_list) +
                    cycler('mec', color_list))
    self.lab_x = labelx
    self.lab_y = labely
    self.row = row
    self.fig, self.axs = plt.subplots(1, 1, dpi=self.dpi, figsize=(width, height))
    self.left = left
    self.right = right
    self.top = top
    self.bottom = bottom
    self.wspace = wspace
    self.hspace = hspace

  def close(self):
    plt.close()

  def plot(self, x:tp.Union[Arr[dbl], tp.List[Arr[dbl]]], *ys:tp.Union[Arr[dbl], tp.List[Arr[dbl]]],
           xlim:tp.Optional[tp.List[float]] = None,
           ylim:tp.Optional[tp.List[float]] = None,
           fout:tp.Optional[str] = None) -> None:
    plt.cla()
    plt.subplots_adjust(left=self.left, right=self.right, top=self.top, bottom=self.bottom, wspace=self.wspace, hspace=self.hspace)
    self.axs.set_prop_cycle(self.cyclers)
    self.axs.set_xlabel(self.lab_x, fontsize=14)
    self.axs.set_ylabel(self.lab_y, fontsize=14)
    if type(x) == list:
      for m in range(len(x)):
        for y in ys:
          self.axs.plot(x[m], y[m], **self.style)
    else:
      for y in ys:
        self.axs.plot(x, y, **self.style)
    if ylim is not None:
      self.axs.set_ylim(ylim)
    if xlim is not None:
      self.axs.set_xlim(xlim)
    # self.fig.tight_layout()
    if fout is None:
      plt.show()
    else:
      plt.savefig(fout, transparent=self.transparency)
      # plt.close()


class vecPlot(BasePlot):
 def plot(self, x:tp.Union[Arr[dbl], tp.List[Arr[dbl]]], *ys:tp.Union[Arr[dbl], tp.List[Arr[dbl]]],
          components:tp.Dict[int, int] = {0:0, 1:3, 2:1, 3:2},
          width:tp.Optional[float] = None, height:tp.Optional[float] = None,
          xlim:tp.Optional[tp.List[float]] = None,
          ylim:tp.Optional[tp.List[float]] = None,
          fout:tp.Optional[str] = None) -> None:
    nr, nc, width, height = get_plotsize(self.row, len(components), width, height)
    fig, axs = plt.subplots(nr, nc, dpi=self.dpi, figsize=(width, height), squeeze=False)
    axs = [a for ax in axs for a in ax]
    ndim = x.ndim
    for ax in axs:
      ax.set_prop_cycle(self.cyclers)
    for k, i in components.items():
      if ndim == 1:
        if type(x) == list:
          for y in ys:
            for u, v in zip(x, y):
              axs[k].plot(u, v[:,i], **self.style)
        else:
          for y in ys:
            axs[k].plot(x, y[:,i], **self.style)
      else:
        if type(x) == list:
          for y in ys:
            for u, v in zip(x, y):
              axs[k].plot(u[:,i], v[:,i], **self.style)
        else:
          for y in ys:
            axs[k].plot(x[:,i], y[:,i], **self.style)
      if ylim is not None:
        axs[k].set_ylim(ylim)
      if xlim is not None:
        axs[k].set_xlim(xlim)
      if type(self.lab_x) == list:
        axs[k].set_xlabel(self.lab_x[k])
      elif type(self.lab_x) == str:
        axs[k].set_xlabel(self.lab_x)
      if type(self.lab_y) == list:
        axs[k].set_ylabel(self.lab_y[k])
      elif type(self.lab_y) == str:
        axs[k].set_ylabel(self.lab_y)
    fig.tight_layout()
    if fout is None:
      plt.show()
    else:
      plt.savefig(fout, bbox_inches='tight', transparent=self.transparency)
      plt.close()


class tensorPlot(BasePlot):
  def plot(self, x:tp.Union[Arr[dbl], tp.List[Arr[dbl]]], *ys:tp.Union[Arr[dbl], tp.List[Arr[dbl]]],
           components:tp.Dict[int, tp.Tuple[int, int]] = {0:(0,0), 1:(1,1), 2:(0,1), 3:(1,0)},
           width:tp.Optional[float] = None, height:tp.Optional[float] = None,
           xlim:tp.Optional[tp.List[float]] = None,
           ylim:tp.Optional[tp.List[float]] = None,
           fout:tp.Optional[str] = None) -> None:
    nr, nc, width, height = get_plotsize(self.row, len(components), width, height)
    fig, axs = plt.subplots(nr, nc, dpi=self.dpi, figsize=(width, height), squeeze=False)
    axs = [a for ax in axs for a in ax]
    ndim = x.ndim
    for ax in axs:
      ax.set_prop_cycle(self.cyclers)
    for k, (i,j) in components.items():
      if ndim == 1:
        if type(x) == list:
          for y in ys:
            for u, v in zip(x, y):
              axs[k].plot(u, v[:,i,j], **self.style)
        else:
          for y in ys:
            axs[k].plot(x, y[:,i,j], **self.style)
      else:
        if type(x) == list:
          for y in ys:
            for u, v in zip(x, y):
              axs[k].plot(u[:,i,j], v[:,i,j], **self.style)
        else:
          for y in ys:
            axs[k].plot(x[:,i,j], y[:,i,j], **self.style)
      if ylim is not None:
        axs[k].set_ylim(ylim)
      if xlim is not None:
        axs[k].set_xlim(xlim)
      if type(self.lab_x) == list:
        axs[k].set_xlabel(self.lab_x[k])
      elif type(self.lab_x) == str:
        axs[k].set_xlabel(self.lab_x)
      if type(self.lab_y) == list:
        axs[k].set_ylabel(self.lab_y[k])
      elif type(self.lab_y) == str:
        axs[k].set_ylabel(self.lab_y)
    fig.tight_layout()
    if fout is None:
      plt.show()
    else:
      plt.savefig(fout, bbox_inches='tight', transparent=self.transparency)
      plt.close()


def plot(fout, x, *ys, labelx="strain", labely=r'$S$ (kPa)', skip=1, msize=3,
    ylim=None, dpi=300, figsize=(4,3)):
  style = {'markersize': msize, 'markevery': skip, 'fillstyle': 'none', 'markeredgewidth': .2}
  fig, axs = plt.subplots(1, 1, dpi=dpi, figsize=figsize)
  axs.set(xlabel=labelx, ylabel=labely)
  custom_cycler = (cycler('color', ['k', 'r']) +
                           cycler('linestyle', ['None', '-'])+
                           cycler('marker', ['o','None'])+
                           cycler('mec', ['k', 'r']))
  axs.set_prop_cycle(custom_cycler)
  for y in ys:
    axs.plot(x, y, **style)
  if ylim is not None:
    axs.set_ylim(ylim)
  fig.tight_layout()
  plt.savefig(fout, bbox_inches='tight', transparent=True)
  plt.close()

def plot_columns_vec(file_name, time, *datas, label='S', legend=['Raw','New'], ylim=None, dpi=300,
                components = {0:0, 1:3, 2:1, 3:2},
                linestyle = None,
                marker=None,
                style = {'markersize': 3, 'markevery': 1, 'fillstyle': 'none', 'markeredgewidth': .2}):
  if linestyle is None:
    linestyle = ['None', '-', '-', '-', '-', '-']
  if marker is None:
    marker = ['o','None', 'None', 'None', 'None', 'None']
  linecycler = cycle(linestyle)
  markercycler = cycle(marker)
  fig, axs = plt.subplots(len(components), 1, dpi=dpi, figsize=(8, 2*len(components)))
  for k, i in components.items():
    for m, d in enumerate(datas):
      axs[k].plot(time, d[:,i], label=legend[m], linestyle=next(linecycler), marker=next(markercycler), **style)
    # axs[k].set_title(fr'${label}_{{{i}}}$')
    if ylim is not None:
      axs[k].set_ylim(ylim)
  handles, labels = axs[0].get_legend_handles_labels()
  # fig.legend(handles, labels, loc='lower right',prop={'size': 11})
  fig.tight_layout()
  plt.savefig(file_name, bbox_inches='tight', transparent=True)
  plt.close()

def plot_rows_vec(file_name, time, *datas, label='S', legend=['Raw','New'], skip=1,
                msize=3, ylim=None, dpi=300,
                components = {0:0, 1:3, 2:1, 3:2}):
  style = {'markersize': msize, 'markevery': skip, 'fillstyle': 'none', 'markeredgewidth': .2}
  fig, axs = plt.subplots(1, len(components), dpi=dpi, figsize=(4*len(components), 3))
  for k, i in components.items():
    for m, d in enumerate(datas):
      axs[k].plot(time[:,i], d[:,i], label=legend[m], **style)
    # axs[k].set_title(fr'${label}_{{{i}}}$')
    if ylim is not None:
      axs[k].set_ylim(ylim)
  handles, labels = axs[0].get_legend_handles_labels()
  # fig.legend(handles, labels, loc='lower right',prop={'size': 11})
  fig.tight_layout()
  plt.savefig(file_name, bbox_inches='tight', transparent=True)
  plt.close()

def plot_tensor_time(file_name, time, *datas, label='S', legend=['Raw','New'], skip=1, msize=3,
    ylim=None, dpi=300, figsize=(8, 8), components = {0:(0,0), 1:(1,1), 2:(0,1), 3:(1,0)}):
  style = {'markersize': msize, 'markevery': skip, 'fillstyle': 'none', 'markeredgewidth': .2}
  fig, axs = plt.subplots(4, 1, dpi=dpi, figsize=figsize)
  for k, (i,j) in components.items():
    for m, d in enumerate(datas):
      axs[k].plot(time, d[:,i,j], label=legend[m], **style)
    # axs[k].set_title(fr'${label}_{{{i}{j}}}$')
    if ylim is not None:
      axs[k].set_ylim(ylim)
  handles, labels = axs[0].get_legend_handles_labels()
  # fig.legend(handles, labels, loc='lower right',prop={'size': 11})
  fig.tight_layout()
  plt.savefig(file_name, bbox_inches='tight', transparent=True)
  plt.close()