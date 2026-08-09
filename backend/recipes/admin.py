from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ('ingredient',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'favorite_count')
    search_fields = ('name', 'author__username', 'author__email')
    list_filter = ('tags',)
    autocomplete_fields = ('author',)
    filter_horizontal = ('tags',)
    readonly_fields = ('favorite_count',)
    inlines = (RecipeIngredientInline,)

    @admin.display(description='Добавлений в избранное')
    def favorite_count(self, obj):
        if obj.pk is None:
            return 0
        return obj.favorited_by.count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', 'created_at')
    search_fields = ('user__username', 'recipe__name')
    autocomplete_fields = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', 'created_at')
    search_fields = ('user__username', 'recipe__name')
    autocomplete_fields = ('user', 'recipe')
