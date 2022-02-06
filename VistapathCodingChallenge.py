# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 07:17:00 2022

@author: spandya
"""




from __future__ import print_function
from __future__ import division
import cv2 as cv
import numpy as np
import argparse



def find_tissue(img, imname):
    
    
    ret1, imthresh = cv.threshold(img[:,:,2], 0, 255, cv.THRESH_OTSU)
    
    kernel1 = np.ones((8,8),np.uint8)
    #kernel2 = np.ones((5,5),np.uint8)
    
    opening = cv.morphologyEx(imthresh, cv.MORPH_OPEN, kernel1)
    
    cropped = opening[60:-210, 60:-40]
    imcrop = originalim[60:-210, 60:-40]

    
    
    contours, _ = cv.findContours(cropped, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    ## I can delete this, not necessary
    # Get the moments
    mu = [None]*len(contours)
    for i in range(len(contours)):
        mu[i] = cv.moments(contours[i])
    # Get the mass centers
    mc = [None]*len(contours)
    for i in range(len(contours)):
        # add 1e-8 to avoid division by zero
        mc[i] = (mu[i]['m10'] / (mu[i]['m00'] + 1e-8), mu[i]['m01'] / (mu[i]['m00'] + 1e-8))
    # Draw contours
    
    drawing = np.zeros((cropped.shape[0], cropped.shape[1], 3), dtype=np.uint8)
    
    for i in range(len(contours)):
        color = (0, 0, 255)
        rect = cv.boundingRect(contours[i])
        cv.drawContours(drawing, contours, i, color, 2)
        x,y,w,h = rect
        cv.rectangle(drawing,(x-2,y-2),(x+w+2,y+h+2),(0,255,0),2)
        cv.putText(drawing, "Contour area ={}".format(cv.contourArea(contours[i])), (x, y-10), cv.FONT_HERSHEY_SIMPLEX, .5, (36,255,12), 1)
        cv.circle(drawing, (int(mc[i][0]), int(mc[i][1])), 4, color, -1)
    
    dst = cv.addWeighted(imcrop, 0.5, drawing, 0.5, 0.0)
    cv.imshow(imname, dst)
    
    # Calculate the area with the moments 00 and compare with the result of the OpenCV function
    for i in range(len(contours)):
        print(' * Contour[%s][%d] - Area = %.2f px' % (imname,i, cv.contourArea(contours[i])))
        
    return mc, contours

def rawmassVGT(rawmc, maskmc):
    diffmc = []
    for i in range(len(maskmc)):

        xdiff = (abs(rawmc[i][0] - maskmc[i][0]))
        ydiff = (abs(rawmc[i][1] - maskmc[i][1]))
        diffmc.append((xdiff,ydiff))

    print("X Y mass center difference (px) = {}".format(diffmc))
    return diffmc

def rawcontourVGT(rawcontours, gtcontours):
    diff = []
    for i in range(len(gtcontours)):

        diff.append(abs(cv.contourArea(rawcontours[i]) - cv.contourArea(gtcontours[i])))

    print("X Y area difference (px) = {}".format(diff))
    return diff



parser = argparse.ArgumentParser(description='Code for Image Moments tutorial.')
parser.add_argument('--raw', help='Path to input raw image.', default='raw.jpeg')
parser.add_argument('--mask', help='Path to input mask image.', default='mask.png')
args = parser.parse_args()
originalim = cv.imread(cv.samples.findFile(args.raw))
maskim = cv.imread(cv.samples.findFile(args.mask))


if originalim is None:
    print('Could not open or find the image:', args.raw)
    exit(0)
    
if maskim is None:
    print('Could not open or find the mask:', args.mask)
    exit(0)

source_window = 'Source'
cv.namedWindow(source_window)
cv.imshow(source_window, originalim)


rawmc, rawcontour = find_tissue(originalim, args.raw)
maskmc, gtcontour = find_tissue(maskim, args.mask)
diff = rawcontourVGT(rawcontour, gtcontour)
diffmc = rawmassVGT(rawmc, maskmc)

cv.waitKey()
