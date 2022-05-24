from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


#--- button main menu parent ----
btnMainMenu = KeyboardButton("В главное меню")
btnAdminPanel = KeyboardButton("Админ-панель")
btnMenu = KeyboardButton("Меню")
btnBack = KeyboardButton("Назад")


#--- buttons main menu ----
btnPlace = KeyboardButton("Выбрать место")
btnOptions = KeyboardButton("Настройки") 
btnCity = KeyboardButton("Выбрать город")


#--- buttons search menu ----
btnReview = KeyboardButton("Отзывы")
btnRating = KeyboardButton("Рейтинг")
btnUserReview = KeyboardButton("Мои отзывы")
btnAddComment = KeyboardButton("Добавить отзыв")
btnNoReview = KeyboardButton("Без комментария")


btnVeryBadMark = KeyboardButton("Ужасно")
btnBadMark = KeyboardButton("Плохо")
btnNormalMark = KeyboardButton("Нормально")
btnGoodMark = KeyboardButton("Хорошо")
btnExcellentMark = KeyboardButton("Отлично")


#--- buttons search sub menu---
btnChoicePicture = KeyboardButton("Картинкой")
btnChoiceText = KeyboardButton("Текстом")
 
 

#--- buttons category menu ----
btnTopPlaces = KeyboardButton("Топ-10 мест")
btnCategory = KeyboardButton("Категории")

btnTC = KeyboardButton("ТЦ")
btnRes = KeyboardButton("Ресторан")
btnСaly = KeyboardButton("Кальянная")
btnBil = KeyboardButton("Бильярдная")
btnBann = KeyboardButton("Баня")
btnPub = KeyboardButton("Паб")
btnClub = KeyboardButton("Клуб")
btnPark = KeyboardButton("Парк")
btnCoff = KeyboardButton("Кофейня")

#--- buttons options menu ----
btnSubscribeMailingOn = KeyboardButton("Подписаться на рассылку")
btnSubscribeMailingOff = KeyboardButton("Отписаться от рассылки")


#--- buttons admin menu ----
btnPublish = KeyboardButton("Опубликовать")
btnEditComment = KeyboardButton("Редактировать отзыв")


#--- buttons comment menu ----
btnNext = KeyboardButton("Еще")
btnEditComment = KeyboardButton("Редактировать отзыв")
btnRemoveComment = KeyboardButton("Удалить отзыв")
btnPlaceUserReview = KeyboardButton("Для конкретного места")
btnMyComments = KeyboardButton("Показать все")


#--- keyboards ----  
mainMenuParent = ReplyKeyboardMarkup().add(btnMenu)
mainMenuAdmin = ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True).add(btnPlace, btnOptions, btnCity, btnCategory, btnAdminPanel)
mainMenuUser = ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True).add(btnPlace, btnOptions, btnCity, btnCategory)
searchMenu = ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True).add(btnReview, btnUserReview, btnRating, btnBack, btnMainMenu)
searchSubMenu = ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True).add(btnChoicePicture, btnChoiceText, btnBack, btnMainMenu)
categoryMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnTopPlaces, btnBack, btnMainMenu)
optionsMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnSubscribeMailingOn, btnSubscribeMailingOff, btnMainMenu)
adminMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnPublish, btnBack, btnMainMenu) 
commentMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnNext, btnAddComment, btnBack, btnMainMenu)
userCommentMenu = ReplyKeyboardMarkup(row_width = 2, resize_keyboard=True).add(btnMyComments, btnPlaceUserReview, btnEditComment, btnRemoveComment, btnBack, btnMainMenu)
reviewMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnNoReview, btnBack, btnMainMenu)
markMenu = ReplyKeyboardMarkup(row_width = 2, resize_keyboard=True).add(btnVeryBadMark, btnBadMark, btnNormalMark, btnGoodMark, btnExcellentMark, btnBack, btnMainMenu)
categoryMenu = ReplyKeyboardMarkup(row_width = 2, resize_keyboard=True).add(btnTC, btnRes, btnСaly, btnBil, btnBann, btnPub, btnClub, btnPark, btnCoff, btnBack, btnMainMenu)
userSubCommentsMenu = ReplyKeyboardMarkup(row_width = 2, resize_keyboard=True).add(btnNext, btnBack, btnMainMenu)