import json
import os
from helper import *
# from tensorflow.keras.models import model_from_json
from subprocess import call
# from IPython.display import display, clear_output
# from PIL import Image
# import seaborn as sn
# import pandas as pd
import random

# model_name = './moving_around/stable'

# json_file = open(model_name+'.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()

# loaded_model = model_from_json(loaded_model_json)

# loaded_model.load_weights(model_name+".h5")


# cam = cv2.VideoCapture(0)

imgs = list(filter(lambda x: x.split('.')[1] == 'jpg',os.listdir('./imgs')))
imgs.sort()



def test_model(roix=(250,250),roiy=(150,80),eye_size=1):
    roi_offset = [roix[0],roiy[0]]

    while True:
        _,frame = cam.read()
        frame = cv2.flip(frame,1)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        roi = gray[roi_offset[1]:roi_offset[1]+roiy[1], roi_offset[0]:roi_offset[0]+roix[1]]
        eye,_ = find_eye(roi, scale_sizes=(70,101,10))

        cv2.imshow('frame',roi)
        if eye['maxmatch'] > 0.87:

            h,w = eye['img'].shape[:2]

            cv2.imshow('eye',cv2.resize(eye['img'],(int(w*eye_size),int(h*eye_size))))
            print('match:',eye['maxmatch'], ', scale:',eye['scale'])
        else:
            # print('no strong match')
            pass
        k = cv2.waitKey(2)
        if k == 27:
            break

    cam.release()
    cv2.destroyAllWindows()
    return



# for imgpath in imgs[:1]:
#     # if imgpath.split('.')[1] != 'jpg': continue
#     # print(imgpath)
#     eye,pupil = find_eye(imgpath)
#     cv2.imshow('eye',eye)
#     cv2.imshow('pupil',pupil)


# while True:
#     _,frame = cam.read()
#     frame = cv2.flip(frame,1)
#     gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

#     roi_offset = [300,150]
#     roi = gray[roi_offset[1]:roi_offset[1]+80, roi_offset[0]:roi_offset[0]+250]
#     eye,pupil = find_eye(roi)

#     cv2.imshow('eye',eye['img'])
#     eh,ew = eye['img'].shape[:2]
#     if pupil is not None:
#         cv2.imshow('pupil',pupil['img'])

#         oex,oey = eye['top_left']
#         opx, opy = pupil['top_left']

#         pw,ph = pupil['width'], pupil['height']
#         cv2.circle(frame,(int(roi_offset[0] + oex + ew/2),int(roi_offset[1] + oey + eh/2)),1,(0,0,255),1)
#         cv2.circle(frame, (int(roi_offset[0]+oex+opx+pw/2),int(roi_offset[1]+oey+opy+ph/2)),1, (255,0,0), 1)
    
#     cv2.rectangle(frame,(roi_offset[0],roi_offset[1]),(roi_offset[0]+250,roi_offset[1]+80),(0,255,0),1)
#     cv2.imshow('frame',frame)

#     k = cv2.waitKey(2)
#     if k == 27:
#         break
#     # if k == 32:
#     #     find_eye(roi)

# cam.release()

print('Looking through',len(imgs),'images...')
# input()
# i = np.random.randint(0,len(imgs))
i = 0
bad_count = 0

img_offset = [270,150]

ind = [int(random.random()*len(imgs)) for _ in range(100)]
print(ind)
# imgs = np.array(imgs)
rightmost = 0
for img in imgs:
    # if img != '3_2_77.jpg': continue
    print('Image #'+str(i),'-->',imgs[i])
    i+=1
    # print(img)
    roi = cv2.imread('./imgs/'+img)
    roi = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    roi = roi[0:100,0:250]
    # cv2.imshow('roi',roi)
    eye,_ = find_eye(roi,find_pupil=False, scale_sizes=(85,116,15))
    # print(eye['maxmatch'])
    if eye['maxmatch'] > 0.87:
        # cv2.imshow(img,eye['img'])
        # print('img'+str(i%50),eye['top_left'])
        rightmost = max(rightmost, eye['top_left'][0])
        tl = [eye['top_left'][0] + img_offset[0], eye['top_left'][1] + img_offset[1]]
        cv2.imwrite('./train/'+img.split('.')[0]+'_'+str(tl)+'.jpg', eye['img'])
    else:
        bad_count+=1
        print(bad_count)
        # input()
    # cv2.waitKey(0)

print('rightmost:',rightmost)
print('bad coutn:',bad_count)
# cv2.destroyAllWindows()





# test_model(eye_size=5, roix=(250,250), roiy=(150,100))