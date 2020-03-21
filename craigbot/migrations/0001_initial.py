# Generated by Django 2.2.6 on 2019-12-17 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='craigBot',
            fields=[
                ('bot_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_found', models.BooleanField()),
                ('email_sent', models.BooleanField()),
                ('search_url', models.CharField(max_length=255)),
                ('price_min', models.IntegerField()),
                ('price_max', models.IntegerField()),
                ('search_query', models.CharField(max_length=255)),
                ('hyperlink_for_result_found', models.CharField(max_length=511)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='newBotRequest',
            fields=[
                ('req_id', models.AutoField(primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('search_query', models.CharField(max_length=255)),
                ('price_min', models.IntegerField()),
                ('price_max', models.IntegerField()),
                ('craig_bot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='craigbot.craigBot')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='craigbot',
            name='newBotReq',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='craigbot.newBotRequest'),
        ),
        migrations.AddField(
            model_name='craigbot',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
