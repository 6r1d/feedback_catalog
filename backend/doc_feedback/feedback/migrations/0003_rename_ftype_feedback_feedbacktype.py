# Generated by Django 4.1.5 on 2023-01-04 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("feedback", "0002_alter_feedback_options_feedback_url"),
    ]

    operations = [
        migrations.RenameField(
            model_name="feedback",
            old_name="ftype",
            new_name="feedbackType",
        ),
    ]
