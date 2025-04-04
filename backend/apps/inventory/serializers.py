from rest_framework import serializers
from .models import Category, Product, Inventory, InventoryTransaction


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "description", "is_active", "products_count"]

    def get_products_count(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "category",
            "category_name",
            "image",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    branch_name = serializers.CharField(source="branch.name", read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Inventory
        fields = [
            "id",
            "branch",
            "branch_name",
            "product",
            "product_name",
            "quantity",
            "last_updated",
            "alert_threshold",
            "is_low_stock",
        ]
        read_only_fields = ["last_updated"]


class InventoryTransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="inventory.product.name", read_only=True)
    branch_name = serializers.CharField(source="inventory.branch.name", read_only=True)
    created_by_name = serializers.CharField(source="created_by.get_full_name", read_only=True)

    class Meta:
        model = InventoryTransaction
        fields = [
            "id",
            "inventory",
            "product_name",
            "branch_name",
            "quantity",
            "transaction_type",
            "transaction_date",
            "reference",
            "notes",
            "created_by",
            "created_by_name",
        ]
        read_only_fields = ["transaction_date"]
