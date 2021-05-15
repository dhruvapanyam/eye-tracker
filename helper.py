import cv2
import numpy as np
import os

TEMPLATE_PATHS = list(map(lambda img: './new_templates/'+img, os.listdir('./new_templates')))
TEMPLATES = [cv2.cvtColor(cv2.imread(tp), cv2.COLOR_BGR2GRAY) for tp in TEMPLATE_PATHS[:9]]

def get_pupil(image,template=None):
    if template is None: template = cv2.imread('black.png')
    template = cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)
    th,tw = template.shape[:2]

    # temp = cv2.resize(template,(int(tw*0.1),int(th*0.1)))

    m = 0
    match = None
    s = 0
    h,w = 0,0
    for SCALE in range(7,10):
        SCALE /= 100
        # cv2.imshow('temp',temp)
        try:
            # print((int(tw*SCALE),int(th*SCALE)))
            temp = cv2.resize(template,(int(tw*SCALE),int(th*SCALE)))
            tm = cv2.matchTemplate(image,temp,cv2.TM_CCOEFF_NORMED)
            am = np.amax(tm)
            if m > am: continue

            matched = np.where(tm == am)
            x0,y0 = matched[1][0],matched[0][0]
            s = SCALE
            match = [int(x0),int(y0)]            
            h = int(th*SCALE)
            w =  int(tw*SCALE)
        except:
            print('failed for scale:',SCALE)
            pass
    # print(match)
    if match is None: return None
    x,y = match    
    roi = cv2.resize(image[y:y+h,x:x+w], (int(w*5),int(h*5)))

    return {
        'img':roi,
        'top_left': [x,y],
        'width': w,
        'height': h
    }


def find_eye(img,write=False,find_pupil=False, scale_sizes=(50,100,5)):


    finscale = 1
    finmatch = [0,0]
    fw,fh = 0,0
    maxmatch = 0
    # chosen = None

    for template in TEMPLATES:
        # print(tp)
        # template = cv2.imread('./templates/'+tp)
        # template = cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)
        # # cv2.imshow(tp,template)
        th,tw = template.shape[:2]

        m = 0
        mscale = 1
        match = [0,0]
        w,h = 0,0
        for scale in range(scale_sizes[0], scale_sizes[1], scale_sizes[2]):
            scale /= 100
            temp = cv2.resize(template,(int(tw*scale),int(th*scale)))
            # if tp == 'top.jpg' and scale == 1.6:
            #     cv2.imshow(tp,temp)

            try:
                x = cv2.matchTemplate(img, temp, cv2.TM_CCOEFF_NORMED)
                am = np.amax(x)
                if(m > am): continue
                m = am
                mscale = scale
                matched = np.where(x == am)
                match = [matched[1][0],matched[0][0]]
                w = int(tw*scale)
                h = int(th*scale)
                # print(scale)
                if m > 0.87: 
                    # print(scale*100-scale_sizes[0])
                    break
                # print('success')
            except:
                pass
        
        if maxmatch > m: continue
        # print('updated match')
        maxmatch = m
        # chosen = tp
        finscale = mscale
        finmatch = match
        fw,fh = w,h

    # print('matched with:',chosen)
    # print('scale of match:',finscale)
    # print('match accuracy:',maxmatch)
    # print('dimensions:',fw,fh)
    x,y = int(finmatch[0]),int(finmatch[1])
    roi = img[y:y+int(fh), x:x+int(0.8*fw)]
    pupil = None
    if find_pupil: 
        pupil = get_pupil(roi)
    
    # cv2.imshow('roi',roi)

    # if write:
    #     f = open('./imgs/'+imgpath.split('.')[0]+'.json','w')
    #     data = {
    #         'topleft':[x,y],
    #         'width':int(fw),
    #         'height':int(fh),
    #         'template':chosen
    #     }
    #     j = json.dumps(data)

    #     f.write(j)
    #     f.close()
    #     cv2.imwrite('./processed/'+imgpath, roi)
    
    return ({
        'top_left': [x,y],
        'img': roi,
        'maxmatch': maxmatch,
        'scale': finscale
    }, pupil)


# for tp in ['topleft.jpg','top.jpg','topright.jpg','bottomleft.jpg','bottom.jpg','bottomright.jpg']:
#     img = cv2.imread('./templates/'+tp)
#     print(img.shape)

# img = cv2.imread('./imgs/0_0_1.jpg')
# cv2.imshow('img',img)
# i = 0
# for tp in TEMPLATES:
#     cv2.imshow('tp'+str(i),tp)
#     i+=1
# cv2.waitKey(0)
