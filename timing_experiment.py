# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 11:20:54 2017

@author: Dustin
"""

import numpy as np
import pandas as pd
import generation_functions as gf
import timeit


train_images = []
train_labels = []
total_times = []
for j in range(20): #Max of 274
    set_name = 'kld'
    card_number = j + 1
    gf.CallImage(set_name, card_number)
    [im,ptimes] = gf.s_PullImage(set_name, card_number)
    [im1,dtimes] = gf.s_DirtyImage(im)
    t0 = timeit.default_timer()
    im2 = gf.d_reshape(im1)
    tresh = timeit.default_timer(); sresh = tresh - t0
    train_images.append(im2)
    tappe = timeit.default_timer(); sappe = tappe - tresh
    ftimes = np.array( (sresh, sappe))
    t_times = np.concatenate( (ptimes, dtimes, ftimes) )
    t_times = t_times[None,:]
    total_times.append(t_times)
    
time_labels = ('open','arra','copy','line','circ','salt','gaus','rota','resh','appe')
time_data = np.concatenate( total_times , axis = 0)
train_data = np.concatenate( train_images, axis = 0)

d_times = pd.DataFrame( time_data, columns = time_labels)
d_times
