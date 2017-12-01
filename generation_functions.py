# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 15:49:01 2017

@author: Dustin
"""
import numpy as np
import requests
from PIL import Image
import os
from io import BytesIO
from numpy import random
from scipy import ndimage
import timeit
#import imagehash as ih

def CardFileName( set_name, card_number ):
    fname = 'images/' + set_name + '_' + str(card_number) + '.png'
    return fname

def CardName( set_name, card_number ):
    cname = set_name + '_' + str(card_number)
    return cname

def CallImage( set_name , card_number ):
    # Call the Scryfall API for a png image if it is not currently saved in the
    #       image folder
    if os.path.isfile(CardFileName(set_name, card_number)):
        pass
    else:
        base = "https://img.scryfall.com/cards/png/en/"
        card_url = base + set_name + '/' + str(card_number) + '.png'
        im = Image.open(BytesIO(requests.get(card_url).content))
        im.save( 'images/' + set_name + '_' + str(card_number) + '.png')
        print( "Called API")

def RemoveImage( set_name, card_number ):
    # Delete an image from the image folder
    if os.path.isfile(CardFileName(set_name, card_number)):
        os.remove( CardFileName(set_name, card_number) )

def PullImage( set_name , card_number ):
    # Pull an image from the images folder and give it as a np.array
    im = Image.open( 'images/' + set_name + '_' + str(card_number) + '.png' )
    im = np.array(im)[:,:,0:3]
    return im

def s_PullImage( set_name , card_number ):
    # Pull an image from the images folder and give it as a np.array
    t0 = timeit.default_timer()
    im = Image.open( 'images/' + set_name + '_' + str(card_number) + '.png' )
    topen = timeit.default_timer(); sopen = topen - t0
    im = np.array(im)[:,:,0:3]
    tarra = timeit.default_timer(); sarra = tarra - topen
    times = np.array( (sopen, sarra) )
    return [im,times]

def s_plot(img):
    Image.fromarray(img).show()

def line( x0, y0, x1, y1):
    x = np.arange( x0, x1+1 , 1)
    m = (y1 - y0)/(x1 - x0)
    y = ( m*( x - x0) + y0 ).astype('int')
    return x,y

def addline( im ):
    # Add a scratch mark to a np.array image.
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
    # Adds a smudge to a np.array image
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
    # Adds a layer of salt and pepper noise to a np.array
    prob = np.random.uniform( 0, 0.01)
    rnd = np.random.rand(im.shape[0], im.shape[1])
    im1 = im.copy()
    im1[rnd < prob] = 0
    im1[rnd > 1 - prob] = 255
    return im1

def DirtyImage( im ):
    # An assembly of filters and objects to add to an np.array image to 
    #       randomly produce a new, dirtier image. Outputs as a np.array
    im1 = np.copy(im[:,:,:])
    for i in range( int( random.uniform(0, 20) ) ):
        im1 = addline(im1)
    for i in range( int( random.uniform(0, 20) ) ):
        im1 = addcircle(im1)
    im1 = addsaltpepper(im1)
    #im1 = ndimage.filters.median_filter( im1, int(random.exponential(3)+1))
    im1 = ndimage.filters.gaussian_filter( im1, random.exponential(1))
    #im1 = ndimage.rotate( im1, random.uniform(-2.5, 2.5) )
    im1 = np.array(Image.fromarray(im1).rotate(random.uniform(-2.5,2.5)))
    return im1

def s_DirtyImage( im ):
    t0 = timeit.default_timer()
    im1 = np.copy(im[:,:,:])
    tcopy = timeit.default_timer(); scopy = tcopy - t0
    for i in range( int( random.uniform(0, 20) ) ):
        im1 = addline(im1)
    tline = timeit.default_timer(); sline = tline - tcopy
    for i in range( int( random.uniform(0, 20) ) ):
        im1 = addcircle(im1)
    tcirc = timeit.default_timer(); scirc = tcirc - tline
    im1 = addsaltpepper(im1)
    tsalt = timeit.default_timer(); ssalt = tsalt - tcirc
    #im1 = ndimage.filters.median_filter( im1, int(random.exponential(3)+1))
    im1 = ndimage.filters.gaussian_filter( im1, random.exponential(1))
    tgaus = timeit.default_timer(); sgaus = tgaus - tsalt
    #im1 = ndimage.rotate( im1, random.uniform(-2.5, 2.5) )
    im1 = np.array(Image.fromarray(im1).rotate(random.uniform(-2.5,2.5)))
    trota = timeit.default_timer(); srota = trota - tgaus
    times = np.array( (scopy, sline, scirc, ssalt, sgaus, srota) )
    return [im1, times]

def HashImage( im ):
    # Convert a numpy array image into a hash, convert the hexidecimal into integers
    ph = ih.phash(Image.fromarray(im[:,:,:]))
    vint = np.vectorize(int)
    iph = vint(np.array(list(str(ph))).astype(str),16)
    return iph


def d_reshape( im, width = 84, length = 117):
    # Reshape the np.array image into a pre-determined size and into a 1D array
    im1 = Image.fromarray(im)
    rm1 = im1.resize( (width, length), Image.ANTIALIAS )
    arm1 = np.array(rm1)
    arm1 = arm1[None,:,:,:]
    #fm1 = np.reshape(arm1, 117*84*3)
    return arm1