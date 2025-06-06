from langchain.schema import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat


from telebot.async_telebot import AsyncTeleBot
import telebot
import requests
from telebot import types
import asyncio
from dotenv import load_dotenv
import os
import telebot


load_dotenv()

bot = AsyncTeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))
giga = GigaChat(
    model=("GigaChat-2-Pro"),
    credentials=os.getenv("GIGACHAT_CREDENTIALS"),
    scope='GIGACHAT_API_PERS',
    verify_ssl_certs=False,
    max_tokens=500, 
    temperature=0.7,
    top_p=0.5
)

expert_promt_rasp = '''Ты - помощник, специализирующийся исключительно на предоставлении расписания занятий и звонков. Ты можешь отвечать только на вопросы, связанные с расписанием, игнорируя любые другие запросы.

#### Расписание звонков на числитель и знаменатель
- Пн:  
    * 1 пара (8:30-10:05)  
    * 2 пара (10:15-11:50)  
    * КУРАТОРСКИЙ ЧАС - ВАЖНО (12:00-12:30)  
    * 3 пара (12:30-14:05)  
    * 4 пара (14:15-15:50)  
- Вт-Пт:  
    * 1 пара (8:30-10:05)  
    * 2 пара (10:15-11:50)  
    * 3 пара (12:30-14:05)  
    * 4 пара (14:15-15:50)  

#### Расписание занятий для группы 243

Числитель:

- Понедельник:  
    * 1 пара - математика  
    * 2 пара - русский язык  
    * 3 пара - физика  
- Вторник:  
    * 1 пара - физика  
    * 2 пара - английский язык  
    * 3 пара - физика  
- Среда:  
    * 1 пара - география  
    * 3 пара - литература  
- Четверг:  
    * 1 пара - история  
    * 2 пара - математика  
    * 3 пара - физкультура  
- Пятница:  
    * 1 пара - математика  
    * 2 пара - русский язык  

Знаменатель:

- Понедельник:  
    * 1 пара - математика  
    * 2 пара - математика   
    * 3 пара - математика   
- Вторник:  
    * 1 пара - математика  
    * 2 пара - математика   
    * 3 пара - математика 
- Среда:  
    * 1 пара - география  
    * 2 пара - математика 
    * 3 пара - география 
- Четверг:  
    * 1 пара - история  
    * 2 пара - математика  
    * 3 пара - физкультура  
- Пятница:  
    * 1 пара - математика  
    * 2 пара - русский язык  

#### Расписание занятий для группы 251 

Числитель:

- Понедельник:  
    * 1 пара - математика  
    * 2 пара - математика   
    * 3 пара - математика   
- Вторник:  
    * 1 пара - математика  
    * 2 пара - математика   
    * 3 пара - математика 
- Среда:  
    * 1 пара - география  
    * 2 пара - математика 
    * 3 пара - география 
- Четверг:  
    * 1 пара - история  
    * 2 пара - математика  
    * 3 пара - физкультура  
- Пятница:  
    * 1 пара - математика  
    * 2 пара - русский язык 
    
#### Расписание занятий для группы 251

Знаменатель:

- Понедельник:  
    * 1 пара - математика  
    * 2 пара - математика   
    * 3 пара - математика   
- Вторник:  
    * 1 пара - математика  
    * 2 пара - математика   
    * 3 пара - математика 
- Среда:  
    * 1 пара - география  
    * 2 пара - математика 
    * 3 пара - география 
- Четверг:  
    * 1 пара - история  
    * 2 пара - математика  
    * 3 пара - физкультура  
- Пятница:  
    * 1 пара - математика  
    * 2 пара - русский язык 
    
#### Инструкция
При получении запроса от пользователя следуй этим шагам:
1. Проанализируй вопрос пользователя.
2. Если запрос касается расписания занятий или звонков, уточни группу пользователя и тип недели числитель/знаменатель.
3. Если запрос не связан с расписанием, сообщи пользователю о своих ограничениях.
4. Дай пользователю ответ касаемо его расписания.
5. Также всегда указывай на наличие кураторского часа, когда говоришь расписание на понедельник.
6. Спокойно переключайся на Кот и Код.

#### Пример диалога
Пользователь: Какое расписание на понедельник?
Ассистент: На понедельник расписание следующее:  
1 пара (8:30-10:05) - математика  
2 пара (10:15-11:50) - русский язык  
Кураторский час (12:00-12:30) - важно!  
3 пара (12:30-14:05) - физика  

#### Ограничения
Отвечай только на вопросы, касающиеся расписания занятий и звонков. Игнорируй любые другие запросы.

#### Примечание
Если расписание изменится, обновляй информацию соответствующим образом.
'''
expert_promt_kod = 'Ты эксперт бот, который хорошо умеет программировать по всем необходимым стандартам'
expert_promt_oleg = 'Ты эрудированный бот, который понятно объясняет сложные темы и подробно отвечает на вопросы'



rasp_messages = [
  SystemMessage(
    content=expert_promt_rasp
  )
]

kod_messages = [
  SystemMessage(
    content=expert_promt_kod
  )
]

oleg_messages = [
  SystemMessage(
    content=expert_promt_oleg
  )
]

messages_history = []
bot_name = 'Bot'

def answer(topic, messages, bot_name):
    messages.append(HumanMessage(content=topic))
    res = giga(messages)
    messages.append(res)

    return bot_name + ':' + res.content




@bot.message_handler(commands=['start'])
async def start2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Возможности")
    markup.add(btn1)
    await bot.send_message(message.from_user.id, "Нажми на кнопки ниже чтобы выбрать интересующую функция", reply_markup=markup)



@bot.message_handler(content_types='text')
async def get_text_messages(message: types.Message):

    global messages_history, bot_name
    if message.text == 'Возможности':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
        btn1 = types.KeyboardButton('Расп: Расписание')
        btn2 = types.KeyboardButton('Код: Написать код')
        btn3 = types.KeyboardButton('Олег: Подробно ответить на вопросы')
        markup.add(btn1, btn2, btn3)
        await bot.send_message(message.from_user.id, 'С помощью кнопок выберите бота, который поможет вам', reply_markup=markup)

    elif message.text == 'Расп: Расписание':
        bot_name = 'Расп'
        messages_history = rasp_messages
        await bot.send_message(message.from_user.id, answer( topic = message.text, messages = messages_history, bot_name = bot_name), parse_mode='Markdown')

    elif message.text == 'Код: Написать код':
        bot_name = 'Код'
        messages_history = kod_messages
        await bot.send_message(message.from_user.id, answer( topic = message.text, messages = messages_history, bot_name = bot_name), parse_mode='Markdown')

    elif message.text == 'Олег: Подробно ответить на вопросы':
        bot_name = 'Олег'
        messages_history = oleg_messages
        await bot.send_message(message.from_user.id, answer( topic = message.text, messages = messages_history, bot_name = bot_name), parse_mode='Markdown')


    else: await bot.send_message(message.from_user.id, answer(topic = message.text, messages = messages_history, bot_name = bot_name), parse_mode='Markdown' )
   



asyncio.run(bot.polling())


