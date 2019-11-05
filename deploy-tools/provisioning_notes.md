Обеспечение работы нового сайта
================================
## необходимые пакеты:
* nginx
* Python 3.6
* virtualenv + pip
* Git


например, в Ubuntu
	
	sudo apt-get install nginx git python36 python3.6-venv

## Конфигурация виртуального узла Nginx

* см. nginx.template.conf
* заменить SITENAME, например, на staging.my-domian.com

## служба Systemd 

* см. gunicorn-systemd.template.service
* заменить SITENAME, например, на staging.my-domian.com

## Структура папок:
Если допустить, что есть учетная запись пользователя в /home/username

/home/username
	sites
		SITENAME
			database
			source
			static
			virtualenv