# Generated by Django 4.1.1 on 2023-02-15 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0008_feedbackdepartment_iddepartment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackdepartment',
            name='IdFeedbackUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.feedbackuser', verbose_name='f_id'),
        ),
    ]
