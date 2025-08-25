import requests
import json


def find_user(email):
    res = requests.get('https://school1298.ru/portal/workers/workersPS-no.json')
    teacher_data = {}
    for i in res.json()['value']:
        if i['email'] == email:
            teacher_name = i['name']
            classes = i.get('classStr').split(',') if i.get('classStr') else []
            teacher_email = i['email']
            teacher_data = {'email': teacher_email,
                            'classes': classes,
                            'name': teacher_name}
            break
        else:
            pass
    return teacher_data
