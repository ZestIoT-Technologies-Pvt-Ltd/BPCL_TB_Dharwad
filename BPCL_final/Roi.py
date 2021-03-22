'''
#   Copyright (C) 2020 by ZestIOT. All rights reserved. The
#   information in this document is the property of ZestIOT. Except
#   as specifically authorized in writing by ZestIOT, the receiver
#   of this document shall keep the information contained herein
#   confidential and shall protect the same in whole or in part from
#   disclosure and dissemination to third parties. Disclosure and
#   disseminations to the receiver's employees shall only be made on
#   a strict need to know basis.

Input: Coordinates and Scores of 5 Persons 
Output: Coordinates and Scores of Persons who are in ROI
Requirements:
This function shall perform the following:
1)For each person it will identify the presence of any one of the below key points in ROI
  keypoints are left knee,left ankle, Right ankle, Right knee
2)A new list of identified person coordinates and scores in ROI is returned
'''    
    
import cv2
import numpy as np
import math
'''
Requiremnets: This variable shall be initialised with a 3*3 matrix with below values 
[[ 1.77928445e+00,  5.69877582e-01,-9.82152353e+02],
 [-5.80034886e-16,  3.59466115e+00, -9.20233254e+02],
 [ 1.99095433e-04,  2.69942866e-03,  1.00000000e+00]]
'''
'''ch_matrix_2mp = np.array([[ 3.46959178e+00,  1.13138862e+00, -1.67618996e+03],
 [ 3.25571048e+00,  2.00140518e+01, -1.00066832e+04],
 [ 2.22885334e-03,  4.97684693e-03,  1.00000000e+00]]) #for raipur'''

#ch_matrix_2mp = np.array([[ 1.45107517e+00, 4.16576604e-01, -6.29475021e+02],
 #[-1.84463740e-01,  4.05110752e+00, -1.03218105e+03],
 #[ 5.24845526e-04,  2.06045617e-03,  1.00000000e+00]])#for sholapur
'''ch_matrix_2mp = np.array([[ 2.73653922e+00,  3.80074891e-01, -1.51186190e+03],
 [ 4.62705522e-01,  4.94364321e+00, -1.78287744e+03],
 [ 6.53350994e-04,  4.15877829e-03,  1.00000000e+00]])#for sholapur'''
'''ch_matrix_2mp = np.array([[ 8.70803538e-01,  1.23744125e-17, -3.04781238e+02],
 [ 1.98966981e-01, -2.77132580e+00,  1.27168324e+03],
 [ 1.37896905e-04,  2.74936441e-04,  1.00000000e+00]])#for Balangir'''
ch_matrix_2mp = np.array([[ 9.48802013e-01,  5.16084777e-02, -3.58075498e+02],
 [-4.27611043e-02,  2.07818967e+00, -7.64055412e+02],
 [ 2.62584437e-06,  3.94470315e-04,  1.00000000e+00]]) #for Dharwad

'''ch_matrix_2mp = np.array([[ 8.51136905e-01,  2.55722747e-01, -2.78077495e+02],
[-1.61991150e-01,  2.23907767e+00, -5.23587794e+02],
[ 2.37583968e-04,  4.87797615e-04,  1.00000000e+00]])#for durgapur1'''
def roi_fun(coordinates,scores):
    view_coords = []
    view_scores = []
    number_roi = 0
    for person in range(0,5):
        if abs(coordinates[person][5][1] - coordinates[person][6][1]) < 30 and abs(coordinates[person][5][0] - coordinates[person][7][0]) < 30 :
            continue
        list_roi=[]
        for body_point in [5,6,7,8,9,10,13,14,15,16]:
            landmark_coords=[0,0]
            if round(scores[person][body_point],1) >= 0.1:
                landmark_coords[0]=round(coordinates[person][body_point][0],1)
                landmark_coords[1]=round(coordinates[person][body_point][1],1)
            else:
                landmark_coords[0] = -1
                landmark_coords[1] = -1
            list_roi.append(landmark_coords)

        for i in range(9,-1,-1):
            x_coordinate = list_roi[i][1]
            y_coordinate = list_roi[i][0]
            a1 = np.array([[x_coordinate,y_coordinate]],dtype='float32')
              #print("a1--->",a1)
            a1 = np.array([a1])
            output1 = cv2.perspectiveTransform(a1,ch_matrix_2mp)
            if((output1[0][0][0] >= 0.0 and output1[0][0][0] <=400) and (output1[0][0][1] >= 0.0 and output1[0][0][1] <=400)):
                view_coords.append(coordinates[person])
                view_scores.append(scores[person])
                number_roi = number_roi+1
                break
                   
    return view_coords,view_scores,number_roi

