# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime
import smtplib
import zipfile
import time
import requests

path = '/home/'
save_path='/mnt-backup/backups/'

now = time.time()
date = datetime.now().strftime("%d.%B.%Y %I:%M:%S %p")

#копирую дерево
shutil.copytree(path + 'test-host', save_path +str(date+"/"))

###### Создаю архим и скидываю туда все файлы ######
fantasy_zip = zipfile.ZipFile(save_path +str(date)+'.zip', 'w')
for folder, subfolders, files in os.walk(save_path+str(date)):
    for file in files:
            fantasy_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), save_path+str(date)), compress_type = zipfile.ZIP_DEFLATED)
fantasy_zip.close()
###### Удаляю каталог, оставив только архив ######
shutil.rmtree(save_path +str(date+"/"))

###### Удаление файлов старше 5 дней ######
for f in os.listdir(save_path):
    if os.stat(os.path.join(save_path,f)).st_mtime < now - 5 * 86400:
         os.remove(os.path.join(save_path, f))

###### Уведомления для Telegram ######
id = ['208428842','1266497665','134787881']
size = 'File size = '
int_size = (os.stat(os.path.join(save_path+str(date)+'.zip')).st_size) / 1048576
str_size = str(int_size)[:str(int_size).find('.')]
m = ' Мб'
for i in id:
    url = requests.post('https://api.telegram.org/bot1153858227:AAHPj_O2ziHpATV9Uwz8hlGRWppDpesqmjg/sendMessage?chat_id='+i+'&text=Backup for test-host completed! '+size+str_size+m)

###### Уведомление на Email ######
# Добавляем необходимые подклассы - MIME-типы
# from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
# from email.mime.text import MIMEText                # Текст/HTML
# from email.mime.image import MIMEImage              # Изображения

# addr_from = "RT-no-reply@yandex.ru"                 # Адресат
# addr_to   = "kolominivan4@gmail.com"                   # Получатель
# password  = "D6sMdC9dcWAvwm4c"                                  # Пароль

# msg = MIMEMultipart()                               # Создаем сообщение
# msg['From']    = addr_from                          # Адресат
# msg['To']      = addr_to                            # Получатель
# msg['Subject'] = 'BACKUP'                 # Тема сообщения

# body = 'Бекап готов, дата: '+date
# msg.attach(MIMEText(body, 'plain'))                 # Добавляем в сообщение текст

# server = smtplib.SMTP('smtp.yandex.ru', 25)        # Создаем объект SMTP
# # server.set_debuglevel(True)                         # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
# server.starttls()                                   # Начинаем шифрованный обмен по TLS
# server.login(addr_from, password)                   # Получаем доступ
# server.send_message(msg)
# server.quit()


