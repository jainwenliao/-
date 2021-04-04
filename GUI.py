# coding:utf-8
import tkinter as tk 
from tkinter import messagebox
import pickle
import os, cv2
from catch_my_faces import get_faces
from set_others import  others_database
from train_function import training_way
from recognize_me import face_validation



#先创建一个窗口
window = tk.Tk()

#给窗口一个可视化的名字
window.title('人脸识别')

#设置窗口的大小
window.geometry('400x300')

#加载image
canvas = tk.Canvas(window, width = 400, height = 135, bg = 'blue') #画布功能
image_file = tk.PhotoImage(file = 'E:\\face_recognization_projects\\face_recognition3\\1.gif')
image = canvas.create_image(200, 0, anchor = 'n', image = image_file)

canvas.pack(side = 'top')
tk.Label(window,text ='Wellcome', font = ('Arial', 14)).pack()

#用户信息
tk.Label(window, text = 'User name:', font = ('Arial', 14)).place(x = 10, y = 170)
tk.Label(window, text = 'Password:', font = ('Arial', 14)).place(x = 10, y = 210)

#用户输入框entry
#用户名
var_usr_name = tk.StringVar()
entry_usr_name = tk.Entry(window,textvariable = var_usr_name, font = ('Arial', 14))
entry_usr_name.place(x=120, y = 175)

#用户密码
var_usr_pwd= tk.StringVar()
entry_usr_pwd = tk.Entry(window,textvariable = var_usr_pwd, font = ('Arial', 14),show = '*')
entry_usr_pwd.place(x=120, y = 215)

#定义用户登录功能
def usr_login():  
    #获取用户输入的账户和密码
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()

    #判断是否存在账户
    try:
        with open('usrs_info.pickle', 'rb') as usr_file:  
            usrs_info = pickle.load(usr_file)

    except FileNotFoundError:  
        with open('usrs_info.pickle','wb') as usr_file:  
            usrs_info = {'admin':'admin'}
            pickle.dump(usrs_info,usr_file)

            usr_file.close

    #如果用户名和密码和文件中的匹配，则显示登录成功

    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:  
            tk.messagebox.showinfo(title = 'Wellcome',message = 'HOW are you?' + usr_name)

        else:
            tk.messagebox.showerror(message = 'Error, your password is wrong, try again.')

    else: 
        is_sign_up = tk.messagebox.askyesno('Welcome！ ', 'You have not sign up yet. Sign up now?')

        if is_sign_up:  
            usr_sign_up()

def face_login():
    face_id = face_validation()
    
    if face_id == 0: 
        tk.messagebox.showinfo(title = 'Wellcome',message = 'HOW are you?' )    

    else: 
        tk.messagebox.showerror(message = 'Error, Please try again.')
        face_validation()
    
def usr_sign_up():  
    
    def sign_up():  
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        nn = new_name.get()
        with open('usrs_info.pickle','rb') as usr_file:  
            exist_usr_info = pickle.load(usr_file)

        if np != npf: 
            tk.messagebox.showerror('Error', 'Password and confirm must be the same')

        elif nn in exist_usr_info.keys(): 
            tk.messagebox.showerror('Error', 'The user has already signed up!')

        else: 
            exist_usr_info[nn] = np
            with open ('usrs_info.pickle','wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)

            is_face_sign_up = tk.messagebox.showinfo('Wellcome','You have successfully signed up.')


        window_sign_up.destroy()

    def face_sign_up():
        with open('usrs_info.pickle','rb') as usr_file:  
            exist_usr_info = pickle.load(usr_file)
            nn_names = list(exist_usr_info.keys())
            nn_name = nn_names[-1]

        others_path = 'E:\\Deep learning\\others_faces'
        my_face_path = 'E:\\face_recognization_projects\\face_recognition3\\database\\'+ nn_name+ '\\me'
        others_face_path = 'E:\\face_recognization_projects\\face_recognition3\\database\\'+ nn_name + '\\others\\'
        training_path = 'E:\\face_recognization_projects\\face_recognition3\\database\\'+ nn_name
        if not os.path.exists(my_face_path ):
            os.makedirs(my_face_path)
        if not os.path.exists(others_face_path):
            os.makedirs(others_face_path)

        get_faces('catch_face', 0, 100, my_face_path)
        others_database(others_path, others_face_path,1000)
        training_way(training_path)


        
        

        

    # 定义长在窗口上的窗口
    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('300x200')
    window_sign_up.title('Sign up window')

    new_name = tk.StringVar()  # 将输入的注册名赋值给变量
        
    #new_name.set('input your  name') 
    tk.Label(window_sign_up, text='User name: ').place(x=10, y=10)  # 将`User name:`放置在坐标（10,10）。
    entry_new_name = tk.Entry(window_sign_up, textvariable= new_name )  # 创建一个注册名的`entry`，变量为`new_name`
    entry_new_name.place(x=130, y=10)  # `entry`放置在坐标（150,10）.
    
    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='Password: ').place(x=10, y=50)
    entry_usr_pwd = tk.Entry(window_sign_up, textvariable = new_pwd, show='*')
    entry_usr_pwd.place(x=130, y=50)
    
    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='Confirm password: ').place(x=10, y=90)
    entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_usr_pwd_confirm.place(x=130, y=90)

    btn_comfirm_sign_up = tk.Button(window_sign_up, text='Sign up', command = sign_up)
    btn_comfirm_sign_up.place(x=90, y=120)
    btn_face_sign_up = tk.Button(window_sign_up, text = 'face_sign_up', command = face_sign_up)
    btn_face_sign_up.place(x = 180, y=120)

        
    
       
 
# 第7步，login and sign up 按钮
btn_login = tk.Button(window, text='Login', command=usr_login)
btn_login.place(x=120, y=250)
btn_face_login = tk.Button(window, text = 'face_login', command = face_login)
btn_face_login.place(x = 185, y =250)
btn_sign_up = tk.Button(window, text='Sign up', command=usr_sign_up)
btn_sign_up.place(x=280, y=250)



#窗口循环显示
window.mainloop()