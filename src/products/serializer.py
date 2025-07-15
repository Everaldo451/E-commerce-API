from django.db import transaction
from rest_framework import serializers
from typing import Callable

from users.models import User
from .models import Tag, Product, ProductMedia
import logging

class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

    def create(self, validated_data:dict):
        logging.debug('create tag')
        tag, _ = Tag.objects.get_or_create(**validated_data)
        return tag


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

    @transaction.atomic
    def create(self, validated_data:dict):
        logging.debug('Start product create.')
        request = self.context.get('request')
        user = request.user

        tags_data = validated_data.pop('tags')
        media_data = validated_data.pop('media')

        product = Product.objects.create(**validated_data, created_by=user)

        logging.debug('tags search')
        tags = self.get_or_create_tags(tags_data)
        logging.debug('tags add')
        product.tags.set(tags)
        logging.debug('product media create.')
        self.use_product_media_method(
            "data",
            media_data=media_data, 
            product=product, 
            media_method=ProductMedia.objects.create,
        )
        logging.debug('product created successfully.')
        return product
    
    @transaction.atomic
    def update(self, instance:Product, validated_data:dict):
        logging.debug("Start product update.")
        request = self.context.get('request')
        tags_data = validated_data.pop('tags', None)
        media_data = validated_data.pop('media', None)

        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)

        if tags_data is not None:
            logging.debug("tags search")
            tags = self.get_or_create_tags(tags_data)
            if request.method == "PATCH":
                logging.debug("tags partial update")
                instance.tags.add(*tags)
            else:
                logging.debug("tags total update")
                instance.tags.set(tags)

        instance.save()

        if media_data is not None:
            logging.debug('product media update.')
            self.use_product_media_method(
                "data",
                media_data=media_data, 
                product=instance, 
                media_method=ProductMedia.objects.get_or_create,
            )
        logging.debug('product updated successfully.')
        return instance


class SearchSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all(),
        required=False
    )
    created_by = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        required=False
    )

    class Meta:
        model = Product
        fields = ['name', 'tags', 'created_at', 'created_by']

