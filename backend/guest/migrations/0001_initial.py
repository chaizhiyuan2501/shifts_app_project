# Generated by Django 4.2.20 on 2025-03-25 03:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50, verbose_name='氏名')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生年月日')),
                ('contact', models.CharField(blank=True, max_length=100, verbose_name='連絡先')),
            ],
        ),
        migrations.CreateModel(
            name='VisitType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='コード')),
                ('name', models.CharField(max_length=50, verbose_name='表示名')),
                ('arrive_time', models.TimeField(verbose_name='来所時間')),
                ('leave_time', models.TimeField(verbose_name='帰宅時間')),
                ('color', models.CharField(default='#cccccc', max_length=10, verbose_name='色コード')),
            ],
        ),
        migrations.CreateModel(
            name='VisitSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日付')),
                ('note', models.TextField(blank=True, null=True, verbose_name='備考')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guest.guest', verbose_name='利用者')),
                ('visit_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='guest.visittype', verbose_name='来訪種別')),
            ],
            options={
                'ordering': ['date'],
                'unique_together': {('guest', 'date')},
            },
        ),
    ]
