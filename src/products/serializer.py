from rest_framework import serializers
from typing import Callable
from .models import Tag, Product, ProductMedia

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class ProductMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductMedia
        fields = ['id', 'data']
        read_only_fields = ['id']
        

class ProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    media = ProductMediaSerializer(many=True)
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'tags', 'media', 'created_at', 'is_available', 'created_by']
        read_only_fields = ['id', 'created_at', 'is_available', 'created_by']
    
    def use_product_media_method(self, *args, media_data:list[dict], product, media_method:Callable) -> None:
        for media in media_data:
                media_data = {key: media[key] for key in args}
                media_method(product=product, **media_data)

    def get_or_create_tags(self, tags_data):
        return [Tag.objects.get_or_create(**tag)[0] for tag in tags_data]

    def create(self, validated_data:dict):
        request = self.context.get('request')
        user = request.user

        tags_data = validated_data.pop('tags')
        media_data = validated_data.pop('media')

        product = Product.objects.create(**validated_data, created_by=user)

        tags = self.get_or_create_tags(tags_data)
        product.tags.set(tags)
        self.use_product_media_method(
            "data",
            media_data=media_data, 
            product=product, 
            media_method=ProductMedia.objects.create,
        )
        return product
    
    def update(self, instance:Product, validated_data:dict):
        request = self.context.get('request')
        tags_data = validated_data.pop('tags', None)
        media_data = validated_data.pop('media', None)

        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)

        if tags_data is not None:
            tags = self.get_or_create_tags(tags_data)
            if request.method == "PATCH":
                instance.tags.add(*tags)
            else:
                instance.tags.set(tags)

        instance.save()

        if media_data is not None:
            self.use_product_media_method(
                "data",
                media_data=media_data, 
                product=instance, 
                media_method=ProductMedia.objects.get_or_create,
            )
        return instance


class SearchSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
    )
    created_by = serializers.CharField(source="created_by.username")

    class Meta:
        model = Product
        fields = ['name', 'tags', 'created_at', 'created_by']

