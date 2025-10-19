# Generated manually to fix JSON field validation issue

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_auto_20251019_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='authors',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='categories',
            field=models.TextField(blank=True, null=True),
        ),
    ]
