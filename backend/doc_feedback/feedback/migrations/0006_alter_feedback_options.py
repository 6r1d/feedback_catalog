# Generated by Django 4.1.5 on 2023-01-26 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("feedback", "0005_rename_feedbacktype_feedback_feedback_type"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="feedback",
            options={"ordering": ["id"], "verbose_name_plural": "Feedback"},
        ),
    ]
