# Generated by Django 3.2.3 on 2023-02-19 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PersonID', models.CharField(default=0, max_length=3)),
                ('Timestamp', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(default='', max_length=25)),
                ('Email', models.CharField(default='', max_length=100)),
                ('Label', models.CharField(blank=True, default=-1, max_length=3, null=True)),
            ],
        ),
    ]