# Generated by Django 4.2.3 on 2023-09-25 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_app', '0014_remove_siteuser_github_remove_siteuser_instagram_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannedUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=110, verbose_name='Banlanma sebebi')),
                ('createdAt', models.DateTimeField(auto_now=True)),
                ('updatedAt', models.DateTimeField(auto_now_add=True)),
                ('authorized', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='yetkili', to=settings.AUTH_USER_MODEL, verbose_name='Banlayan')),
                ('suspect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Banlanan')),
            ],
        ),
        migrations.AddField(
            model_name='siteuser',
            name='banRecord',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='site_app.bannedusers', verbose_name='Ban Kaydi'),
        ),
    ]
