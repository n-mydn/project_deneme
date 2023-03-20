# Generated by Django 4.1.1 on 2023-01-31 17:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('feedback', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Admin', 'Admin'), ('Hastane Admini', 'Hastane Admini'), ('Departman Admini', 'Departman Admini'), ('Departman Kullanıcısı', 'Departman Kullanıcısı'), ('Personel', 'Personel'), ('Hasta', 'Hasta')], max_length=21, verbose_name='user_roles')),
            ],
        ),
        migrations.CreateModel(
            name='UserAddProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='user_phone')),
                ('user_adress', models.TextField(max_length=100, verbose_name='user_adress')),
                ('user_status', models.BooleanField(choices=[('Aktif', 'Aktif'), ('Pasif', 'Pasif')], verbose_name='user_status')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.city', verbose_name='user_city')),
                ('user_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.company', verbose_name='user_company')),
                ('user_country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.country', verbose_name='user_country')),
                ('user_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.department', verbose_name='user_department')),
                ('user_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userroles', verbose_name='user_role')),
            ],
        ),
    ]
