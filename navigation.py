from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

bthProfile = KeyboardButton('Profile')
bthSub = KeyboardButton('Subscription')
bthList = KeyboardButton("For subscriber")


mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(bthProfile, bthSub, bthList)


sub_inline_markup = InlineKeyboardMarkup(row_width=1)
bthSubMonth = InlineKeyboardButton(text='Month - 150 rubles', callback_data='submonth')
sub_inline_markup.insert(bthSubMonth)
