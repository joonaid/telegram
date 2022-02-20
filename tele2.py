import telebot
from flask import Flask , request
import os
from telebot.types import InlineKeyboardMarkup , InlineKeyboardButton
from pprint import pprint
TOKEN ='5126798288:AAErHBKOZV7FvYP0cER2hXWUtcqO_IYMIZY'
server = Flask(__name__)
msg1 = 'يرجى كتابة معلوماتك الشخصية عزيزي الطالب: ( الاسم , العمر , اسم الدرس او الدروس اللتي تريد الاشتراك بها)'
msg2 = 'تفضل بكتابة استفسارك عزيزي الزائر..'
def markup_inline():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("التسجيل كطالب في المعهد", callback_data='Register') ,
         InlineKeyboardButton("ارسال استفسارك حول المعهد" , callback_data='feedback')
    )
    return markup

bot = telebot.TeleBot(TOKEN)
admin =5154442427
group_id = -660744649

@bot.callback_query_handler(func=lambda msg :True)
def call_back(call ):
    if call.data == 'Register':
        #bot.answer_callback_query(call.id , msg1)
        bot.send_message(call.message.chat.id , msg1)
    if call.data == 'feedback':
        bot.send_message(call.message.chat.id , msg2)
       # bot.answer_callback_query(call.id , msg2)



@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(msg.chat.id , f"اهلا بك عزيزي الزائر {msg.from_user.first_name} يرجى الضغظ على احد الخيارات في الاسفل من اجل الاستمرار.. " ,reply_markup= markup_inline())
@bot.message_handler(commands=["id"])
def start(msg):
    bot.send_message(msg.chat.id , msg.from_user.id)
@bot.message_handler(func=lambda msg: True , content_types=['text' , 'photo'])
def forward_msg(msg):
    #print(msg.from_user.id , admin )
    #if msg.from_user.id != admin:

      bot.forward_message(-660744649 , msg.chat.id , msg.message_id)
      bot.forward_message(admin, msg.chat.id, msg.message_id)
      bot.send_message(group_id , f"{msg.from_user.first_name}  user_id :  {msg.chat.id}-id")
      bot.send_message(msg.chat.id , 'لقد تم ارسال رسالتك بنجاح..! ')

      #re_call the func agaın



      print(type(msg))
      print(msg.text)
      msgg = (msg.text).find("-id")
      print(type(msgg))

      if msgg >= 0:
        bot.send_message(int(msg.text[0:msgg]) ,msg.text[msgg+4:])
        print(msgg)
        print(msg.text[0:msgg])


@server.route('/'+TOKEN,methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return '!' , 200

@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url = ''+TOKEN)
    return '!', 200

if __name__=="__main__":
    server.run(host='0.0.0.0' ,port= int(os.environ.get('PORT' , 5000)))




