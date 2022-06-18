"""
http://mysite.com:8000/create?title=nature&url=https://bipbap.ru/wp-content/uploads/2017/04/priroda_kartinki_foto_03.jpg
http://mysite.com:8000/create?title=road_with_moon&url=https://vjoy.cc/wp-content/uploads/2020/09/bezymyannyjkvytstsk.jpgрр



from django.http import HttpResponseBadRequest
HttpResponseBadRequest() - не ошибка (не унаследован он BaseException)
поэтому просто вызывается без raise
посылает HTTP-response с кододм ответа 400 (bad request)
"""
# from django.contrib.auth.models import User
#
# User
