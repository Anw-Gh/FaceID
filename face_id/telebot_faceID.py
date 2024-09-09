import telebot # telebot

from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup #States

# States storage
from telebot.storage import StateMemoryStorage

import csv
import os


from train import train
from split_video import split
from test_recognizer import test_photo
# import recognizer





state_storage = StateMemoryStorage()
bot = telebot.TeleBot("",
state_storage=state_storage)


#use this class to save states in every step (when need to)l.
class MyStates(StatesGroup):
    
    reg = State()
    admin = State()

    first_name = State()
    last_name = State()
    full_name = State()
    id_num = State()
    
    get_video = State()
    get_photo = State()
    
    train = State()

admin = 'admin_username'
admin_id = #put admin_id as int




@bot.message_handler(commands=['start'])
def start_message(message):
    

    bot.set_state(message.from_user.id, MyStates.reg, message.chat.id)
    bot.send_message(message.chat.id,
                     
f'''Welcome,i'm a FaceID bot you can sign as admin or emplowee..
i designed to help registering you, or have control with the company's database.
You must be provided with the company password.
if you do not have the password, contact the technical support department @{admin}

avilible commands:
    /register_ : for register as new employee.
    /admin_ : get information and data.
    /test : will show you if you are in company's database or not..'
    /cancel : cancel everything.
    
    NOTE: you shoud add the password after ( _ )

'''
)
#actived registering, now i can be admin or employee, or test my bot






@bot.message_handler(state=MyStates.reg, commands = ['test'])
def test_data(message):
    bot.send_message(message.chat.id, "ok, send me a photo.")
    bot.set_state(message.from_user.id, MyStates.get_photo, message.chat.id)
    #startting get_photo.




@bot.message_handler(state=MyStates.get_photo, content_types=['photo'])
def test_pic(message):
    print('i got a photo..')
    bot.send_message(message.chat.id, "wait please..\nif you did not get any response,\nthat mean your photo does not have any faces\n if you think there is a mistake, please contact with IT supporter.")
    
    fileID = message.photo[-1].file_id #take only one photo
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    print('i downloaded it..')
    
    
    with open('cash_telephoto/temp.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)
        
        #call test_photo() from test_recognizer.py
        name = test_photo('cash_telephoto/temp.jpg')
        
        print('name is:', name)
     
        
        if name == 'empty':
            bot.send_message(message.chat.id,"Don't try to fool me, there is no face in this picture, or your face is so blurred that even people can't see it, \thaha..😆")
        
        elif name=='unknown':
            bot.send_message(message.chat.id,"i don't know who you are, if you think your pics in database, send another photo showing your face clearly..")
            bot.send_photo(message.chat.id, photo=open('cash_telephoto/img_saved.jpg', 'rb'))
            print('photo is sent.')
            
        else:
            
            print('sending photo..')
            bot.send_message(message.chat.id,f"hello, you are {name}\ni will send you a photo, please wait...")
            bot.send_photo(message.chat.id, photo=open('cash_telephoto/img_saved.jpg', 'rb'))
            print('photo is sent.')
            




#admin
@bot.message_handler(state=MyStates.reg, commands = ['admin_a555'])
def is_admin(message):
   
    
    bot.send_message(message.chat.id,
                     
'''Welcome adimn, you can do a sevral things as an admin:
    
/get_details : will send you the attendance_sheet.
/get_names : will send you the employees names.
/get_unknown : will send you pictures of unknown people

'''
)

    bot.set_state(message.from_user.id, MyStates.admin, message.chat.id)
   
#activated admin: can do: get data, get photo of unknwon, get names.
    






@bot.message_handler(state=MyStates.admin, commands = ['get_details'])
def get_details(message):
     
        
    with open('attendance_sheet.csv', 'r') as source:
        details=''
        
        for row_number, row in enumerate(source.readlines()):
            if row_number == 0:
                continue
            else:
                data = row.split(';')
                result1 = data[0]
                result2 = data[1]
                result3 = data[2]   
                details =details+f'''name\t\t|\t\tdata\t\t\t|\t\ttime
{result1}\t\t|\t\t{result2}\t\t|\t\t{result3}
----------------------------
'''
        bot.send_message(message.chat.id , str(details))
        # print(details)
        
   
    
   
@bot.message_handler(state=MyStates.admin, commands = ['get_names'])
def get_names(message):
    dir_path = 'train_dir'

    names=''

    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isdir(os.path.join(dir_path, path)):
            names=names+'\n-'+path
    bot.send_message(message.chat.id ,names)






@bot.message_handler(state=MyStates.admin, commands = ['get_unknown'])
def get_unknown(message):
    dir_path = 'unknown_people'
    unknown=[]
    for x in os.listdir('unknown_people'):
        if x.endswith(".jpg"):
            unknown.append(x)
    if not unknown:
        bot.send_message(message.chat.id ,'empty at the momment...')
    for i in range(0, len(unknown)):
        bot.send_photo(message.chat.id, photo=open(f'{dir_path}/'+unknown[i], 'rb'))













#register
@bot.message_handler(state=MyStates.reg , commands = ['register_r555'])
def get_first_name(message):
    
    bot.set_state(message.from_user.id, MyStates.first_name, message.chat.id)
    bot.send_message(message.chat.id, 'Hi, write me your first name:')
    






@bot.message_handler(state=MyStates.first_name)
def get_last_name(message):
    
    bot.send_message(message.chat.id, 'Now write me your last name:')
    bot.set_state(message.from_user.id, MyStates.last_name, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['first_name'] = message.text





@bot.message_handler(state=MyStates.last_name)
def get_full_name(message):
    
    bot.set_state(message.from_user.id, MyStates.id_num, message.chat.id)
    bot.send_message(message.chat.id, "What is your ID?")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['last_name'] = message.text





#get full info..

photo_path=[]
@bot.message_handler(state=MyStates.id_num, is_digit=True)
def ready_for_answer(message):
    
    
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        msg = ("Ready, take a look:\n<b>"
               f"first name: {data['first_name']}\n"
               f"last name: {data['last_name']}\n"
               f"ID: {message.text}</b>")
        
        
        bot.send_message(message.chat.id, msg, parse_mode="html")
        # Directory 
        directory = f'{data["first_name"]} {data["last_name"]}_{message.text}'
        
        photo_path.append(directory)
        # Parent Directory path 
        
        parent_dir = "train_dir"
            
        # Path 
        path = os.path.join(parent_dir, directory) 
            

        os.makedirs(path) 
        print("Directory '% s' created" % directory) 
        print(f'the photo folder is: {photo_path[0]}')
        
        
        
    bot.delete_state(message.from_user.id, message.chat.id)
    
    bot.send_animation(message.chat.id, 'https://cdn.dribbble.com/users/3258568/screenshots/6815101/face.gif')
  
    bot.send_message(message.chat.id,
'''Now, Please send a video, not exceeding 10 seconds.
showing your front face clearly with good lighting.
and move your face slowly as in the (GIF) sent...''')


    bot.set_state(message.from_user.id, MyStates.get_video, message.chat.id)

#waiting for video.





#incorrect id
@bot.message_handler(state=MyStates.id_num, is_digit=False)
def id_incorrect(message):

    bot.send_message(message.chat.id, 'Looks like you are submitting a string in the field ID. Please enter a number')







@bot.message_handler(state=MyStates.get_video ,content_types=['video'])
def video_splitting(message):
    
    print('im in video func')
    
    fileID = message.video.file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
  
    print('i got video.mp4')
    print(f'the photo folder is: {photo_path[0]}')
    
    with open('cash_vid/user_video.mp4', 'wb') as new_file:
        new_file.write(downloaded_file)
        print('i downloaded it..')
        
        split(f'train_dir/{photo_path[0]}','cash_vid/user_video.mp4')
    
    bot.set_state(message.from_user.id, MyStates.train, message.chat.id)
    
    bot.send_message(message.chat.id,
                     
'''your video received.
please send /train command, so your data will be stored in company's database.''')
    




@bot.message_handler(state=MyStates.train ,commands=['train'])
def train_data(message):
    
    train('train_dir' , 'trained_data') # call train func.
    bot.send_message(message.chat.id,'Training done.')
    





# Any state
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message):
    """
    Cancel state
    """
    bot.send_message(message.chat.id, "Your state has been cancelled.")
    bot.delete_state(message.from_user.id, message.chat.id)
    print('user cancel everything..') 






bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

bot.infinity_polling(skip_pending=True)