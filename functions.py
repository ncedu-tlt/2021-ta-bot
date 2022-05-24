import requests
from config import IGONRE_WORDS, except_middleware

from aiogram import types
from aiogram.dispatcher import FSMContext
import keyboard as kb

from aiostates import AioState

from entry import bot

import middleware

@middleware.filter(IGONRE_WORDS)
async def place(message: types.Message, state: FSMContext):

     print("!!!")

     ecxp = ""

     async with state.proxy() as data:
          try:
               uiPlace = {
                    'name': message.text,
                    'city': data['city']
               }

               response = requests.post("https://ta-bot-api-gateway.herokuapp.com/api/place/name", json=uiPlace).json()

               print(response)

               async with state.proxy() as data: 
                    data['placeSearch'] = message.text
                    data['placeId'] = response['id']
                    data['comments'] = -1
                    
                    print(data['placeSearch'])
                    print(data['placeId'])
                    print(data['comments'])

          except:
               ecxp = except_middleware

     
     if ecxp == "":     
          await bot.send_message(message.from_user.id, f"Вы выбрали место: {message.text}")

     else:
          await bot.send_message(message.from_user.id, ecxp)
     



async def message_collector(message: types.Message, state: FSMContext):

     if message.text == "Меню":
          if await is_admin(message.from_user.id):
               await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb.mainMenuAdmin)
          else:
               await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb.mainMenuUser)
               
     elif message.text == "Выбрать место":
          await AioState.placeSearch.set()

          async with state.proxy() as data:               
               data['user_comments'] = -1
               print(data['user_comments'])
         
          await bot.send_message(message.from_user.id, "Введите место", reply_markup=kb.searchMenu)
          
     elif message.text == "Рейтинг":
          await AioState.rating.set()
          await bot.send_message(message.from_user.id, "Способ просмотра рейтинга", reply_markup=kb.searchSubMenu)

     elif message.text == "Категории":
          await AioState.category.set()
          await bot.send_message(message.from_user.id, "Категории поиска", reply_markup=kb.categoryMenu)
          
     elif message.text == "Настройки":
          await AioState.options.set()
          await bot.send_message(message.from_user.id, "Выберите нужные настройки", reply_markup=kb.optionsMenu)

     elif message.text == "Админ-панель":
          if await is_admin(message.from_user.id):
               await AioState.adminPanel.set()
               await bot.send_message(message.from_user.id, "Меню администратора", reply_markup=kb.adminMenu)
          else:
               await bot.send_message(message.from_user.id, "Я не понимаю тебя", reply_markup=kb.mainMenuUser)
     
     elif message.text == "Отзывы":       
          await AioState.comments.set()
          await bot.send_message(message.from_user.id, "Просмотр отзывов", reply_markup=kb.commentMenu)

     elif message.text == "Мои отзывы":
          await AioState.userComments.set()
          await bot.send_message(message.from_user.id, "Мои отзывы", reply_markup=kb.commentMenu)

     elif message.text == "Выбрать город":
          await AioState.citySwap.set()
          await bot.send_message(message.from_user.id, "Введите город")
     
     elif message.text == "Категории":
          await AioState.category.set()
          await bot.send_message(message.from_user.id, "Здесь вы можете найти популярные места по категориям", reply_markup=kb.categoryMenu)




async def sub_mailing(message: types.Message):
     hasSub = False 
     
     if message.text.lower() == "подписаться на рассылку":
          hasSub = True

          uiUser = {
          'subscription': hasSub
          }

          response = requests.put(f"https://ta-bot-api-gateway.herokuapp.com/api/subscription/{message.from_user.id}", json=uiUser).json()
          print(response)

          await bot.send_message(message.from_user.id, "Теперь вы будете получать новости")



     elif message.text.lower() == "отписаться от рассылки":
          hasSub = False

          uiUser = {
          'subscription': hasSub
          }
          
          response = requests.put(f"https://ta-bot-api-gateway.herokuapp.com/api/subscription/{message.from_user.id}", json=uiUser).json()
          print(response)
          
          await bot.send_message(message.from_user.id, "Теперь вы не будете получать новости")


     elif message.text.lower() == "в главное меню":
          await AioState.any_state.set()
          if await is_admin(message.from_user.id):
               await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb.mainMenuAdmin)
          else:
               await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb.mainMenuUser)



async def show_user_comments(message: types.Message):
     await AioState.userComments.set()
     await bot.send_message(message.from_user.id, "Мои отзывы", reply_markup=kb.userCommentMenu)



async def show_comments(message: types.Message):          
     await AioState.comments.set()
     await bot.send_message(message.from_user.id, "Просмотр отзывов", reply_markup=kb.commentMenu)




async def show_rating(message: types.Message):
     if message.text.lower() == "рейтинг":
          response =  requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/rating/tenbestplace").json()
          output_str = ""
          for each in response:
               output_str += f"{each['number']}. {each['namePlace']} {each['ratingRatio']}\n"
          
          await bot.send_message(message.from_user.id, "Рейтинг мест положительные/отрицательные оценки\n" + output_str, reply_markup=kb.searchMenu)



async def admin_panel(message: types.Message, state: FSMContext):

     output_str = ""

     if message.text.lower() == "опубликовать":

          response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/subscription").json()

          for each in response:
               output_str += f"{each}\n"

               try:                     
                    
                    async with state.proxy() as data:

                         await bot.send_message(each['id'], data['mail'], reply_markup=kb.adminMenu)
               except:                    
                    print("ID not found: ", each['id'])

     elif message.text.lower() == "в главное меню":
          await AioState.any_state.set()
          await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb.mainMenuAdmin)
     else:
          async with state.proxy() as data:
               data['mail'] = message.text



async def up_to_main(message: types.Message):
     if await is_admin(message.from_user.id):
          await bot.send_message(message.from_user.id, "Возврат в главное меню", reply_markup=kb.mainMenuAdmin)
     else:
          await bot.send_message(message.from_user.id, "Возврат в главное меню", reply_markup=kb.mainMenuUser)

     await AioState.any_state.set()



async def return_main(message: types.Message):
     if await is_admin(message.from_user.id):
          await bot.send_message(message.from_user.id, "В главное меню", reply_markup=kb.mainMenuAdmin)
     else:
          await bot.send_message(message.from_user.id, "В главное меню", reply_markup=kb.mainMenuUser)
     await AioState.any_state.set()



async def is_admin(user_id: int):
     response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/role/{user_id}").json()

     if str(response['role']).lower() == "admin":
          return True
     else:
          return False
