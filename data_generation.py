# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 15:51:36 2017

@author: Dustin
"""

import numpy as np
import pandas as pd
import pyodbc
import generation_functions as gf

server = 'SQL2016TRAINING'
database = 'magic_images'
table = 'data_v1'
#conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=.\'+server+';DATABASE ='+database+';Trusted_Connection = yes')

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=.\SQL2016TRAINING;DATABASE=magic_images;Trusted_Connection=yes')
cursor = conn.cursor()

# Delete all data in the current SQL Server. This is only needed when the data generating process
#   changes significantly. I would like to make a log of what sets have what data so I dont have 
#   to constantly delete generated data at some point.
cursor.execute( 'DELETE FROM ' +database+'.dbo.'+table)


card_row = 100   #How many rows per card image do I want?
dt = pd.DataFrame( columns = ['conn','dele','call','pull','copy','line',
                              'circ','salt','medi','gaus','rota','drty','hash'])
for j in range(274):
    set_name = 'kld'
    card_number = j + 1
    gf.CallImage(set_name, card_number)
    im = gf.PullImage(set_name, card_number)
    for i in range(card_row):
        im1 = gf.DirtyImage(im)
        iph = gf.HashImage(im1)
        ipha = np.append( iph, "'" + set_name + "_" + str(card_number) + "'" )
        query = 'INSERT INTO '+database+'.dbo.'+table+' VALUES ('+",".join(ipha.astype(str))+')'
        cursor.execute(query)

    cursor.commit()
    print( gf.CardName(set_name, card_number) + ' is finished' )
