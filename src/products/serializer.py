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
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
    )
    media = ProductMediaSerializer(many=True)
    created_by = serializers.SerializerMethodField('get_created_by')

    def get_created_by(self, obj):
        return f'{obj.created_by.first_name} {obj.created_by.last_name}'

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'tags', 'media', 'created_at', 'is_available','created_by']
        read_only_fields = ['id', 'created_at', 'is_available', 'created_by']
    
    def use_product_media_method(self, *args, media_data:list[dict], product, media_method:Callable) -> None:
        for media in media_data:
                media_data = {key: media[key] for key in args}
                media_method(product=product, **media_data)

    def create(self, validated_data:dict):
        request = self.context.get('request')
        user = request.user

        tags_data = validated_data.pop('tags')
        media_data = validated_data.pop('media')

        product = Product.objects.create(**validated_data, created_by=user)

        product.tags.set(tags_data)
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
            if request.method == "PATCH":
                instance.tags.add(*tags_data)
            else:
                instance.tags.set(tags_data)

        instance.save()

        if media_data is not None:
            self.use_product_media_method(
                "data",
                media_data=media_data, 
                product=instance, 
                media_method=ProductMedia.objects.get_or_create,
            )
        return instance
