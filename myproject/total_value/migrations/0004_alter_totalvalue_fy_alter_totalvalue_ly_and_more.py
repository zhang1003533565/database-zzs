# Generated by Django 5.2 on 2025-04-12 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('total_value', '0003_alter_totalvalue_jhpt_delete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='totalvalue',
            name='fy',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='副业'),
        ),
        migrations.AlterField(
            model_name='totalvalue',
            name='ly',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='林业'),
        ),
        migrations.AlterField(
            model_name='totalvalue',
            name='my',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='牧业'),
        ),
        migrations.AlterField(
            model_name='totalvalue',
            name='nyzcz',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='农业总产值'),
        ),
        migrations.AlterField(
            model_name='totalvalue',
            name='yy',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='渔业'),
        ),
        migrations.AlterField(
            model_name='totalvalue',
            name='zzy',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='种植业'),
        ),
    ]
