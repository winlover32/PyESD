# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 11:34:25 2022

@author: dboateng
"""

import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 
import seaborn as sns
import os 
import matplotlib as mpl
import seaborn as sns 

try:  
    from plot_utils import *
    
except:
    from .plot_utils import *


def correlation_heatmap(data, cmap, ax=None, vmax=None, vmin=None, center=0, cbar_ax=None, 
                        add_cbar=True, title=None, label= "Correlation Coefficinet", fig_path=None, fig_name=None,
                        xlabel=None, ylabel=None, fig=None):
    
    if ax is None:
        fig,ax = plt.subplots(1,1, sharex=False, figsize=(15, 13))
        
    
    if add_cbar == True:
        if cbar_ax is None:
            cbar_ax = [0.90, 0.4, 0.02, 0.25]
        
        
        cbar_ax = fig.add_axes(cbar_ax)
        cbar_ax.get_xaxis().set_visible(False)
        cbar_ax.yaxis.set_ticks_position('right')
        cbar_ax.set_yticklabels([])
        cbar_ax.tick_params(size=0)
        
    sns.set(font_scale=1.2)
    if all(parameter is not None for parameter in [vmin, vmax]):
        
        sns.heatmap(ax=ax, data=data, cmap=cmap, vmax=vmax, vmin=vmin, center=center, cbar=add_cbar,
                    square=True, cbar_ax = cbar_ax, cbar_kws={"label": label, "shrink":0.5,
                                                              "drawedges": False},
                    linewidth=0.5, linecolor="black")
    else:
        
        sns.heatmap(ax=ax, data=data, cmap=cmap, robust=True, cbar=add_cbar,
                    square=True, cbar_ax = cbar_ax, cbar_kws={"label": label, "shrink":0.5,
                                                              "drawedges": False},
                    linewidth=0.5, linecolor="black")
    
    if xlabel is not None:
        ax.set_xlabel(xlabel, fontsize=18)
        ax.set_ylabel(ylabel, fontsize=18)
    
    plt.tight_layout()
    
    plt.subplots_adjust(left=0.15, right=0.88, top=0.97, bottom=0.05)
    
    if fig_path is not None:
        plt.savefig(os.path.join(fig_path, fig_name), bbox_inches="tight", format= "svg")
        

def barplot(methods, stationnames, path_to_data, ax=None, xlabel=None, ylabel=None, 
            varname="test_r2", varname_std="test_r2_std", filename="validation_score_", legend=True,
            fig_path=None, fig_name=None, show_error=False):
    
    if ax is None:
        fig,ax = plt.subplots(1,1, sharex=False, figsize=(18, 15))
        
    df, df_std = barplot_data(methods, stationnames, path_to_data, varname=varname, varname_std=varname_std, 
                     filename=filename)
    
    colors = [selector_method_colors[m] for m in methods]
    mpl.rcParams["axes.prop_cycle"] = cycler("color", colors)
    
    if show_error == True:
        
        df.plot(kind="bar", yerr=df_std, rot=0, ax=ax, legend = legend, fontsize=20, capsize=4)
    else:
        
        df.plot(kind="bar", rot=0, ax=ax, legend = legend, fontsize=20, capsize=4)
        
        
        
    if xlabel is not None:
        ax.set_ylabel(ylabel, fontweight="bold", fontsize=20)
        ax.set_xlabel(xlabel, fontweight="bold", fontsize=20)
        
    if legend ==True:    
        ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1), borderaxespad=0., frameon=True, fontsize=20)
    plt.tight_layout()
    plt.subplots_adjust(left=0.05, right=0.95, top=0.97, bottom=0.05)
    
    if fig_path is not None:
        plt.savefig(os.path.join(fig_path, fig_name), bbox_inches="tight", format= "svg")
        

def boxplot(regressors, stationnames, path_to_data, ax=None, xlabel=None, ylabel=None, 
            varname="test_r2", filename="validation_score_",
            fig_path=None, fig_name=None):
    
    if ax is None:
        fig,ax = plt.subplots(1,1, sharex=False, figsize=(20, 15))
    
    
    scores = boxplot_data(regressors, stationnames, path_to_data, filename=filename, 
                     varname=varname)
    
    color = { "boxes": black,
              "whiskers": green,
              "medians": orange,
              "caps": black,
               }
    
    
    scores.plot(kind= "box", rot=0, ax=ax, fontsize=20, color= color, sym="r+", grid=False,
                )
    
    if xlabel is not None:
        ax.set_ylabel(ylabel, fontweight="bold", fontsize=20)
        ax.set_xlabel(xlabel, fontweight="bold", fontsize=20)
        
    plt.tight_layout()
    plt.subplots_adjust(left=0.05, right=0.95, top=0.97, bottom=0.05)
    
    if fig_path is not None:
        plt.savefig(os.path.join(fig_path, fig_name), bbox_inches="tight", format= "svg")


def heatmaps(data, cmap, label=None, title=None, vmax=None, vmin=None, center=None, ax=None,
             cbar=True, cbar_ax=None):
    
    if ax is None:
        fig,ax = plt.subplots(1,1, figsize=(20,15))
        plt.subplots_adjust(left=0.02, right=1-0.02, top=0.94, bottom=0.45, hspace=0.25)
    
    if all(parameter is not None for parameter in [vmax, vmin, center]):
        
        if cbar == False:
            sns.heatmap(data=data, ax=ax, cmap=cmap, vmax=vmax, vmin=vmin, center=center, 
                        square=True, cbar=cbar, linewidth=0.3)
        else:
            sns.heatmap(data=data, ax=ax, cmap=cmap, vmax=vmax, vmin=vmin, center=center, 
                        square=True, cbar=cbar, cbar_kws={"label":label, 
                                                          "shrink":.50,}, cbar_ax=cbar_ax,
                        linewidth=0.3)
    else:
        if cbar == False:
            sns.heatmap(data=data, ax=ax, cmap=cmap, square=True, cbar=cbar, linewidth=0.3)
        else:
            sns.heatmap(data=data, ax=ax, cmap=cmap, square=True, cbar=cbar,
                        cbar_kws={"label":label,"shrink":.50,}, cbar_ax=cbar_ax,
                        linewidth=0.3)
        
    ax.set_title(title)
    
    
    
    
    
    