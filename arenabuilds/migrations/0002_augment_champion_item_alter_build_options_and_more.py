# Generated by Django 5.1.7 on 2025-04-02 11:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arenabuilds', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Augment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='augments/')),
            ],
        ),
        migrations.CreateModel(
            name='Champion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='champions/')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='items/')),
            ],
        ),
        migrations.AlterModelOptions(
            name='build',
            options={},
        ),
        migrations.RemoveField(
            model_name='build',
            name='augments',
        ),
        migrations.AlterField(
            model_name='build',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='build',
            name='items',
        ),
        migrations.CreateModel(
            name='BuildAugment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('augment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arenabuilds.augment')),
                ('build', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arenabuilds.build')),
            ],
        ),
        migrations.AlterField(
            model_name='build',
            name='champion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arenabuilds.champion'),
        ),
        migrations.CreateModel(
            name='BuildItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('build', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arenabuilds.build')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arenabuilds.item')),
            ],
        ),
        migrations.AddField(
            model_name='build',
            name='augments',
            field=models.ManyToManyField(through='arenabuilds.BuildAugment', to='arenabuilds.augment'),
        ),
        migrations.AddField(
            model_name='build',
            name='items',
            field=models.ManyToManyField(through='arenabuilds.BuildItem', to='arenabuilds.item'),
        ),
    ]
