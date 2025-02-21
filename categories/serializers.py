from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    deleted_at = serializers.DateTimeField(read_only=True, required=False, help_text="This field is automatically populated with the current date and time when the category is deleted.")
    class Meta:
        model = Category
        fields = '__all__'  # Or specify the fields you want to expose

    def validate_parent(self, value):
        if value == self.instance:  # prevent setting itself as parent
            raise serializers.ValidationError(
                "A category cannot be its own parent.")
        if self.instance and value:  # prevent changing parent to its own child
            if value == self.instance.parent:
                return value
            children = Category.objects.filter(parent=self.instance)
            if value in children:
                raise serializers.ValidationError(
                    "A category cannot have its child as its parent.")
        return value
