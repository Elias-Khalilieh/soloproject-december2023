# Generated by Django 2.2.4 on 2023-12-21 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='message',
        ),
        migrations.AddField(
            model_name='comment',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='event_comments', to='football_app.Event'),
            preserve_default=False,
        ),
    ]