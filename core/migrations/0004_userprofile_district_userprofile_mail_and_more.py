# Generated by Django 5.1.7 on 2025-04-29 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_userprofile_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='district',
            field=models.CharField(default='unknown', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mail',
            field=models.EmailField(default='Unknown', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='user_photos/'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='state',
            field=models.CharField(default='Unknown', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='full_name',
            field=models.CharField(max_length=100),
        ),
    ]
