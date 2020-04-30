# Generated by Django 3.0.2 on 2020-04-26 21:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20200426_1220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assessment_completion',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='assessment_completion',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='assessment_completion',
            name='is_graded',
        ),
        migrations.AddField(
            model_name='assessment_completion',
            name='student',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='student_assessment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='peer_assessment',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 26, 21, 22, 11, 375301)),
        ),
        migrations.CreateModel(
            name='Instructor_Assessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_graded', models.BooleanField(default=False)),
                ('grade', models.PositiveIntegerField(default=0)),
                ('comment', models.TextField(default='')),
                ('assessment_completion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructor_completion', to='accounts.Assessment_Completion')),
            ],
        ),
    ]