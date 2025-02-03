# Generated by Django 4.2 on 2025-02-01 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wallets", "0006_alter_operation_wallet"),
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
                related_name="operations",
                to="wallets.wallet",
                verbose_name="Кошелек",
            ),
        ),
    ]
