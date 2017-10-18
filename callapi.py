import numpy as np
import pandas as pd
import requests
from PIL import Image
import os
from io import BytesIO
from numpy import random
from scipy import misc, ndimage
from time import clock
import timeit
import imagehash as ih

def CardFileName( set_name, card_number ):
    fname = 'images/' + set_name + '_' + str(card_number) + '.png'
    return fname

def CallImage( set_name , card_number ):
    if os.path.isfile(CardFileName(set_name, card_number)):
        pass
    else:
        base = "https://img.scryfall.com/cards/png/en/"
        card_url = base + set_name + '/' + str(card_number) + '.png'
        im = Image.open(BytesIO(requests.get(card_url).content))
        im.save( 'images/' + set_name + '_' + str(card_number) + '.png')
        print( "Called API")

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
    im1 = np.copy(im[:,:,:])
    for i in range( int( random.uniform(0, 20) ) ):
        im1 = addline(im1)
    for i in range( int( random.uniform(0, 20) ) ):
        im1 = addcircle(im1)
    im1 = addsaltpepper(im1)
    im1 = ndimage.filters.median_filter( im1, int(random.exponential(3)+1))
    im1 = ndimage.filters.gaussian_filter( im1, random.exponential(2))
    im1 = ndimage.rotate( im1, random.uniform(-5,5) )
    return im1

def HashImage( im ):
    ph = ih.phash(Image.fromarray(im[:,:,:]))
    vint = np.vectorize(int)
    iph = vint(np.array(list(str(ph))).astype(str),16)
    return iph


set_name = 'kld'
card_number = 3

CallImage(set_name, card_number)
im = PullImage(set_name, card_number)
im1 = DirtyImage(im)
iph = HashImage(im1)
print( iph )

#os.remove( 'images/' + set_name + '_' + str(card_number) + '.png' )