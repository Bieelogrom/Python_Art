# Generated by Django 5.1.4 on 2025-01-16 02:57

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_posts_data_publicacao"),
    ]

    operations = [
        migrations.CreateModel(
            name="PostagensSalvas",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "horario_salvo",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "id_postagem_salva",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.posts"
                    ),
                ),
                (
                    "id_usuario_que_salvou",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
