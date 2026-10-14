from django.contrib import admin
from .models import Inventario, Libro, Orden


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
	list_display = ("id", "titulo", "precio")
	search_fields = ("titulo",)


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
	list_display = ("id", "libro", "cantidad")
	search_fields = ("libro__titulo",)


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
	list_display = ("id", "libro", "total", "fecha_creacion")
	list_filter = ("fecha_creacion",)
