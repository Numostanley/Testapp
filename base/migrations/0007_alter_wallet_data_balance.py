# Generated by Django 4.0.1 on 2022-02-13 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_datatransactions_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='Data_balance',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
