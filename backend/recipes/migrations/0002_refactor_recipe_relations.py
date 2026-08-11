from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient_name_unit',
            ),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='%(class)s_relations',
                to='recipes.recipe',
                verbose_name='Рецепт',
            ),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='%(class)s_relations',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Пользователь',
            ),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='%(class)s_relations',
                to='recipes.recipe',
                verbose_name='Рецепт',
            ),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='%(class)s_relations',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Пользователь',
            ),
        ),
    ]
