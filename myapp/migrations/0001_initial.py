# Generated by Django 3.2 on 2022-01-13 12:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='uploads/item', verbose_name='商品画像')),
                ('name', models.CharField(max_length=30)),
                ('category', models.CharField(choices=[('novel', '文学/小説'), ('society', '人文/社会'), ('culture', 'ノンフィクション/教養'), ('travel', '地図/旅行ガイド'), ('economy', 'ビジネス/経済'), ('health', '健康/医学'), ('IT', 'コンピュータ/IT'), ('hobby', '趣味/スポーツ/実用'), ('life', '住まい/暮らし/子育て'), ('art', 'アート/エンタメ'), ('foreign', '洋書'), ('picture', '絵本'), ('study', '参考書'), ('other', 'その他')], max_length=30)),
                ('quality', models.CharField(choices=[('new', '新品/未使用'), ('no_damaged', '目立った傷や汚れなし'), ('little_damaged', 'やや傷や汚れあり'), ('damaged', '傷や汚れあり'), ('bad', '全体的に状態が悪い')], max_length=20)),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999999)])),
                ('detail', models.TextField(max_length=5000)),
                ('sell_time', models.DateTimeField(auto_now_add=True)),
                ('give_time', models.DateTimeField(blank=True, null=True)),
                ('is_purchased', models.BooleanField(blank=True, default=False)),
                ('is_settle', models.BooleanField(blank=True, default=False)),
                ('is_given', models.BooleanField(blank=True, default=False)),
                ('is_got', models.BooleanField(blank=True, default=False)),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Item',
            },
        ),
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('talk', models.CharField(max_length=500)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('talk_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='talk_from', to=settings.AUTH_USER_MODEL)),
                ('talk_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='talk_item', to='myapp.item')),
                ('talk_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='talk_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Talk',
            },
        ),
        migrations.CreateModel(
            name='Nortify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('nortify', models.CharField(blank=True, max_length=100, null=True)),
                ('is_checked', models.BooleanField(default=False)),
                ('friend', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='talk_with', to=settings.AUTH_USER_MODEL)),
                ('nortify_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nortify_item', to='myapp.item')),
                ('notice_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notice_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Nortify',
            },
        ),
    ]
