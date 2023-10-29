import datetime

import telebot

from telebot import types
from threading import Thread
from function import *


bot_token = '5641281628:AAG7Wv1YU-wzXH5ondK2q1zMRaAjZnuQ_iA'
bot = telebot.TeleBot(bot_token)



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
).add(types.KeyboardButton("💵Расчет💵")) 



all_list = ['1829352344', '1025194570', '1053756513', '326639777', '354493576']
employee_list = ['1829352344', '1025194570', '1053756513']

data_enter = {
	'1025194570': '',
	'1829352344': '',
	'1053756513': ''
}

data_enter_prepayment = {
	'1025194570': False,
	'1829352344': False,
	'1053756513': False
}


def check_date():
	while True:
		now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime('%H:%M:%S')
		if now == '09:30:00':
			days_ = get_json()

			day = [str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).year), str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).day), str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).month)]
			interval_ = get_interval(day, days_)

			for user in employee_list:
				try:
					if f'{day[2]}.{day[1]}' not in days_[interval_][user]['day'].keys():
						bot.send_message(user, f'🕓Пора сделать выбор!', reply_markup=button_)
				except Exception as e:
					print(f'{user} - {e}')

def start_bot():
	while True:
		try:
			bot.polling(non_stop=True, interval=0)
		except Exception as e:
			print(e)

@bot.message_handler(commands=['start'])
def start(message):
	user_id = str(message.from_user.id)
	if user_id in employee_list:
		bot.send_message(message.chat.id, 'Привет! Я бот для учета рабочих дней и выходных', reply_markup=button_)
	else:
		bot.send_message(message.chat.id, 'Извини, ты не сотрудник (')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	user_id = str(call.message.chat.id)

	days_ = get_json()

	day = [str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).year), str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).day), str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).month)]
	interval_ = get_interval(day, days_)

	if call.data == 'full':
		bot.edit_message_text(f'Отлично! Вы выбрали "{data_enter[user_id]}"(Полная смена)\nПодтвердить?', call.message.chat.id, call.message.message_id, reply_markup=button_confirm_full)

	if call.data == 'half':
		bot.edit_message_text(f'Отлично! Вы выбрали "{data_enter[user_id]}"(Неполная смена)\nПодтвердить?', call.message.chat.id, call.message.message_id, reply_markup=button_confirm_half)

	if call.data == 'yes_full':
		days_[interval_][user_id]['day'][f'{day[2]}.{day[1]}'] = f'{data_enter[user_id]}(Полная смена)'

		bot.edit_message_text(f'Отлично! Вы выбрали "{data_enter[user_id]}"', call.message.chat.id, call.message.message_id)

		for user in all_list:
			if user_id != user or user_id != '1829352344':
				try:
					bot.send_message(user, f'{days_[interval_][user_id]["Name"]} выбрал "{data_enter[user_id]}"(Полная смена)', reply_markup=button_)
				except Exception as e:
					print(f'{user} - {e}')
		
	if call.data == 'yes_half':
		days_[interval_][user_id]['day'][f'{day[2]}.{day[1]}'] = f'{data_enter[user_id]}(Неполная смена)'

		bot.edit_message_text(f'Отлично! Вы выбрали "{data_enter[user_id]}"(Неполная смена)', call.message.chat.id, call.message.message_id)

		for user in all_list:
			if user_id != user or user_id != '1829352344':
				try:
					bot.send_message(user, f'{days_[interval_][user_id]["Name"]} выбрал "{data_enter[user_id]}"(Неполная смена)', reply_markup=button_)
				except Exception as e:
					print(f'{user} - {e}')

	if call.data == 'yes':
		days_[interval_][user_id]['day'][f'{day[2]}.{day[1]}'] = data_enter[user_id]

		bot.edit_message_text(f'Отлично! Вы выбрали "{data_enter[user_id]}"', call.message.chat.id, call.message.message_id)

		for user in all_list:
			if user_id != user or user_id != '1829352344':
				try:
					bot.send_message(user, f'{days_[interval_][user_id]["Name"]} выбрал "{data_enter[user_id]}"', reply_markup=button_)
				except Exception as e:
					print(f'{user} - {e}')

	if call.data == 'no':
		bot.edit_message_text(f'Выбери другой ответ', call.message.chat.id, call.message.message_id, reply_markup=button_)

	post_json(days_)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	global data_enter

	user_id = str(message.from_user.id)


	if user_id not in all_list:
		bot.send_message(message.chat.id, 'Извини, ты не сотрудник (')
		return

	days_ = get_json()

	day = [str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).year), str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).day), str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).month)]
	interval_ = get_interval(day, days_)

	if data_enter_prepayment[user_id]:
		if message.text.isdigit():
			days_[interval_][user_id]["prepayment"] += int(message.text)
			bot.send_message(message.chat.id, f'Вы взяли аванс на {message.text}руб.\nВаш текущий аванс - {days_[interval_][user_id]["prepayment"]}руб.', reply_markup=button_)
			post_json(days_)
		else:
			bot.send_message(message.chat.id, 'Вы ввели не число!', reply_markup=button_)
		data_enter_prepayment[user_id] = False

	if (message.text == '🛠️Саморез+' or message.text == '🛴Самокат+' or message.text == '🏠Выходной') and user_id in employee_list:
		if interval_ != None:
			try:
				if f'{day[2]}.{day[1]}' not in days_[interval_][user_id]['day'].keys():
					data_enter[user_id] = message.text
					if  message.text != '🏠Выходной':
						bot.send_message(message.chat.id, f'Вы выбрали "{message.text}"\nВыберите какой рабочий день', reply_markup=button_choose)
					else:
						bot.send_message(message.chat.id, f'Вы выбрали "{message.text}"', reply_markup=button_confirm)
				else:
					bot.send_message(message.chat.id, f'Вы уже выбрали "{days_[interval_][user_id]["day"][f"{day[2]}.{day[1]}"]}"', reply_markup=button_)
			except:
				return

	elif message.text == '💵Расчет💵':
		answer = calculation_money(days_, interval_)

		bot.send_message(message.chat.id, 
			f'*Расчёт на {interval_}*\n\n'

			f'*Иван*:\n'

			f'	🛠️Саморез:\n'
			f'	-_Полный_ - {answer["Александр"]["day"]["🛠️Саморез+"]["full"]}\n'
			f'	-_Неполный_ - {answer["Александр"]["day"]["🛠️Саморез+"]["half"]}\n'

			f'	🛴Самокат:\n'
			f'	-_Полный_ - {answer["Александр"]["day"]["🛴Самокат+"]["full"]}\n'
			f'	-_Неполный_ - {answer["Александр"]["day"]["🛴Самокат+"]["half"]}\n'

			f'	🏠Выходной - {answer["Александр"]["day"]["🏠Выходной"]}\n\n'
			f'*Заработано > {answer["Александр"]["money"]}₽*\n'
			f'*Аванс >> {days_[interval_]["1053756513"]["prepayment"]}₽*\n'
			f'*Заработано с учетом аванса >>> {answer["Александр"]["money"] - days_[interval_]["1053756513"]["prepayment"]}₽*\n\n\n'

			f'*Петр*:\n'
			
			f'	🛠️Саморез:\n'
			f'	-_Полный_ - {answer["Андрей"]["day"]["🛠️Саморез+"]["full"]}\n'
			f'	-_Неполный_ - {answer["Андрей"]["day"]["🛠️Саморез+"]["half"]}\n'

			f'	🛴Самокат:\n'
			f'	-_Полный_ - {answer["Андрей"]["day"]["🛴Самокат+"]["full"]}\n'
			f'	-_Неполный_ - {answer["Андрей"]["day"]["🛴Самокат+"]["half"]}\n'

			f'	🏠Выходной - {answer["Андрей"]["day"]["🏠Выходной"]}\n\n'

			f'*Заработано > {answer["Андрей"]["money"]}₽*\n'
			f'*Аванс >> {days_[interval_]["1025194570"]["prepayment"]}₽*\n'
			f'*Заработано с учетом аванса >>> {answer["Андрей"]["money"] - days_[interval_]["1025194570"]["prepayment"]}₽*'

			, reply_markup=button_, parse_mode="Markdown")
	
	elif message.text == '💵Аванс💵':
		data_enter_prepayment[user_id] = True
		bot.send_message(message.chat.id, 'Введите сумму аванса\nБез символов и точек, просто число!', reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
	th_bot = Thread(target=start_bot)
	th_date = Thread(target=check_date)

	th_bot.start()
	th_date.start()