# Generated by Django 4.0.2 on 2022-02-16 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_profile_created_alter_profile_profile_image_skill'),
        ('firstapp', '0004_tag_review_project_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Users.profile'),
        ),
    ]
