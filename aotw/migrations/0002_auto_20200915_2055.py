# Generated by Django 3.1 on 2020-09-15 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aotw', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='score',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='album',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='aotw.album'),
        ),
    ]
