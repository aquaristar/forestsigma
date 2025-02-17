# Generated by Django 3.1.4 on 2020-12-09 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testroom', '0003_auto_20201208_0832'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='value',
            new_name='item_result',
        ),
        migrations.AddField(
            model_name='test',
            name='scale_result',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='test',
            name='subscale_result',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='testitem',
            unique_together={('test_id', 'item_id')},
        ),
    ]
