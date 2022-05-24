from aiogram import types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext

import keyboard as kb
from service.servicepool import ServicePool
from fsm.fsm import FSMCustom
from aiostates import AioState
import builder

from functions import admin_panel, message_collector, place, return_main, show_user_comments ,show_comments, sub_mailing, up_to_main, show_rating, is_admin

import dicttool
from events import event_system
import config
from entry import bot, dp

import requests


fsm = FSMCustom()
ServicePool.create() 


@dp.message_handler(commands=["start"])
async def start_app(message: types.Message):

     await event_system.EventSystem.bind_event("Назад", "up_main")
     await event_system.EventSystem.bind_event("В главное меню", "main")
     await event_system.EventSystem.bind_event("Отзывы", "comments")
     await event_system.EventSystem.bind_event("Рейтинг", "rating")
     await event_system.EventSystem.bind_event("Подписаться на рассылку", "options")
     await event_system.EventSystem.bind_event("Отписаться от рассылки", "options")
     await event_system.EventSystem.bind_event("Мои отзывы", "user_comments")

     print("App startig... \n")
     
     await bot.send_message(message.from_user.id, f"Привет {message.from_user.first_name}, на связи Информатор-бот!", reply_markup=kb.mainMenuParent)
     
     await AioState.any_state.set()

     uiUser = {       
          'id': message.from_user.id,
          'name': f"{message.from_user.first_name}",
          'role': "User",
          'subscription': True,
          'city': "TLT"
     }

     response = requests.post(f"https://ta-bot-api-gateway.herokuapp.com/api/register", json = uiUser).json()

     print(response)

     await bot.send_message(message.from_user.id, "Добро пожаловать!")


@dp.message_handler(state = AioState.placeSearch)
async def place_search(message: types.Message, state: FSMContext):  
     await place(message, state)
     

@dp.message_handler(state = AioState.category)
async def find_with_category(message: types.Message):

     if message.text.lower() == "назад" or message.text.lower() == "в главное меню":
          await AioState.any_state.set()

          if await is_admin(message.from_user.id):
               await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb.mainMenuAdmin)
          else:
               await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb.mainMenuUser)

     else:

          category_id = await dicttool.get_value_by_key(config.CATEGORY_ALIAS, message.text)

          uiCategory = {
               'id': category_id,
               'name': message.text
          }

          response = requests.post(f"https://ta-bot-api-gateway.herokuapp.com/api/place/category", json=uiCategory).json()

          output_str = ""

          for place in response:
               output_str += f"{place['number']}.\t\t{place['namePlace']}\t\tАдрес: {place['address']}\n"

          await bot.send_message(message.from_user.id, output_str)

          print(response)


@dp.message_handler(state = AioState.options)
async def shopw_options(message: types.Message):
     await sub_mailing(message)



@dp.message_handler(state = AioState.adminPanel)
async def show_admin(message: types.Message, state: FSMContext):
     await admin_panel(message, state)



@dp.message_handler(state = AioState.comments)
async def show_comment(message: types.Message, state: FSMContext):
     
     if message.text.lower() == "назад" or message.text.lower() == "в главное меню":
          await AioState.placeSearch.set()
          await bot.send_message(message.from_user.id, "Выберите место", reply_markup=kb.searchMenu)

     elif message.text.lower() == "в главное меню":
          if await is_admin(message.from_user.id):
               await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb.mainMenuAdmin)
          else:
               await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb.mainMenuUser)


     elif message.text.lower() == "добавить отзыв":
          await AioState.reviewComment.set()
          await bot.send_message(message.from_user.id, "Введите текст отзыва", reply_markup=kb.reviewMenu)

     else:

          async with state.proxy() as data:
               pageNumber = data['comments'] + 1
             
          if pageNumber > 0:        
               async with state.proxy() as data:
                    data['comments'] += 1        
                    placeId = data['placeId']                       
                    response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/place/{placeId}/{pageNumber}").json()

          else:   
               async with state.proxy() as data:
                    placeId = data['placeId']                   
                    response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/place/{placeId}/{pageNumber}").json()                    
                    data['comments'] += 1

          output_str = ""

          count = 1
          
          if type(response) == list:

               if await dicttool.find_in(response, 'error') == True:
                    async with state.proxy() as data:
                         pageNumber = 0
                         data['comments'] = 0               
                    count = 1        
                    response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/place/{placeId}/{pageNumber}").json()
                    output_str = await builder.comments(response, count, output_str)
               else:         
                    output_str = await builder.comments(response, count, output_str)
          else:
               
               if await dicttool.has_key(response, 'error') == True:                                      
                    async with state.proxy() as data:
                         pageNumber = 0
                         data['comments'] = 0      
                    print("PLSID ", placeId)                                                                    
                    count = 1                   
                    response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/place/{placeId}/{pageNumber}").json()
                    output_str = await builder.comments(response, count, output_str)
               else:
                    output_str = await builder.comments(response, count, output_str)


          await bot.send_message(message.from_user.id, "Отзывы:\n\n" + output_str, reply_markup=kb.commentMenu)

          print("Comment page: ", pageNumber)  



@dp.message_handler(state = AioState.userComments)
async def show_user_comment(message: types.Message, state: FSMContext):
     
     if message.text.lower() == "назад":
          await AioState.placeSearch.set()
          await bot.send_message(message.from_user.id, "Выберите место", reply_markup=kb.searchMenu)
     
     elif message.text.lower() == "редактировать отзыв":
          await AioState.editComments.set()
          await bot.send_message(message.from_user.id, "Введите номер отзыва")

     elif message.text.lower() == "удалить отзыв":
          await AioState.removeComment.set()
          await bot.send_message(message.from_user.id, "Введите номер отзыва")
     
     elif message.text.lower() == "для конкретного места":          
          async with state.proxy() as data:
               data['userPlaceComments'] = 0

          await bot.send_message(message.from_user.id, "Введите название места", reply_markup = kb.userSubCommentsMenu)
          

          await AioState.determinatedPlace.set()

     elif message.text.lower() == "показать все":
          await bot.send_message(message.from_user.id, "Все отзывы", reply_markup=kb.userSubCommentsMenu)
          await AioState.userSubComments.set()
          
          async with state.proxy() as data:
               pageNumber = data['user_comments'] + 1
               

          if pageNumber > 0:        
               async with state.proxy() as data:
                    data['user_comments'] += 1  
                    response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/author/{message.from_user.id}/{pageNumber}").json()
                    print(response)

          else:   
               async with state.proxy() as data:                    
                    response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/author/{message.from_user.id}/{pageNumber}").json()
                    print(response)
                    data['user_comments'] += 1

          output_str = ""

          count = 1
          
          if type(response) == list:

               if await dicttool.find_in(response, 'error') == True:
                    async with state.proxy() as data:
                         pageNumber = 0
                         data['user_comments'] = 0        
                    count = 1        
                    response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/author/{message.from_user.id}/{pageNumber}").json()
                    output_str = await builder.user_comments(response, count, output_str)
               else:         
                    output_str = await builder.user_comments(response, count, output_str)
          else:
               
               if await dicttool.has_key(response, 'error') == True:                                      
                    async with state.proxy() as data:
                         pageNumber = 0
                         data['user_comments'] = 0                                       
                    count = 1                   
                    response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/author/{message.from_user.id}/{pageNumber}").json()
                    output_str = await builder.user_comments(response, count, output_str)
               else:
                    output_str = await builder.user_comments(response, count, output_str)


          await bot.send_message(message.from_user.id, "Мои отзывы:\n\n" + output_str, reply_markup=kb.userSubCommentsMenu)

          print("Comment page: ", pageNumber)
     

     else:

          async with state.proxy() as data:
               pageNumber = data['user_comments'] + 1
               

          if pageNumber > 0:        
               async with state.proxy() as data:
                    data['user_comments'] += 1  
                    response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/author/{message.from_user.id}/{pageNumber}").json()
                    print(response)

          else:   
               async with state.proxy() as data:                    
                    response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/author/{message.from_user.id}/{pageNumber}").json()
                    print(response)
                    data['user_comments'] += 1

          output_str = ""

          count = 1
          
          if type(response) == list:

               if await dicttool.find_in(response, 'error') == True:
                    async with state.proxy() as data:
                         pageNumber = 0
                         data['user_comments'] = 0        
                    count = 1        
                    response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/author/{message.from_user.id}/{pageNumber}").json()
                    output_str = await builder.user_comments(response, count, output_str)
               else:         
                    output_str = await builder.user_comments(response, count, output_str)
          else:
               
               if await dicttool.has_key(response, 'error') == True:                                      
                    async with state.proxy() as data:
                         pageNumber = 0
                         data['user_comments'] = 0                                       
                    count = 1                   
                    response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/author/{message.from_user.id}/{pageNumber}").json()
                    output_str = await builder.user_comments(response, count, output_str)
               else:
                    output_str = await builder.user_comments(response, count, output_str)


          await bot.send_message(message.from_user.id, "Мои отзывы:\n\n" + output_str, reply_markup=kb.userSubCommentsMenu)

          print("Comment page: ", pageNumber)


@dp.message_handler(state = AioState.userSubComments)
async def show_user_comment(message: types.Message, state: FSMContext):
     
     if message.text.lower() == "назад":
          await AioState.userComments.set()
          await bot.send_message(message.from_user.id, "Мои отзывы", reply_markup=kb.userCommentMenu)

     elif message.text.lower() == "в главное меню":
          await AioState.any_state.set()

          if await is_admin(message.from_user.id):
               await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb.mainMenuAdmin)
          else:
               await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb.mainMenuUser)
     
     else:
          async with state.proxy() as data:
               pageNumber = data['user_comments'] + 1
               

          if pageNumber > 0:        
               async with state.proxy() as data:
                    data['user_comments'] += 1  
                    response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/author/{message.from_user.id}/{pageNumber}").json()
                    print(response)

          else:   
               async with state.proxy() as data:                    
                    response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/author/{message.from_user.id}/{pageNumber}").json()
                    print(response)
                    data['user_comments'] += 1

          output_str = ""

          count = 1
          
          if type(response) == list:

               if await dicttool.find_in(response, 'error') == True:
                    async with state.proxy() as data:
                         pageNumber = 0
                         data['user_comments'] = 0        
                    count = 1        
                    response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/author/{message.from_user.id}/{pageNumber}").json()
                    output_str = await builder.user_comments(response, count, output_str)
               else:         
                    output_str = await builder.user_comments(response, count, output_str)
          else:
               
               if await dicttool.has_key(response, 'error') == True:                                      
                    async with state.proxy() as data:
                         pageNumber = 0
                         data['user_comments'] = 0                                       
                    count = 1                   
                    response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/author/{message.from_user.id}/{pageNumber}").json()
                    output_str = await builder.user_comments(response, count, output_str)
               else:
                    output_str = await builder.user_comments(response, count, output_str)


          await bot.send_message(message.from_user.id, "Мои отзывы:\n\n" + output_str, reply_markup=kb.userSubCommentsMenu)

          print("Comment page: ", pageNumber)



@dp.message_handler(state = AioState.determinatedPlace)
async def user_comment_place(message: types.Message, state: FSMContext):
     async with state.proxy() as data:
          data['userPlaceName'] = message.text
     
     await AioState.determinatedComment.set()

     await bot.send_message(message.from_user.id, f"Отзывы для места '{message.text}'", reply_markup=kb.userSubCommentsMenu)
          
     if message.text.lower() == "назад":
          await AioState.placeSearch.set()
          await bot.send_message(message.from_user.id, "Выберите место", reply_markup=kb.searchMenu)

     elif message.text.lower() == "в главное меню":
          await AioState.any_state.set()

          if await is_admin(message.from_user.id):
               await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb.mainMenuAdmin)
          else:
               await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb.mainMenuUseru)
     else :
          
          excp = ""

          async with state.proxy() as data:
               try:
                    pageNumber = data['userPlaceComments'] + 1
                    uiPlace = {
                              'name': data['userPlaceName'],
                              'city': data['city']
                         }
                    
                    responsePlace = requests.post(f"https://ta-bot-api-gateway.herokuapp.com/api/place/name", json= uiPlace).json()
                    placeId = responsePlace['id']


                    if pageNumber > 0:        
                         async with state.proxy() as data:
                              data['userPlaceComments'] += 1
                              
                              response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/place/{placeId}/{message.from_user.id}/{pageNumber}").json()

                    else:   
                         async with state.proxy() as data: 
                              response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/place/{placeId}/{message.from_user.id}/{pageNumber}").json()                    
                              data['userPlaceComments'] += 1

                    output_str = ""

                    count = 1
                    
                    if type(response) == list:

                         if await dicttool.find_in(response, 'error') == True:
                              async with state.proxy() as data:
                                   pageNumber = 0
                                   data['userPlaceComments'] = 0               
                              count = 1        
                              response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/place/{placeId}/{message.from_user.id}/{pageNumber}").json()
                              output_str = await builder.comments(response, count, output_str)
                         else:         
                              output_str = await builder.comments(response, count, output_str)
                    else:
                         
                         if await dicttool.has_key(response, 'error') == True:                                      
                              async with state.proxy() as data:
                                   pageNumber = 0
                                   data['userPlaceComments'] = 0               
                              count = 1                   
                              response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/place/{placeId}/{message.from_user.id}/{pageNumber}").json()
                              output_str = await builder.comments(response, count, output_str)
                         else:
                              output_str = await builder.comments(response, count, output_str)


                    await bot.send_message(message.from_user.id, "Отзывы:\n\n" + output_str, reply_markup=kb.userSubCommentsMenu)

                    print("Comment page: ", pageNumber)
               
               except:
                    excp = config.except_middleware

                    await bot.send_message(message.from_user.id, excp)



@dp.message_handler(state = AioState.determinatedComment)
async def show_user_comment_place(message: types.Message, state: FSMContext):  

     if message.text.lower() == "назад":
          await AioState.placeSearch.set()
          await bot.send_message(message.from_user.id, "Выберите место", reply_markup=kb.searchMenu)

     elif message.text.lower() == "в главное меню":
          await AioState.any_state.set()

          if await is_admin(message.from_user.id):
               await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb.mainMenuAdmin)
          else:
               await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb.mainMenuUseru)

     else :
          
          async with state.proxy() as data:
               pageNumber = data['userPlaceComments'] + 1
               uiPlace = {
                         'name': data['userPlaceName'],
                         'city': data['city']
                    }
               
               responsePlace = requests.post(f"https://ta-bot-api-gateway.herokuapp.com/api/place/name", json= uiPlace).json()
               placeId = responsePlace['id']


               if pageNumber > 0:        
                    async with state.proxy() as data:
                         data['userPlaceComments'] += 1
                         
                         response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/place/{placeId}/{message.from_user.id}/{pageNumber}").json()

               else:   
                    async with state.proxy() as data: 
                         response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/place/{placeId}/{message.from_user.id}/{pageNumber}").json()                    
                         data['userPlaceComments'] += 1

               output_str = ""

               count = 1
               
               if type(response) == list:

                    if await dicttool.find_in(response, 'error') == True:
                         async with state.proxy() as data:
                              pageNumber = 0
                              data['userPlaceComments'] = 0               
                         count = 1        
                         response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/place/{placeId}/{message.from_user.id}/{pageNumber}").json()
                         output_str = await builder.comments(response, count, output_str)
                    else:         
                         output_str = await builder.comments(response, count, output_str)
               else:
                    
                    if await dicttool.has_key(response, 'error') == True:                                      
                         async with state.proxy() as data:
                              pageNumber = 0
                              data['userPlaceComments'] = 0               
                         count = 1                   
                         response = requests.get(f"https://ta-bot-api-gateway.herokuapp.com/api/place/{placeId}/{message.from_user.id}/{pageNumber}").json()
                         output_str = await builder.comments(response, count, output_str)
                    else:
                         output_str = await builder.comments(response, count, output_str)


               await bot.send_message(message.from_user.id, "Отзывы:\n\n" + output_str, reply_markup=kb.userSubCommentsMenu)

               print("Comment page: ", pageNumber)



@dp.message_handler(state = AioState.removeComment)
async def remove_comment(message: types.Message):
     requests.delete(f"https://ta-bot-api-gateway.herokuapp.com/api/review/{message.text}")

     await bot.send_message(message.from_user.id, "Отзыв успешно удален", reply_markup = kb.userCommentMenu)

     await AioState.userComments.set()



@dp.message_handler(state = AioState.editComments)
async def edit_comment(message: types.Message, state: FSMContext):
     async with state.proxy() as data:
          data['userPlaceId'] = message.text
     
     await AioState.reviewEditComments.set()

     await bot.send_message(message.from_user.id, "Введите текст отзыва", reply_markup=kb.reviewMenu) 



@dp.message_handler(state = AioState.reviewEditComments)
async def write_review(message: types.Message, state: FSMContext):
     if message.text.lower() == "без комментария":
          async with state.proxy() as data:
               data['review'] = ""

     else:
          async with state.proxy() as data:
               data['review'] = message.text
     
     await AioState.markEditComments.set()

     await bot.send_message(message.from_user.id, "Оцените место", reply_markup=kb.markMenu)



@dp.message_handler(state = AioState.markEditComments)
async def mark_review(message: types.Message, state: FSMContext):     
     async with state.proxy() as data:
          data['mark'] = await dicttool.get_value_by_key(config.MARKS_ALIAS, message.text)
                    
          uiReview = {
               'review': data['review'],
               'authorId': message.from_user.id,         
               'mark': data['mark'],
               'placeId': data['userPlaceId']
          }

          response = requests.put(f"https://ta-bot-api-gateway.herokuapp.com/api/review/{data['userPlaceId']}", json=uiReview).json()     

     print(response)

     await bot.send_message(message.from_user.id, "Отзыв был успешно изменен!", reply_markup=kb.userCommentMenu)

     await AioState.userComments.set()



@dp.message_handler(state = AioState.reviewComment)
async def write_review(message: types.Message, state: FSMContext):
     if message.text.lower() == "без комментария":
          async with state.proxy() as data:
               data['review'] = ""

     else:
          async with state.proxy() as data:
               data['review'] = message.text
     
     await AioState.markComment.set()

     await bot.send_message(message.from_user.id, "Оцените место", reply_markup=kb.markMenu)



@dp.message_handler(state = AioState.markComment)
async def mark_review(message: types.Message, state: FSMContext):     
     async with state.proxy() as data:
          data['mark'] = await dicttool.get_value_by_key(config.MARKS_ALIAS, message.text)
                    
          uiReview = {
               'review': data['review'],
               'authorId': message.from_user.id,         
               'mark': data['mark'],
               'placeId': data['placeId']
          }

     response = requests.post(f"https://ta-bot-api-gateway.herokuapp.com/api/review", json=uiReview).json()     

     print(response)

     await bot.send_message(message.from_user.id, "Благодарим за ваш отзыв!", reply_markup=kb.searchMenu)

     await AioState.placeSearch.set()



@dp.message_handler(state = AioState.citySwap)
async def change_city(message: types.Message, state: FSMContext):
     async with state.proxy() as data:
          data['city'] = message.text

     if await is_admin(message.from_user.id):
          await bot.send_message(message.from_user.id, f"Ваш город: {data['city']}", reply_markup=kb.mainMenuAdmin)
     else:
          await bot.send_message(message.from_user.id, f"Ваш город: {data['city']}", reply_markup=kb.mainMenuUser)
     

     await AioState.any_state.set()



@dp.message_handler(state = AioState.any_state)
async def bot_message(message: types.Message, state: FSMContext):    
     await message_collector(message, state)

    

@dp.message_handler()
async def other(message: types.Message):
     if message.text == "В главное меню":

          if await is_admin(message.from_user.id):
               await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb.mainMenuAdmin)
          else:
               await bot.send_message(message.from_user.id, "Главное меню", reply_markup=kb.mainMenu)

          await event_system.EventSystem.bind_event("Назад", "up_main")
          await event_system.EventSystem.bind_event("В главное меню", "main")
          await event_system.EventSystem.bind_event("Отзывы", "comments")
          await event_system.EventSystem.bind_event("Рейтинг", "rating")
          await event_system.EventSystem.bind_event("Подписаться на рассылку", "options")
          await event_system.EventSystem.bind_event("Отписаться от рассылки", "options")
          await event_system.EventSystem.bind_event("Мои отзывы", "user_comments")

          await AioState.any_state.set()



def awake():
     event_system.EventSystem.register_handler("up_main",  up_to_main)
     event_system.EventSystem.register_handler("main",  return_main)
     event_system.EventSystem.register_handler("comments", show_comments)
     event_system.EventSystem.register_handler("rating", show_rating)
     event_system.EventSystem.register_handler("options", sub_mailing)
     event_system.EventSystem.register_handler("user_comments", show_user_comments)


if __name__ == "__main__":
     awake()
     executor.start_polling(dp, skip_updates = True)