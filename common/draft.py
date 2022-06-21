"""
http://mysite.com:8000/create?title=nature&url=https://bipbap.ru/wp-content/uploads/2017/04/priroda_kartinki_foto_03.jpg
http://mysite.com:8000/create?title=road_with_moon&url=https://vjoy.cc/wp-content/uploads/2020/09/bezymyannyjkvytstsk.jpgрр



from django.http import HttpResponseBadRequest
HttpResponseBadRequest() - не ошибка (не унаследован он BaseException)
поэтому просто вызывается без raise
посылает HTTP-response с кододм ответа 400 (bad request)




# Характеристики:
#
#  - оптимизировано для быстрого ввода-вывода.
#  - позволяет использовать различные структуры данных
#  - хранит данные в оперативной памяти, но можно настроить
#     копирование блоков данных на диски с определённой переодичностью
#     или при насуплении некоторого действия
#  - хорошо расширяется, довольно гибкий
#
# Поддерживает типы данных:
#
#  - строки
#  - хеши
#  - списки
#  - кортежи
#  - сортированные кортежи
#  - битовые карты
#  - HyperLogLogs
#
#
#
# SQL лучше подходит - долговременное хранения относительно постоянных данных
# Redis лучше подходит - часто изменяющейся информации или той, к которой
#                         необходимо иметь быстрый доступ (например к кешу)


# Консоль
# порт Redis - 6379
# Параллельно сервер Redis должен быть запущен в другой консоли
# установка и запуск Redis (если установлен, то приступай сразу к запуску)
# https://skillbox.ru/media/base/kak_ustanovit_redis_v_os_windows_bez_ispolzovaniya_docker/
#
#
# redis-cli
# 127.0.0.1:6379> EXPIRE name 2
# (integer) 1
# 127.0.0.1:6379> GET name
# (nil)
# 127.0.0.1:6379> GET total 1
# (error) ERR wrong number of arguments for 'get' command
# 127.0.0.1:6379> SET total 1
# OK
# 127.0.0.1:6379> GET total
# "1"
# 127.0.0.1:6379> DEL total
# (integer) 1
# 127.0.0.1:6379> GET total
# (nil)


"""

"""
from pprint import pprint as pp
from django.db import connection, reset_queries
reset_queries()
connection.queries
"""


from redis import StrictRedis, Redis

r = Redis('123',123,123)
r.zincrby
r.zrange()
