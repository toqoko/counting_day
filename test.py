import json
import datetime

import telebot
import requests

answer = {
	'Александр': {
		'🛠️Саморез+': 0,
		'🛴Самокат+': 0,
		'🏠Выходной': 0
	},
	'Андрей': {
		'🛠️Саморез+': 0,
		'🛴Самокат+': 0,
		'🏠Выходной': 0
	}
}


# Получения интервала
def get_interval(day, days_):
	for d in days_:
		y_day = int(day[0])
		d_day = int(day[1])
		m_day = int(day[2])

		first_ = d.split('-')[0].split('.')
		y_first = int(first_[0])
		d_first = int(first_[1])
		m_first = int(first_[2])

		second_ = d.split('-')[1].split('.')
		y_second = int(second_[0])
		d_second = int(second_[1])
		m_second = int(second_[2])


		if datetime.date(y_first, m_first, d_first) <= datetime.date(y_day, m_day, d_day) <= datetime.date(y_second, m_second, d_second):
			return d



r = requests.get('https://json.extendsclass.com/bin/7e751a1f2dd0', headers={
		'Security-key': 'couting'
	})

days_ = json.loads(r.text)
bot_token = '5641281628:AAG7Wv1YU-wzXH5ondK2q1zMRaAjZnuQ_iA'
bot = telebot.TeleBot(bot_token)

day = ['2022', '11', '12']
print(day)
interval_ = get_interval(day, days_)



for d in days_[interval_]['1053756513']['day']:
	answer['Александр'][days_[interval_]['1053756513']['day'][d]] += 1

for d2 in days_[interval_]['1025194570']['day']:
	answer['Андрей'][days_[interval_]['1025194570']['day'][d2]] += 1

bot.send_message('1829352344', 
	f'*Расчёт на {interval_}*\n\n'
	f'_Александр_:\n'
	f'  🛠️Саморез - {answer["Александр"]["🛠️Саморез+"]}\n'
	f'  🛴Самокат - {answer["Александр"]["🛴Самокат+"]}\n'
	f'  🏠Выходной - {answer["Александр"]["🏠Выходной"]}\n\n'
	f'_Андрей_:\n'
	f'  🛠️Саморез - {answer["Андрей"]["🛠️Саморез+"]}\n'
	f'  🛴Самокат - {answer["Андрей"]["🛴Самокат+"]}\n'
	f'  🏠Выходной - {answer["Андрей"]["🏠Выходной"]}\n\n'
, parse_mode="Markdown")