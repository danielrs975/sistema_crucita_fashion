# Generated by Django 2.1.4 on 2019-01-04 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_auto_20190103_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='grupo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]
