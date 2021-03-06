# Generated by Django 2.2.8 on 2019-12-16 20:46

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='csUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('lang', models.CharField(choices=[('ru', 'Русский'), ('en', 'Английский')], default='ru', max_length=10, verbose_name='Язык интерфейса')),
                ('user_info', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('avatar', models.ImageField(blank=True, default='./user/logo/default.png', max_length=127, null=True, upload_to='user\\logo', verbose_name='Фото профиля')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('release_year', models.IntegerField(choices=[(1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019)], default=2019, verbose_name='Год выпуска')),
                ('append_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')),
                ('is_single_color', models.BooleanField(default=True, verbose_name='Заводская окраска?')),
                ('with_graffity', models.BooleanField(default=False, verbose_name='Граффити?')),
                ('is_pumped', models.BooleanField(default=False, verbose_name='Прокачана?')),
                ('params', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='Характеристики')),
                ('desc', models.CharField(max_length=30, verbose_name='Дополнительное описание')),
                ('base_rate', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Базовая цена аренды, за 1 час')),
                ('give_to_rent', models.BooleanField(default=False, verbose_name='Сдавать в аренду ?')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to=settings.AUTH_USER_MODEL, verbose_name='Собственник')),
            ],
            options={
                'verbose_name': 'Авто',
                'verbose_name_plural': 'Авто',
            },
        ),
        migrations.CreateModel(
            name='RentEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('duration', models.DurationField(verbose_name='Продолжительность аренды')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InteriorGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='./car/interior/default.jpg', max_length=127, upload_to='car\\interior', verbose_name='Фото авто(интерьер)')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interior_images', to='core.Car')),
            ],
        ),
        migrations.CreateModel(
            name='ExteriorGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='./car/exterior/default.jpg', max_length=127, upload_to='car\\exterior', verbose_name='Фото авто(экстерьер)')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exterior_images', to='core.Car')),
            ],
        ),
    ]
