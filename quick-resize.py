"""
Photo Manipulator

Date created: Aug 8 2016 00:16
Date modified: Jan 17 2019 17:06
Created by: Alex Naylor
Modified by: Alex Naylor
"""

#imports
from PIL import Image

import math
import os
import fnmatch
import platform

### USER VARIABLES ###
desResolution = 1920,1080   #Width,height (desired for final image)
keepResolution = False #Set to 'False' if you want to resize the image to the desired resolution
                       #Set to 'True' if you want to keep the new resolution
######################

desAspectRatio = float(desResolution[0])/desResolution[1]

OS = platform.system()
workDir = os.getcwd()
outputFileType = '.jpg'

if OS == 'Windows':
    slash = '\\'
elif OS == 'Linux':
    slash = '/'

saveDir = workDir + '{0}Photos{0}Updated{0}'.format(slash)

if not os.path.exists(saveDir):
    os.makedirs(saveDir)

files = [os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(workDir)
    for f in fnmatch.filter(files, '*.jpg')]

for filePath in files:
    photo = Image.open(filePath)
    
    currFileName = filePath.split(slash)[-1]
    newFileName = currFileName.rstrip('.jpg')+outputFileType
    newFilePath = saveDir+newFileName

    if os.path.exists(newFilePath): continue#Not working yet
   
    currWidth, currHeight = photo.size
    aspectRatio = float(currWidth)/currHeight

    frac = -1
    newHeight = float(currHeight)
    newWidth = float(currWidth)        

    #If the image is more than 16:9, the height is the limiting factor
    if aspectRatio > desAspectRatio:    
        print("{0} too tall for desired aspect ratio; adjusting height...".format(currFileName))
        while not frac == 0.0:
            frac, newWidth = math.modf(newHeight*desAspectRatio)
    
            newHeight -= 1
        
        print("Height reduced to {0}".format(newHeight))
    
    #If the image is less than 16:9, the width is the limiting factor
    elif aspectRatio < desAspectRatio:
        print("{0} too wide for desired aspect ratio; adjusting width...".format(currFileName))
        while not frac == 0.0:
            frac, newHeight = math.modf(newWidth/desAspectRatio)
    
            newWidth -= 1

        print("Width reduced to {0}".format(newWidth))

    #If the image needs further adjustments to reach the desired aspect ratio, crop as required
    if not aspectRatio == desAspectRatio:  
        print("Current aspect ratio does not match desired aspect ratio; cropping...")
        heightCrop = int(currHeight - newHeight)
        widthCrop = int(currWidth - newWidth)
        vertFrac, integer = math.modf(float(heightCrop)/2)
        horzFrac, integer = math.modf(float(widthCrop)/2)
            
        if (vertFrac == 0.0) and (horzFrac == 0.0):
            topCrop = int(heightCrop/2)
            bottomCrop = int(currHeight-heightCrop/2)
            leftCrop = int(widthCrop/2)
            rightCrop = int(currWidth-widthCrop/2)
        elif (vertFrac == 0.5) and (horzFrac == 0.0):
            topCrop = int(heightCrop/2+0.5)
            bottomCrop = int(currHeight-int(heightCrop/2-0.5))
            leftCrop = int(widthCrop/2)
            rightCrop = int(currWidth-widthCrop/2)  
        elif (vertFrac == 0.0) and (horzFrac == 0.5):
            topCrop = int(heightCrop/2)
            bottomCrop = int(currHeight-heightCrop/2)
            leftCrop = int(widthCrop/2+0.5)
            rightCrop = int(currWidth-int(widthCrop/2-0.5))     
        elif (vertFrac == 0.5) and (horzFrac == 0.5):
            topCrop = int(heightCrop/2+0.5)
            bottomCrop = int(currHeight-int(heightCrop/2-0.5))
            leftCrop = int(widthCrop/2+0.5)
            rightCrop = int(currWidth-int(widthCrop/2-0.5))

        photo.crop((leftCrop,topCrop,rightCrop,bottomCrop))

    if keepResolution == False:
        print("Resize image to desired resolution...")
        resolution = desResolution
    else:
        print("Keep new image resolution...")
        resolution = int(newWidth),int(newHeight)

    photo.resize((resolution),Image.BICUBIC).save(newFilePath)
    print("Photo saved in {0}\n\n".format(newFilePath))