# Generated by Django 4.2 on 2025-01-30 05:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("wallets", "0002_remove_wallet_id_alter_wallet_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wallet",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                help_text="Уникальный идентификатор кошелька",
                primary_key=True,
                serialize=False,
                unique=True,
                verbose_name="UUID кошелька",
            ),
        ),
    ]
