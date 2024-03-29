# Generated by Django 4.0.5 on 2022-06-18 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribed_to', to=settings.AUTH_USER_MODEL, verbose_name='Подписка от')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_subscribed', to=settings.AUTH_USER_MODEL, verbose_name='Подписка на')),
            ],
            options={
                'verbose_name': 'Промежуточная таблица - контакте',
                'ordering': ('-created',),
            },
        ),
    ]
