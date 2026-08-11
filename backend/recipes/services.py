from django.db.models import Sum

from .models import RecipeIngredient


def build_shopping_list(user):
    ingredients = (
        RecipeIngredient.objects.filter(
            recipe__shoppingcart_relations__user=user,
        )
        .values(
            'ingredient__name',
            'ingredient__measurement_unit',
        )
        .annotate(total_amount=Sum('amount'))
        .order_by('ingredient__name')
    )
    lines = ['Список покупок', '']
    lines.extend(
        (
            f"{item['ingredient__name']} "
            f"({item['ingredient__measurement_unit']}) — "
            f"{item['total_amount']}"
        )
        for item in ingredients
    )
    return '\n'.join(lines)
