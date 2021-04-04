import sys
import os
import cv2

def others_database(input_dir, train_others_dir, train_pic_num):
    #检测输出地址是否存在，如果不存在就创建一个
    if not os.path.exists(train_others_dir):
        os.makedirs(train_others_dir)
    classfier_path = 'E:\\Opencv\\haarcascades_cuda\\haarcascade_frontalface_alt_tree.xml'  #人脸分类器算法所在的目录

    #人脸分类器
    classfier = cv2.CascadeClassifier(classfier_path)
    size = 64 #图片的尺寸
    index = 0

    imgs = os.listdir(input_dir)#获取路径下的所有文件

    for img in imgs:
        if img.endswith('.jpg'):
            print('Being processed picture %s' % index)
            img_path = input_dir + '/' + img

            image_name = img
            #读取路径下的所有图片
            img = cv2.imread(img_path)
            #将图片灰度化
            gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      
            # 人脸检测，调整图片的尺寸
            faceRects = classfier.detectMultiScale(img, scaleFactor = 1.2, minNeighbors = 3, minSize = (64, 64))
            if len(faceRects) > 0:            #大于0则检测到人脸                                   
                for faceRect in faceRects:    #单独框出每一张人脸
                    x, y, w, h = faceRect  
                    #cv2.imshow('image',img)
                    #将当前帧保存为图像 
                    if index < train_pic_num:
                        faces_path = '%s%s.jpg'%(train_others_dir,index)           
                        image = gray[y - 10: y + h + 10, x - 10: x + w + 10]
                        image = cv2.resize(image,(size,size))
                        cv2.imwrite(faces_path, image)
                
                    index += 1

            if index == train_pic_num:
                break

    cv2.destroyAllWindows()

'''
if __name__ == '__main__':
    others_database(
        'E:\\Deep learning\\others_faces',
        'E:\\face_recognization_projects\\face_recognition3\\train\\others\\',
        'E:\\face_recognization_projects\\face_recognition3\\validation\\others\\',
        1000, 
        100
    )
'''