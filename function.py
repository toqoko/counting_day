import json
import datetime

import requests

from config import interval_list




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

def check_date(interval, days_):
	user_money = {
		'🛴Самокат+(Полная смена)': 0,
		'🛠️Саморез+(Полная смена)': 0,
		'🛴Самокат+(Неполная смена)': 0,
		'🛠️Саморез+(Неполная смена)': 0,
		'🏠Выходной': 0
	}

	for d in days_:
		day_data = d.split('.')
		y_day = int(day_data[2])
		d_day = int(day_data[1])
		m_day = int(day_data[0])

		first_ = interval.split('-')[0].split('.')
		y_first = int(first_[0])
		d_first = int(first_[1])
		m_first = int(first_[2])

		second_ = interval.split('-')[1].split('.')
		y_second = int(second_[0])
		d_second = int(second_[1])
		m_second = int(second_[2])


		if datetime.date(y_first, m_first, d_first) <= datetime.date(y_day, m_day, d_day) <= datetime.date(y_second, m_second, d_second):
			user_money[days_[d]] += 1

	return user_money

def calculation_money():
	data = get_json()

	d = get_interval([str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).year), str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).day), str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).month)], interval_list)		

	print(d)
	message = f'*Расчёт на {d}\n\n*'
	for user in data:
		user_money = check_date(d, data[user]['days'])
		money = 0
		
		for day in user_money:
			if '(Полная смена)' in day:
				money += user_money[day] * data[user]['salary']
			elif '(Неполная смена)' in day:
				money += user_money[day] * (data[user]['salary'] / 2)
			
		message = message + (
			f'*{data[user]["Name"]}:*\n'
			'🛠️Саморез:\n'
			f'-_Полный_-{user_money["🛠️Саморез+(Полная смена)"]}\n'
			f'-_Неполный_-{user_money["🛠️Саморез+(Неполная смена)"]}\n'
			'🛴Самокат:\n'
			f'-_Полный_-{user_money["🛴Самокат+(Полная смена)"]}\n'
			f'-_Неполный_-{user_money["🛴Самокат+(Неполная смена)"]}\n'
			f'🏠Выходной-{user_money["🏠Выходной"]}\n\n'
			f'*Заработано > {int(money)}₽*\n'
			f'*Аванс >> {int(data[user]["prepayment"])}₽*\n'
			f'*Заработано с учетом аванса >>> {int(money - data[user]["prepayment"])}₽*\n\n\n'
		)
	return message

def get_json():
	r = requests.get('https://json.extendsclass.com/bin/7e751a1f2dd0', headers={
			'Security-key': 'couting'
		})
	return json.loads(r.text)

def post_json(data):
	r = requests.put('https://json.extendsclass.com/bin/7e751a1f2dd0', headers={
		'Security-key': 'couting',
	}, data=str(data).replace("'", '"').encode("utf-8"))

def add_employee(data):
	json_ = get_json()

	json_[data['id']] = {
		'Name': data['name'],
		'salary': data['salary'],
		'prepayment': 0,
		'prepayment_status': '0',
		'days': {}
	}

	post_json(json_)

if __name__ == '__main__':
	print(get_json())
	# add_employee({
	# 	'id': '5797115474',
	# 	'name': 'Daniil',
	# 	'salary': 1000
	# 	})

	# print(calculation_money())