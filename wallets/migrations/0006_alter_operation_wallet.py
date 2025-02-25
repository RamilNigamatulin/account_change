# Generated by Django 4.2 on 2025-01-31 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wallets", "0005_alter_wallet_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="operation",
            name="wallet",
            field=models.ForeignKey(
                blank=True,
                help_text="Введите кошелек",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="wallets.wallet",
                verbose_name="Кошелек",
            ),
        ),
    ]
