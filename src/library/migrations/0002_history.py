# Generated by Django 4.2.2 on 2023-06-13 14:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reserved_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('reserved_to', models.DateTimeField(blank=True, null=True)),
                ('overdue', models.BooleanField(default=False)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.book')),
                ('reader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.reader')),
            ],
        ),
    ]
