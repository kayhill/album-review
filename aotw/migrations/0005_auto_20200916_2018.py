# Generated by Django 3.1 on 2020-09-16 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aotw', '0004_auto_20200916_1924'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='audioDB_albumID',
            new_name='idAlbum',
        ),
        migrations.RenameField(
            model_name='album',
            old_name='audioDB_artistID',
            new_name='idArtist',
        ),
        migrations.RenameField(
            model_name='album',
            old_name='year',
            new_name='intYearReleased',
        ),
        migrations.RenameField(
            model_name='album',
            old_name='title',
            new_name='strAlbum',
        ),
        migrations.RenameField(
            model_name='album',
            old_name='album_art',
            new_name='strAlbumThumb',
        ),
        migrations.RenameField(
            model_name='album',
            old_name='artist',
            new_name='strArtist',
        ),
        migrations.RenameField(
            model_name='album',
            old_name='description',
            new_name='strDescriptionEN',
        ),
        migrations.RenameField(
            model_name='album',
            old_name='genre',
            new_name='strGenre',
        ),
        migrations.RenameField(
            model_name='album',
            old_name='label',
            new_name='strLabel',
        ),
        migrations.AddField(
            model_name='album',
            name='custom',
            field=models.BooleanField(default=False),
        ),
    ]
