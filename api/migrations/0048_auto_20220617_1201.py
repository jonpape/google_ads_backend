# Generated by Django 3.2.4 on 2022-06-17 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_editkeywordthemes_mytoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='editadschedule',
            name='mytoken',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='editgeotargets',
            name='mytoken',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]