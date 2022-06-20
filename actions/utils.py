from datetime import timedelta, datetime

from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from actions.models import Action


def create_action(user, verb, target=None) -> True | False:
    last_minute = timezone.now() - timedelta(seconds=60)
    # сравниваем, что не actions сделаных менее минуты назад
    similar_actions = Action.objects.filter(
        user=user,
        verb=verb,
        created__gte=last_minute
    )
    if target:
        # получаем contenttype для модели
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions.filter(
            target_ct=target_ct,
            target_id=target.pk
        )
    if not similar_actions:
        action = Action(
            user=user,
            verb=verb,
            target=target,
        )
        action.save()
        return True
    return False
