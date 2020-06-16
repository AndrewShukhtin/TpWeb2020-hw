# Generated by Django 3.0.7 on 2020-06-14 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='likeforquestion',
            name='like',
        ),
        migrations.RemoveField(
            model_name='likeforquestion',
            name='user',
        ),
        migrations.AddField(
            model_name='answer',
            name='likes_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='answer',
            name='photo',
            field=models.CharField(default='/img/me.jpg', max_length=120),
        ),
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.TextField(verbose_name='Поле ответа....'),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Заголовок вопроса'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Tag'),
        ),
        migrations.DeleteModel(
            name='LikeForAnswer',
        ),
        migrations.DeleteModel(
            name='LikeForQuestion',
        ),
    ]
