# Generated by Django 2.1.3 on 2018-11-25 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(db_index=True, max_length=150)),
                ('ident', models.IntegerField(db_index=True, max_length=255)),
            ],
        ),
    ]
