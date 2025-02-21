from celery import shared_task
import json
from products.models import Category, Product
from django.utils import timezone
import os
@shared_task
def process_json_upload(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

            categories_data = data.get('categories', [])
            products_data = data.get('products', [])

            # Create or update categories
            for category_data in categories_data:
                category, created = Category.objects.update_or_create(
                    id=category_data['id'],
                    defaults={
                        'category_name': category_data['category_name'],
                        'description': category_data['description'],
                        'created_at': category_data.get('created_at'),
                        'updated_at': category_data.get('updated_at'),
                    }
                )

            # Create or update products
            for product_data in products_data:
                category_id = product_data['category_id']
                try:
                    category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    print(f"Category with ID {category_id} not found. Skipping product.")
                    continue  # Skip to the next product

                product, created = Product.objects.update_or_create(
                    id=product_data['id'],
                    defaults={
                        'category': category,
                        'product_name': product_data['product_name'],
                        'product_description': product_data['product_description'],
                        'product_price': product_data['product_price'],
                        'currency': product_data['currency'],
                        'stock_quantity': product_data['stock_quantity'],
                        'sku': product_data['sku'],
                        'image_url': product_data['image_url'],
                        'created_at': product_data.get('created_at'),
                        'updated_at': product_data.get('updated_at'),
                    }
                )
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error processing JSON file: {e}")
        # Handle the error appropriately, e.g., log it, send a notification, etc.
    finally:
        os.remove(file_path) # Clean up the uploaded file after processing