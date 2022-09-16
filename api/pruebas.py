from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
payload = {'fecha':'2022-05-10','hora':'00:00'}
fecha_inicio = datetime.combine(datetime.strptime(payload["fecha"], "%Y-%m-%d"), (datetime.strptime(payload["hora"], "%H:%M")).time())

html_text = requests.post('http://127.0.0.1:30036/hour', data=payload)
soup = BeautifulSoup(html_text.text, 'lxml')
fecha = soup.find('input', id='fechashow').get('value')
predvalue = soup.find('input', id='predvalue').get('value')
realvalue = soup.find('input', id='realvalue').get('value')
prediccion_hora_json = {"fecha": fecha_inicio.isoformat(), "real":realvalue, "prediccion": predvalue}
print(prediccion_hora_json)


html_text_day = requests.post('http://127.0.0.1:30036/day', data=payload)
soup_day = BeautifulSoup(html_text_day.text, 'lxml')
tabla_datos = soup_day.find('tbody')
conjunto_datos = tabla_datos.find_all('td')
array_datos_horas = []
fecha_aux = fecha_inicio
for i,k in zip(conjunto_datos[0::2], conjunto_datos[1::2]):
    array_datos_horas.append({"real":i.text, "prediccion": k.text, "fecha": fecha_aux.isoformat()})
    fecha_aux = fecha_aux + timedelta(hours=1)

print(array_datos_horas)


html_text_semana = requests.post('http://127.0.0.1:30036/week', data=payload)
soup_week = BeautifulSoup(html_text_semana.text, 'lxml')
tabla_datos_week = soup_week.find('tbody')
conjunto_datos_week = tabla_datos_week.find_all('td')
array_datos_semana = []
fecha_aux_semana = fecha_inicio
for i,k in zip(conjunto_datos_week[0::2], conjunto_datos_week[1::2]):
    array_datos_semana.append({"real":i.text, "prediccion": k.text, "fecha": fecha_aux_semana.isoformat()})
    fecha_aux_semana = fecha_aux_semana + timedelta(hours=1)
print(array_datos_semana)
