# Generated by Django. Add the is_counted field to Sale model
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('cashDesk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='is_counted',
            field=models.BooleanField(default=False),
        ),
    ]

