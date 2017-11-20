# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 14:52:07 2017

@author: Dustin
"""

import numpy as np
import pandas as pd
import generation_functions as gf


dum = np.matrix( np.empty(117*84*3))
dum[:] = np.NAN

df = pd.DataFrame(dum)
df.insert( 0, "name", "")
df.drop(0, inplace = True)

df.to_csv('tumbnail_data.csv')

row_per_card = 100
for j in range(50):
    set_name = 'kld'
    card_number = j + 1
    gf.CallImage(set_name, card_number)
    im = gf.PullImage(set_name, card_number)
    for i in range(row_per_card):
        im1 = gf.DirtyImage(im)
        iph = gf.d_reshape(im1)
        ipha = np.append( "'" + set_name + "_" + str(card_number) + "'", iph )
        df.loc[len(df)] = ipha
    with open('thumbnail.csv','a') as f:
        df.to_csv(f, header=False)