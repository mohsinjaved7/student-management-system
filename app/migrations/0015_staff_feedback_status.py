# Generated by Django 4.2.3 on 2023-07-25 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_student_feedback_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff_feedback',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]