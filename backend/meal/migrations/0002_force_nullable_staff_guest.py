from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealorder',
            name='guest',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='guest.guest',
                null=True,
                blank=True,
                verbose_name='患者',
            ),
        ),
        migrations.AlterField(
            model_name='mealorder',
            name='staff',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='staff.staff',
                null=True,
                blank=True,
                verbose_name='スタッフ',
            ),
        ),
    ]
