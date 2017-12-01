# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 14:52:07 2017

@author: Dustin
"""

import numpy as np
import pandas as pd
import generation_functions as gf
from timeit import default_timer


train_images = []
train_labels = []
row_per_card = 100

for j in range(274):
    t0 = default_timer()
    set_name = 'kld'
    card_number = j + 1
    gf.CallImage(set_name, card_number)
    im = gf.PullImage(set_name, card_number)
    for i in range(row_per_card):
        im1 = gf.DirtyImage(im)
        im2 = gf.d_reshape(im1)
        train_images.append( im2 )
        train_labels.append( gf.CardName(set_name, card_number))
    t1 = default_timer(); t_percard = t1 - t0
    print( set_name + str(card_number) + ' is complete! ' + str(t_percard) + 'seconds')
    
train_images = np.concatenate( train_images, axis = 0)
train_labels = np.concatenate( train_labels, axis = 0)

np.savez('train_images.npz', train_images)
np.savez('train_labels.npz', train_labels)
    
#dp = pd.read_csv('C:/Users/Dustin/Desktop/thumbnail_data.csv')



#server = 'SQL2016TRAINING'
#database = 'magic_images'
#table = 'data_v1'
#conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=.\'+server+';DATABASE ='+database+';Trusted_Connection = yes')

#conn = pyodbc.connect('DRIVER={SQL Server};SERVER=.\SQL2016TRAINING;DATABASE=magic_images;Trusted_Connection=yes')
#cursor = conn.cursor()

# Delete all data in the current SQL Server. This is only needed when the data generating process
#   changes significantly. I would like to make a log of what sets have what data so I dont have 
#   to constantly delete generated data at some point.
# cursor.execute( 'DELETE FROM ' +database+'.dbo.'+table)

#query = 'INSERT INTO '+database+'.dbo.'+table+' VALUES ('+",".join(ipha.astype(str))+')'
#cursor.execute(query)
#cursor.commit()