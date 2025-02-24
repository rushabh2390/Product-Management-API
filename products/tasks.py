from celery import shared_task
import json
from products.models import Category, Product
from categories.serializers import CategorySerializer
from django.utils import timezone
import os


@shared_task
def process_json_upload(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

            categories_data = data.get('Category', [])
            products_data = data.get('Product', [])
            print(categories_data, products_data)
            # Create or update categories
            category_entry = []
            for category_data in categories_data:

                category_entry.append(Category(
                    category_name= category_data['category_name'],
                    description=category_data['description'],
                    created_at=category_data.get('created_at'),
                    updated_at=category_data.get('updated_at'),
                ))
          
            Category.objects.bulk_create(category_entry)
            # Create or update products
            products_entry = []
            for product_data in products_data:
                category_name = product_data['category']
                try:
                    category = Category.objects.get(
                        category_name=category_name)
                except Category.DoesNotExist:
                    category = Category.objects.create({
                        'category_name': category_name}
                    )
                products_entry.append(
                    Product(
                        category=category,
                        product_name=product_data['product_name'],
                        product_description=product_data['product_description'],
                        product_price=product_data['product_price'],
                        currency=product_data['currency'],
                        stock_quantity=product_data['stock_quantity'],
                        sku=product_data['sku'],
                        image_url=product_data['image_url'],
                        created_at=product_data.get('created_at'),
                        updated_at=product_data.get('updated_at'),
                    )
                )
            
            Product.objects.bulk_create(products_entry)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error processing JSON file: {e}")
        # Handle the error appropriately, e.g., log it, send a notification, etc.
    finally:
        os.remove(file_path)  # Clean up the uploaded file after processing
