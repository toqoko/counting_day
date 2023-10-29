import datetime

import telebot

from telebot import types
from threading import Thread
from function import *
from button import *
from config import *



bot = telebot.TeleBot(bot_token)

user_add = {
	'data': {
		'id': None,
		'name': None,
		'salary': None 
	},
	'status': None
}


@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, 'Привет! Я бот для учета рабочих дней и выходных', reply_markup=button_)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	global user_add
	

	if call.data == 'yes_user_add':
		bot.edit_message_text(f'Отлично! Вы добавили нового сотрудника', call.message.chat.id, call.message.message_id)
		add_employee(user_add['data'])
		user_add['data'] = {}
		user_add['status'] = None

	elif call.data == 'no_user_add':
		bot.edit_message_text(f'Перешли мне любое сообщения нового сотрудника', call.message.chat.id, call.message.message_id)
		user_add['data'] = {}
		user_add['status'] = 'id'

	elif call.data == 'dell':
		bot.edit_message_text('👟Уволен', call.message.chat.id, call.message.message_id)
		data = get_json()
		del data[call.message.text.split('---')[1]]
		post_json(data)

	user_id = str(call.message.chat.id)

	data = get_json()
	day = [str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).year), str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).day), str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).month)]


	if call.data == 'full':
		chose = call.message.text.split('"')[1]
		bot.edit_message_text(f'Отлично! Вы выбрали "{chose}"(Полная смена)\nПодтвердить?', call.message.chat.id, call.message.message_id, reply_markup=button_confirm_full)

	if call.data == 'half':
		chose = call.message.text.split('"')[1]
		bot.edit_message_text(f'Отлично! Вы выбрали "{chose}"(Неполная смена)\nПодтвердить?', call.message.chat.id, call.message.message_id, reply_markup=button_confirm_half)

	if call.data == 'yes_full':
		chose = call.message.text.split('"')[1]
		data[user_id]['days'][f'{day[2]}.{day[1]}.{day[0]}'] = f'{chose}(Полная смена)'

		bot.edit_message_text(f'Отлично! Вы выбрали "{chose}"', call.message.chat.id, call.message.message_id)

		for user in data.keys():
			if user_id != user:
				try:
					bot.send_message(user, f'{days_[interval_][user_id]["Name"]} выбрал "{chose}"(Полная смена)', reply_markup=button_)
				except Exception as e:
					print(f'{user} - {e}')
		
	if call.data == 'yes_half':
		chose = call.message.text.split('"')[1]
		data[user_id]['days'][f'{day[2]}.{day[1]}.{day[0]}'] = f'{chose}(Неполная смена)'

		bot.edit_message_text(f'Отлично! Вы выбрали "{chose}"(Неполная смена)', call.message.chat.id, call.message.message_id)

		for user in data.keys():
			if user_id != user:
				try:
					bot.send_message(user, f'{data[user_id]["Name"]} выбрал "{chose}"(Неполная смена)', reply_markup=button_)
				except Exception as e:
					print(f'{user} - {e}')

	if call.data == 'yes':
		chose = call.message.text.split('"')[1]
		data[user_id]['days'][f'{day[2]}.{day[1]}.{day[0]}'] = chose

		bot.edit_message_text(f'Отлично! Вы выбрали "{chose}"', call.message.chat.id, call.message.message_id)

		for user in data.keys():
			if user_id != user:
				try:
					bot.send_message(user, f'{days_[interval_][user_id]["Name"]} выбрал "{chose}"', reply_markup=button_)
				except Exception as e:
					print(f'{user} - {e}')

	if call.data == 'no':
		bot.edit_message_text(f'Выбери другой ответ', call.message.chat.id, call.message.message_id)

	post_json(data)

def start_bot():
	while True:
		try:
			bot.polling(non_stop=True, interval=0)
		except Exception as e:
			print(e)

def check_date():
	while True:
		now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime('%H:%M:%S')
		if now == time_reminder:
			employee_list = get_json()

			day = [str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).year), str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).day), str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).month)]

			for user in employee_list:
				try:
					print(employee_list[user]['days'].keys())
					if f'{day[2]}.{day[1]}.{day[0]}' not in employee_list[user]['days'].keys():
						bot.send_message(user, f'🕓Пора сделать выбор!', reply_markup=button_)
				except Exception as e:
					print(f'{user} - {e}')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	global user_add
	user_id = str(message.from_user.id)
	data = get_json()

	if user_id == admin_id:
		if message.text == '💼Новый сотрудник':
			user_add['status'] = 'id'
			bot.send_message(message.chat.id, 'Перешли мне любое сообщения нового сотрудника')
			return

		elif message.text == '👨‍💻Сотрудники':
			for employee in data:
				bot.send_message(message.chat.id,
					f"---{employee}---\n\n"
					f"Имя - {data[employee]['Name']}\n"
					f"Зарплата - {data[employee]['salary']}\n"
					f"Кол-во рабочих дней - {len(data[employee]['days'])}", reply_markup=button_delete_user
				)
			return

		if user_add['status'] == 'id' and (message.forward_from):
			user_add['data']['id'] = str(message.forward_from.id)
			user_add['status'] = 'name'
			bot.send_message(message.chat.id, 'Напиши мне его имя')
			return

		elif user_add['status'] == 'name':
			user_add['data']['name'] = message.text.strip()
			user_add['status'] = 'salary'
			bot.send_message(message.chat.id, 'Напиши мне его зарплату')
			return

		elif user_add['status'] == 'salary':
			user_add['data']['salary'] = int(message.text.strip())
			bot.send_message(message.chat.id,
				"Вы уверены в верности данных?\n\n"
				f"Имя - {user_add['data']['name']}\n"
				f"Зарплата - {user_add['data']['salary']}", reply_markup=button_confirm_user_add
				)
			return

	if user_id not in data.keys():
		bot.send_message(message.chat.id, 'Извини, ты не сотрудник (')
		return

	day = [str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).year), str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).day), str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).month)]

	if data[user_id]['prepayment_status'] == '1':
		if message.text.isdigit():
			data[user_id]["prepayment"] += int(message.text)
			bot.send_message(message.chat.id, f'Вы взяли аванс на {message.text}руб.\nВаш текущий аванс - {data[user_id]["prepayment"]}руб.', reply_markup=button_)
		else:
			bot.send_message(message.chat.id, 'Вы ввели не число!', reply_markup=button_)
		data[user_id]['prepayment_status'] = '0'
		post_json(data)

	if (message.text == '🛠️Саморез+' or message.text == '🛴Самокат+' or message.text == '🏠Выходной') and user_id in data.keys():
		if f'{day[2]}.{day[1]}.{day[0]}' not in data[user_id]['days'].keys():
			if  message.text != '🏠Выходной':
				bot.send_message(message.chat.id, f'Вы выбрали "{message.text}"\nВыберите какой рабочий день', reply_markup=button_choose)
			else:
				bot.send_message(message.chat.id, f'Вы выбрали "{message.text}"', reply_markup=button_confirm)
		else:
			bot.send_message(message.chat.id, f'Вы уже выбрали "{data[user_id]["days"][f"{day[2]}.{day[1]}.{day[0]}"]}"', reply_markup=button_)

	elif message.text == '💵Расчет💵':
		answer = calculation_money()

		bot.send_message(message.chat.id, answer, reply_markup=button_, parse_mode="Markdown")

	elif message.text == '💵Аванс💵':
		data[user_id]['prepayment_status'] = '1'
		bot.send_message(message.chat.id, 'Введите сумму аванса\nБез символов и точек, просто число!', reply_markup=types.ReplyKeyboardRemove())
		post_json(data)

if __name__ == '__main__':
	th_bot = Thread(target=start_bot)
	th_date = Thread(target=check_date)

	th_bot.start()
	th_date.start()
