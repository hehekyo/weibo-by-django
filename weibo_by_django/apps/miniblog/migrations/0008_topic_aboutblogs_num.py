# Generated by Django 2.1.3 on 2019-01-14 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniblog', '0007_miniblog_has_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='aboutblogs_num',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='相关微博数'),
        ),
    ]
