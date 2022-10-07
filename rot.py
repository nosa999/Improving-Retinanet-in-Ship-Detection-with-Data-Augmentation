from __future__ import division   # for python-2.x compatibility
from matplotlib import cm
import cv2
import numpy as np 
import csv
from PIL import Image
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import math

from decimal import Decimal
import os



# k=0## shomarandeii k dar hengame khundane fileha estefade kardim k dar nahayat baraye namgozari akshaye jadid estefade kardim
# x=os.listdir('shiptxt')## khundane filehaye mojud dar folder annotation marbut b ship
# x=sorted(x)## moratab kardane filehaye annotation 
# t=os.listdir('ship')## khundane filehaye mojud dar folder marbut b akshaye ship
# t=sorted(t)## moratab kardane fileha


def myRot(aabb,image):

	
	flagd=0
	j=0
	i=0
	sum1=0
	result = np.zeros((5, 5))
	degf = []
	scalef = []
	area_obj = 0
	area_temp = 0
	img = image

	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	
	template1 = cv2.imread('keras_retinanet/utils/t5.jpg',0)
	# print(type(template1))
	a11, b11, a21, b21 = aabb
	a1 = int(a11)
	b1 = int(b11)
	a2 = int(a21)
	b2 = int(b21)
	width1, height1 = template1.shape[::-1]
	#area_obj = (b2 - b1) * (a2 - a1)
	#area_temp = height * width
	#scale = float (area_obj) / area_temp	
	
###################################3	37+60+6+8=111
	locationd = []
	# print(scale)
	# scale_percent = scale*100
	# x= float (scale_percent)/100

	# width = int(template1.shape[1] * x)
	# height = int(template1.shape[0] * x)
	
	dy=b2-b1
	dx=a2-a1	
	# if dy < dx:
	# 	dim = (dy,dx)
	# else:
	# 	dim = (dx,dy)
	dim = (dx,dy)

	
	
	# print(type(template1))
	# cv2.imshow('tem',template1)


	for deg in range (0,360,1):
		#cv2.waitKey(0)
		
		center =(float(width1-1)/2.0, float(height1-1)/2.0)	

		rotation_matrix = cv2.getRotationMatrix2D(center,deg, 1)
		# print(rotation_matrix)
		abs_cos = abs(rotation_matrix[0,0]) 
		abs_sin = abs(rotation_matrix[0,1])

	

		# find the new width and height bounds
		bound_w = int(height1 * abs_sin + width1 * abs_cos)
		bound_h = int(height1 * abs_cos + width1 * abs_sin)
		# subtract old image center (bringing image back to origo) and adding the new image center coordinates
		rotation_matrix[0, 2] += bound_w/2 - center[0]
		rotation_matrix[1, 2] += bound_h/2 - center[1]
		# bound_w = width1
		# bound_h = height1
		

		img111 = cv2.warpAffine(template1, rotation_matrix,(bound_w,bound_h),borderMode=cv2.BORDER_REPLICATE)
		# cv2.imshow('rot',img111)

		resized = cv2.resize(img111, dim, interpolation = cv2.INTER_AREA)
		# width1, height1 = resized.shape[::-1]
		# cv2.imshow('resize',resized)

		
		# cv2.waitKey(0)
		# print(img111.shape)
		# width, height = img111.shape[::-1]

		# print(dy,height1,dx,width1,width,height)
	
		
		result = cv2.matchTemplate(gray_img[b1:b2, a1:a2], resized, cv2.TM_CCOEFF_NORMED)
		# print(result.shape)
		# print(result,deg)
		# raw_input("Press Enter to continue...")

		locationd.append(result)

		# locationd.append(np.where(result>=0.7))
		
	max_ind = 0
	max_ = 0
	index_ = 0
	
	for de in locationd:

		if de >= max_:
			max_ = de
			max_ind = index_
		index_ += 1
	locations = []
	for scale in range(15,20):
		scale_percent = scale*10
		width = int(template1.shape[1] * scale_percent / 100)
		height = int(template1.shape[0] * scale_percent / 100)
		dim1 = (width, height)
		resized = cv2.resize(template1, dim1, interpolation = cv2.INTER_AREA)
		width,height = resized.shape[::-1]
		center =(float(width-1)/2.0, float(height-1)/2.0)
		rotation_matrix = cv2.getRotationMatrix2D(center,max_ind, 1)
		abs_cos = abs(rotation_matrix[0,0]) 
		abs_sin = abs(rotation_matrix[0,1])

		# find the new width and height bounds
		bound_w = int(height * abs_sin + width * abs_cos)
		bound_h = int(height * abs_cos + width * abs_sin)
		# subtract old image center (bringing image back to origo) and adding the new image center coordinates
		rotation_matrix[0, 2] += bound_w/2 - center[0]
		rotation_matrix[1, 2] += bound_h/2 - center[1]
		img1 = cv2.warpAffine(resized, rotation_matrix,(bound_w,bound_h),borderMode=cv2.BORDER_REPLICATE)
		resized = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)
		result = cv2.matchTemplate(gray_img[b1:b2, a1:a2], resized, cv2.TM_CCOEFF_NORMED)
		locations.append(result)
	max_inds = 0
	max_s = 0
	index_s = 0
	# print(locations)
	for se in locations:
		# print(se)
		# raw_input("")
		if se >= max_s:
			max_s = se
			max_inds = index_s
		index_s += 1
	
	finScale = (max_inds+15)*10
	#print(finScale,max_s)
	width1 = int(template1.shape[1] * finScale / 100)
	height1 = int(template1.shape[0] * finScale / 100)

	box_center = (int((a2 + a1)/2),int((b2 + b1)/2))
	
	# exit()



	w_box = width1
	h_box = height1
	# p1 = ((box_center[0] - (w_box/2)) ,(box_center[1] - (h_box/2)))
	p1 = box_center

	# p1=(a1,b1)
	deg = -max_ind 
	# deg = 0
	# teta = (deg*np.pi)/180

	dim1 = (w_box,h_box)
	# print(dim1)

	rect = p1,dim1,deg
	box = cv2.boxPoints(rect)
	box = np.int0(box)



	o1 = (box[0][0],box[0][1])
	o2 = (box[1][0],box[1][1])
	o3 = (box[2][0],box[2][1])
	o4 = (box[3][0],box[3][1])

	return o1,o2,o3,o4
	# return box,deg



# def myDraw(lenZ, eachRec, image,name, finaldeg):
	# im = image
	# ind = 0
	# for each in eachRec:
		# o1 = (each[0][0],each[0][1]-10)
		# # print('each0000000000000',each[0])
		# # print(o1)

		# deg = repr(-finaldeg[ind])
		# # print(deg)

		# image = cv2.drawContours(image,[each],0,(0,0,255),2)
		# font = cv2.FONT_HERSHEY_SIMPLEX
		# cv2.putText(image,deg,o1, font, 1,(255,255,255),2,cv2.LINE_AA)
		# ind += 1

	# cv2.imwrite('new/'+name,image)
	

# for file in x:
		
	# k=k+1;
	
	# if k==26:
		# break;
	# else:
		# f = open('shiptxt/' + file, "r")
		
		# reader = csv.reader(f, delimiter=',', quotechar=' ',quoting = csv.QUOTE_NONE)	
		# finaldeg = []

		# i = 0
		# eachRec = []
		# for row in reader:
			# lista = []
			# i += 1
			
			# if len(row)==5:
				# for item in row:
					# item = item.replace('(', '')
					# item = item.replace(')', '')
					# lista.append(item)
				
				# top_bot = int(lista[0]),int(lista[1]),int(lista[2]),int(lista[3])
				
				# eachRec1 = []
				# for j in range(0,4):
					# eachRec1.append(top_bot[j])
				# # print(eachRec1)
				# image = cv2.imread('ship/' + t[k-1])
				# name=(t[k-1]+'.png');
				# myEachRec = myRot(eachRec1,image,name)
			
				# eachRec.append(myEachRec[0])
				# # print(eachRec)
				# # print(len(eachRec[0]))
				# finaldeg.append(myEachRec[1])
				# lenZ = i
			
		# image = cv2.imread('ship/' + t[k-1])
		
		# myDraw(lenZ,eachRec,image,name,finaldeg)
		# # exit()
