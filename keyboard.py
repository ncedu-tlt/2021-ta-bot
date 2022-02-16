from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


#--- button main menu parent ----
btnMemu = KeyboardButton("Меню")
btnBack = KeyboardButton("Назад")

#--- buttons main menu ----
btnSearch = KeyboardButton("Поиск")
btnCategory = KeyboardButton("Категории")
btnOptions = KeyboardButton("Настройки") 



#--- buttons search menu ----
btnReview = KeyboardButton("Отзывы")
btnRating = KeyboardButton("Рейтинг")

#--- buttons search sub menu---
btnChoicePicture = KeyboardButton("Картинкой")
btnChoiceText = KeyboardButton("Текстом")
 


#--- buttons category menu ----
btnTopPlaces = KeyboardButton("Топ-10 мест")


#--- buttons options menu ----
btnSubscribeMailingOn = KeyboardButton("Подписаться на рассылку")
btnSubscribeMailingOff = KeyboardButton("Отписаться от рассылки")


#--- keyboards ----  
mainMenuParent = ReplyKeyboardMarkup().add(btnMemu)
mainMenu = ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True).add(btnSearch, btnCategory, btnOptions, btnBack)
searchMenu = ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True).add(btnReview, btnRating, btnBack)
searchSubMenu = ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True).add(btnChoicePicture, btnChoiceText, btnBack)
categoryMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnTopPlaces, btnBack)
optionsMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnSubscribeMailingOn, btnSubscribeMailingOff)