# Generated by Django 3.1.4 on 2020-12-14 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Message')),
                ('from_address', models.EmailField(default='gctdljgkjnm@mail.ru', max_length=155, verbose_name='From email')),
                ('to_address', models.EmailField(max_length=155, verbose_name='To email')),
                ('status', models.CharField(choices=[('waiting to send', 'Waiting to send'), ('sended', 'Sended')], default='waiting to send', max_length=15)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('send_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('send_timeout', models.IntegerField(default=0)),
            ],
        ),
    ]
