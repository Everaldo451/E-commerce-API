from rest_framework import serializers
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
    created_by = serializers.SerializerMethodField('get_created_by')

    def get_created_by(self, obj):
        return f'{obj.created_by.first_name} {obj.created_by.last_name}'

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'tags', 'media', 'created_at', 'is_available','created_by']
        read_only_fields = ['id', 'created_at', 'is_available', 'created_by']

    def create(self, validated_data:dict):
        tags_data = validated_data.pop('tags')
        media_data = validated_data.pop('media')

        product = Product.objects.create(**validated_data)

        tag_objs = [
            Tag.objects.get_or_create(name=tag['name'])[0]
            for tag in tags_data
        ]
        product.tags.set(tag_objs)

        for media in media_data:
            ProductMedia.objects.create(product=product, **media)
        return product
    
    def update(self, instance:Product, validated_data:dict):
        tags_data = validated_data.pop('tags', None)
        media_data = validated_data.pop('media', None)

        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)

        if tags_data is not None:
            tag_objs = [
                Tag.objects.get_or_create(name=tag['name'])[0]
                for tag in tags_data
            ]
            instance.tags.set(tag_objs)

        instance.save()

        if media_data is not None:
            for media in media_data:
                ProductMedia.objects.get_or_create(product=instance, data=media['data'])
        return instance
