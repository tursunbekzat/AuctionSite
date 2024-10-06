from django.core.management.base import BaseCommand
from core.models import Category
import random

class Command(BaseCommand):
    help = 'Create fake categories'

    def handle(self, *args, **kwargs):
        categories_list = [
            "Electronics",
            "Fashion",
            "Home & Garden",
            "Sports & Outdoors",
            "Toys & Hobbies",
            "Health & Beauty",
            "Automotive",
            "Books",
            "Jewelry",
            "Collectibles"
        ]
        
        for category_name in categories_list:
            category_slug = category_name.lower().replace(" ", "-")  # Генерируем slug
            Category.objects.create(name=category_name, slug=category_slug)
            self.stdout.write(self.style.SUCCESS(f'Category "{category_name}" created!'))
