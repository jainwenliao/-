'''利用数据增强训练CNN'''

from keras import layers
from keras import models
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator

def training_way(train_path): 

    '''借鉴猫狗大战，设置的四层卷积、四层池化'''
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3,3), activation = 'relu', input_shape = (150, 150,3)))
    model.add(layers.MaxPooling2D((2,2)))
    model.add(layers.Conv2D(64,(3,3), activation = 'relu'))
    model.add(layers.MaxPooling2D(2,2))
    model.add(layers.Conv2D(128,(3,3), activation = 'relu'))
    model.add(layers.MaxPooling2D(2,2))
    model.add(layers.Conv2D(128,(3,3), activation = 'relu'))
    model.add(layers.MaxPooling2D(2,2))

    model.add(layers.Flatten())#将三维展平

    model.add(layers.Dropout(0.5))#用于降低过拟合

    model.add(layers.Dense(512,activation='relu'))
    model.add(layers.Dense(1,activation = 'sigmoid')) 

    #把人脸识别看成分类问题，这里用二分类
    model.compile(loss='binary_crossentropy',
    optimizer = optimizers.RMSprop(lr = 1e-4),
    metrics = ['acc'])

    #图片处理，数据增强处理
    train_datagen = ImageDataGenerator(
        rescale = 1. / 255,
        rotation_range = 40, #图片随机旋转的角度范围
        width_shift_range = 0.2, #图片在水平上平移
        height_shift_range = 0.2, #在垂直方向上的平移
        shear_range = 0.2, #随机错切变换  
        zoom_range = 0.2, #随机缩放的范围
        horizontal_flip = True, #随机将一半图像翻转
    )

    #验证集不需要增强，不然就没有真实性了
    #validation_datagen = ImageDataGenerator(rescale = 1. / 255)

    train_generator = train_datagen.flow_from_directory(
        train_path,
        target_size = (150,150),
        batch_size = 20,
        class_mode = 'binary'
    )
    '''
    先不使用验证集
    validation_generator = validation_datagen.flow_from_directory(
        validation_path,
        target_size = (150,150),
        batch_size= 20,
        class_mode = 'binary'
    )
    '''
    #print(train_generator.class_indices) 确认标签对于的分类
    #print(train_generator.filenames) 给出所有图片和对于的类别

    history = model.fit(
        train_generator,
        steps_per_epoch = 50,
        epochs = 10
        #validation_data = validation_generator,
        #validation_steps = 1
    )

    model.save('face_training_1.h5')
