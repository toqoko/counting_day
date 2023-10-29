from telebot import types

button_admin = types.ReplyKeyboardMarkup(resize_keyboard=True) 
button_admin.add(types.KeyboardButton("💼Новый сотрудник")).add(types.KeyboardButton("👨‍💻Сотрудники"))

button_confirm_user_add = types.InlineKeyboardMarkup()
button_confirm_user_add.add(
	types.InlineKeyboardButton(text='✅ДА✅', callback_data='yes_user_add'), 
	types.InlineKeyboardButton(text='❌ЗАНОВО❌', callback_data='no_user_add'), 
)

button_delete_user= types.InlineKeyboardMarkup()
button_delete_user.add(types.InlineKeyboardButton(text='👟УВОЛИТЬ👟', callback_data='dell'))

button_confirm_half = types.InlineKeyboardMarkup()
button_confirm_full = types.InlineKeyboardMarkup()
button_confirm = types.InlineKeyboardMarkup()
button_choose = types.InlineKeyboardMarkup()


button_confirm_half.add(
	types.InlineKeyboardButton(text='✅ВЫБРАТЬ✅', callback_data='yes_half'), 
	types.InlineKeyboardButton(text='❌ОТМЕНА❌', callback_data='no'), 
)
button_confirm_full.add(
	types.InlineKeyboardButton(text='✅ВЫБРАТЬ✅', callback_data='yes_full'), 
	types.InlineKeyboardButton(text='❌ОТМЕНА❌', callback_data='no'), 
)
button_confirm.add(
	types.InlineKeyboardButton(text='✅ВЫБРАТЬ✅', callback_data='yes'), 
	types.InlineKeyboardButton(text='❌ОТМЕНА❌', callback_data='no'), 
)
button_choose.add(
	types.InlineKeyboardButton(text='🕘НЕПОЛНЫЙ🕘', callback_data='half'), 
	types.InlineKeyboardButton(text='🕘ПОЛНЫЙ🕘', callback_data='full')
).add(types.InlineKeyboardButton(text='❌ОТМЕНА❌', callback_data='no'))


button_ = types.ReplyKeyboardMarkup(resize_keyboard=True) 

button_.add(
	types.KeyboardButton("🛠️Саморез+"), 
	types.KeyboardButton("🛴Самокат+")
).add(
	types.KeyboardButton("🏠Выходной"), 
	types.KeyboardButton("💵Аванс💵")
).add(
	types.KeyboardButton("💼Новый сотрудник"),
	types.KeyboardButton("👨‍💻Сотрудники")
).add(types.KeyboardButton("💵Расчет💵"))