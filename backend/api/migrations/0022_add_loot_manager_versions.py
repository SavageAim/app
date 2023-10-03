# Generated by Django 3.2.19 on 2023-07-27 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_team_member_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='loot_manager_version',
            field=models.CharField(choices=[('item', 'item'), ('fight', 'fight')], default='item', max_length=10),
        ),
    ]
