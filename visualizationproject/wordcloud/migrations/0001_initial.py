# Generated by Django 4.2 on 2023-05-04 13:18

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.CharField(editable=False, max_length=32, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Trending',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wordcloud.category')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.CharField(editable=False, max_length=32, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('thumbnail', models.URLField()),
                ('url', models.URLField()),
                ('count_of_views', models.PositiveBigIntegerField(default=0)),
                ('count_of_comments', models.PositiveBigIntegerField(default=0)),
                ('categories', models.ManyToManyField(through='wordcloud.Trending', to='wordcloud.category')),
            ],
        ),
        migrations.AddField(
            model_name='trending',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wordcloud.video'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(blank=True, null=True)),
                ('video', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wordcloud.video')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='videos',
            field=models.ManyToManyField(through='wordcloud.Trending', to='wordcloud.video'),
        ),
    ]