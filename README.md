# T-shop
Test e-shop written with Django.

## Установка на Ubuntu 18.04
### Создаём нового пользователя, даём ему root-права и логинимся под ним
```
$ sudo adduser djangoadmin
$ sudo usermod -aG sudo djangoadmin
$ su djangoadmin
```
### Обновляем систему
```
$ sudo apt -y update
$ sudo apt -y upgrade
```
### Устанавливаем необходимые пакеты, git и веб-сервер
```
$ sudo apt -y install python3-pip python3-dev python3-venv git nginx
```
### Создадём виртуальной окружение и активируем его
```
$ cd
$ python3 -m venv ./venv
$ source venv/bin/activate
```
### Клонируем репозиторий
```
$ git clone https://github.com/saitaro/T-shop.git
```
### Заходим в директорию проекта и устанавливаем зависимости
```
$ cd T-shop
$ pip3 install -r requirements.txt 
```
### Создаём миграции и таблицы в базе данных
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```
### Собираем все статичные файлы в папку STATIC_ROOT
```
$ python3 manage.py collectstatic
```
### Запускаем сервер приложений, проверяем работоспособность сайта в браузере
```
$ gunicorn --bind 0.0.0.0:8000 tshop.wsgi
```
...затем останавливаем его и выходим из виртуального окружения
```
<Ctrl+C>
$ deactivate
```
### Создаём и настраиваем скрипт под unix-сокет gunicorn
```
$ sudo nano /etc/systemd/system/gunicorn.socket
```
Копируем в файл настройки:
```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```
### Создаём сервис systemd для gunicorn
```
sudo nano /etc/systemd/system/gunicorn.service
```
Копируем в файл настройки:
```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=djangoadmin
Group=www-data
WorkingDirectory=/home/djangoadmin/T-shop
ExecStart=/home/djangoadmin/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          tshop.wsgi:application

[Install]
WantedBy=multi-user.target
```
### Запускаем и подключаем скрипты сокета
```
$ sudo systemctl start gunicorn.socket
$ sudo systemctl enable gunicorn.socket
```
## Настройка nginx
### Создаём файл проекта
```
sudo nano /etc/nginx/sites-available/T-shop
```
И копируем в него конфигурацию:
```
server {
    listen 80;
    server_name <IP-адрес_сервера>;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/djangoadmin/T-shop;
    }
    
    location /media/ {
        root /home/djangoadmin/T-shop;    
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

### Создадим симлинк, чтобы nginx подключил проект
```
sudo ln -s /etc/nginx/sites-available/T-shop /etc/nginx/sites-enabled
```

### Проверяем корректность конфигурации nginx
```
sudo nginx -t

```

### Увеличим максимальный размер загрузки

Откроем файл конфигурации nginx

```
$ sudo nano /etc/nginx/nginx.conf
```

Добавим строку в раздел http

```
...
http {
        ...
        client_max_body_size 20M;
        ...
}
...
```

### Перезапускаем сервер

```
$ sudo systemctl restart nginx
```

### Добавляем адрес сервера в ALLOWED_HOSTS в настройках проекта

```
ALLOWED_HOSTS = ['ip-адрес_сервера']
```
### Перезапускаем nginx и Gunicorn

```
$ sudo systemctl restart nginx
$ sudo systemctl restart gunicorn
```