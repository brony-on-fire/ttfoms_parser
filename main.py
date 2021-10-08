#/usr/bin/env python3

import requests

from time import time

#Функция проверки номера полиса ОМС
def get_oms_code(oms_code):
	params = (
		('render', '1'),
	)

	data = {
	  'PolicyForm[series]': '',
	  'PolicyForm[number]': oms_code,
	  'PolicyForm[enp]': ''
	}

	response = requests.post('https://www.ttfoms.tomsk.ru/search/policyajax', params=params, data=data).text

	if 'Действует' in response:
		return 'Действует'
	elif 'Не действует' in response:
		return 'Аннулирован'
	elif 'полис не найден' in response:
		return 'Не найден'
	else:
		return 'Неизвестный ответ'

#Запрашиваем имя файла со списком
my_file = input('Введите имя файла со списком: ')
start_time = time()

#Считываем элементы с файла в список
with open(f'{my_file}.csv', 'r') as f:
    file_list = f.read().splitlines()

list_of_code = []
for i in file_list:
    if i[-1] != '-':
        new_element = i.split(';')
        list_of_code.append(new_element)

#Основной цикл проверки полисов ОМС
for i, code in list_of_code:
    document_status = get_oms_code(code)
    if document_status != "Действует":
        protocol = open(f'protocol_{my_file}.csv', 'a')
        protocol.write(f"{i} - {code} - {document_status}\n")
        protocol.close()
    timer_now = round(time()-start_time)
    print(f'{i}. {code} - {document_status}. Время прошло: {timer_now} секунд')
