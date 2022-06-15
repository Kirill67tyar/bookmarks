from django.contrib.auth.models import User

from images.utils import get_object_or_null


class EmailAuthBackend:

    # здесь интересный момент.
    # т.к. поле email в модели User по умолчанию не имеет параметр unique=True
    # две разных записи в таблице User могут иметь один и тот же email
    # (два пользователя один и тот же email)
    # И если мы используем user = User.objects.get(email=email)
    # то выдаст не модель User, а QS и вызовется ошибка MultipleObjectsReturned
    # если использовать  user = User.objects.filter(email=username).first()
    # то всё будет нормально
    # но он вернёт только первого пользователя, которого встретит
    # а это баг
    # вывод - для возможности аутентификации по email
    # нужно делать так, чтобы email имел параметр unique=True (был уникальным)
    def authenticate(self, request, **credentials):
        username = credentials.get('username', credentials.get('email'))
        # email = credentials.get('username', credentials.get('email')) #  если так, то будет ошибка
        password = credentials.get('password')
        try:
            # user = User.objects.get(email=username)
            user = get_object_or_null(User, email=username)
            if user:
                if user.check_password(password):
                    return user
            return None

        except User.DoesNotExist:
            return None

    # def authenticate(self, request, username=None, password=None):
    #     user = User.objects.filter(email=username).first()
    #     if user:
    #         if not user.check_password(password):
    #             return None
    #     return user

    def get_user(self, user_id):
        return get_object_or_null(User, pk=user_id)
