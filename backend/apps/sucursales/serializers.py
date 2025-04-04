from rest_framework import serializers
from .models import Branch, Table


class BranchSerializer(serializers.ModelSerializer):
    tables_count = serializers.SerializerMethodField()

    class Meta:
        model = Branch
        fields = ["id", "name", "address", "phone", "email", "is_active", "created_at", "updated_at", "tables_count"]
        read_only_fields = ["created_at", "updated_at"]

    def get_tables_count(self, obj):
        return obj.tables.count()


class TableSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source="branch.name", read_only=True)

    class Meta:
        model = Table
        fields = ["id", "branch", "branch_name", "number", "capacity", "status", "is_active"]
