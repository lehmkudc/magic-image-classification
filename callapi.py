import numpy as np
import pandas as pd
import requests
from PIL import Image
import os
from io import BytesIO
from numpy import random
from scipy import misc, ndimage
from time import clock, sleep
import timeit
import imagehash as ih
import pyodbc

def CardFileName( set_name, card_number ):
    fname = 'images/' + set_name + '_' + str(card_number) + '.png'
    return fname

def CardName( set_name, card_number ):
    cname = set_name + '_' + str(card_number)
    return cname

def CallImage( set_name , card_number ):
    if os.path.isfile(CardFileName(set_name, card_number)):
        pass
    else:
        base = "https://img.scryfall.com/cards/png/en/"
        card_url = base + set_name + '/' + str(card_number) + '.png'
        im = Image.open(BytesIO(requests.get(card_url).content))
        im.save( 'images/' + set_name + '_' + str(card_number) + '.png')
        print( "Called API")

def RemoveImage( set_name, card_number ):
    if os.path.isfile(CardFileName(set_name, card_number)):
        os.remove( CardFileName(set_name, card_number) )

def PullImage( set_name , card_number ):
    im = Image.open( 'images/' + set_name + '_' + str(card_number) + '.png' )
    im = np.array(im)[:,:,0:3]
    return im

def s_plot(img):
    Image.fromarray(img).show()

def line( x0, y0, x1, y1):
    x = np.arange( x0, x1+1 , 1)
    m = (y1 - y0)/(x1 - x0)
    y = ( m*( x - x0) + y0 ).astype('int')
    return x,y

def addline( im ):
    thick = int( np.random.uniform( 1, im.shape[1]/100) )
    color = random.randint(2,size = 1)[0]*np.array((255,255,255))
    x0 = int(np.random.uniform( 0, im.shape[0]-1 ))
    y0 = int(np.random.uniform( 0, im.shape[1] ))
    x1 = int(np.random.uniform( x0+1, im.shape[0] ))
    y1 = int(np.random.uniform( 0, im.shape[1] ))
    x = np.array([])
    y = np.array([])
    for i in range(thick):
        xn,yn = line( x0, (y0+i)%im.shape[1] ,x1, (y1 + i)%im.shape[1])
        x = np.append( x, xn ).astype('int')
        y = np.append( y, yn ).astype('int')
    im1 = np.copy(im[:,:,:])
    im1[x,y,:] = color
    return(im1)

def addcircle( im ):
    r = int( np.random.uniform( 1, im.shape[1]/50))
    color = random.randint(2,size = 1)[0]*np.array((255,255,255))
    a = int(np.random.uniform( 0, im.shape[0] ))
    b = int(np.random.uniform( 0, im.shape[1] ))
    nx,ny = im[:,:,1].shape
    x,y = np.ogrid[-a:nx-a,-b:ny-b]
    mask = x*x + y*y <= r*r
    im1 = np.copy(im[:,:,:])
    im1[mask,:] = color
    return(im1)

def addsaltpepper(im):
    prob = np.random.uniform( 0, 0.01)
    rnd = np.random.rand(im.shape[0], im.shape[1])
    im1 = im.copy()
    im1[rnd < prob] = 0
    im1[rnd > 1 - prob] = 255
    return im1

def DirtyImage( im ):
    t1 = timeit.default_timer()
    im1 = np.copy(im[:,:,:])
    tcopy = timeit.default_timer(); print( 'copy time: ' + str(tcopy-t1) )
    for i in range( int( random.uniform(0, 20) ) ):
        im1 = addline(im1)
    tline = timeit.default_timer(); print( 'line time: ' + str(tline-tcopy) )
    for i in range( int( random.uniform(0, 20) ) ):
        im1 = addcircle(im1)
    tcirc = timeit.default_timer(); print( 'circ time: ' + str(tcirc-tline) )
    im1 = addsaltpepper(im1)
    tsalt = timeit.default_timer(); print( 'salt time: ' + str(tsalt-tline) )
    im1 = ndimage.filters.median_filter( im1, int(random.exponential(3)+1))
    tmedi = timeit.default_timer(); print( 'medi time: ' + str(tmedi-tsalt) )
    im1 = ndimage.filters.gaussian_filter( im1, random.exponential(2))
    tgaus = timeit.default_timer(); print( 'gaus time: ' + str(tgaus-tmedi) )
    im1 = ndimage.rotate( im1, random.uniform(-5,5) )
    trota = timeit.default_timer(); print( 'rota time: ' + str(trota-tgaus) )
    return im1

def HashImage( im ):
    # Convert a numpy array image into a hash, convert the hexidecimal into integers
    ph = ih.phash(Image.fromarray(im[:,:,:]))
    vint = np.vectorize(int)
    iph = vint(np.array(list(str(ph))).astype(str),16)
    return iph

#===========================================================================================
# Connect to SQL Server with pyodbc. Because I'm terrible at python, i cant quite get quotes
#   to stop escaping the '/' in the SQL query so I can call server, database, and table separately.
server = 'SQL2016TRAINING'
database = 'magic_images'
table = 'data_v1'
#conn = pyodbc.connect('DRIVER={SQL SERVER};SERVER=.\'+server+';DATABASE ='+database+';Trusted_Connection = yes')

t0 = timeit.default_timer()
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=.\SQL2016TRAINING;DATABASE=magic_images;Trusted_Connection=yes')
tconn = timeit.default_timer(); print( 'conn time: ' + str(tconn-t0) )
cursor = conn.cursor()

# Delete all data in the current SQL Server. This is only needed when the data generating process
#   changes significantly. I would like to make a log of what sets have what data so I dont have 
#   to constantly delete generated data at some point.
cursor.execute( 'DELETE FROM ' +database+'.dbo.'+table)
tdelete = timeit.default_timer(); print( 'dele time: ' + str(tdelete - tconn) )
#==============================================================================================

#==============================================================================================
# The big script that creates data. I will likely change a lot of this to be class-based when
#   I get comfortable enough with OOP python.

# I am currently only working with the kaladesh expansion, which is 274 cards.

card_row = 1   #How many rows per card image do I want?
dt = pd.DataFrame( columns = ['conn','dele','call','pull','copy','line',
                              'circ','salt','medi','gaus','rota','drty','hash'])

for j in range(1):
    t0 = timeit.default_timer()
    set_name = 'kld'
    card_number = j + 1
    CallImage(set_name, card_number)
    tcall = timeit.default_timer(); print( 'call time: ' + str(tcall-t0) )
    im = PullImage(set_name, card_number)
    tpull = timeit.default_timer(); print( 'pull time: ' + str(tpull-tcall) )
    for i in range(card_row):
        t0 = timeit.default_timer()
        im1 = DirtyImage(im)
        tdirty = timeit.default_timer(); print( 'drty time: ' + str(tdirty-t0) )
        iph = HashImage(im1)
        thash = timeit.default_timer(); print( 'hash time: ' + str(thash-tdirty))
        ipha = np.append( iph, "'" + set_name + "_" + str(card_number) + "'" )
        query = 'INSERT INTO '+database+'.dbo.'+table+' VALUES ('+",".join(ipha.astype(str))+')'
        cursor.execute(query)

    cursor.commit()
    print( CardName(set_name, card_number) + ' is finished' )


#RemoveImage(set_name, card_number)
#Roughly 9 seconds to dirty an image.
#print( d_card.head() )
#d_card.to_csv('images/test.csv' )
#os.remove( 'images/' + set_name + '_' + str(card_number) + '.png' )