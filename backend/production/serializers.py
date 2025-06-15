from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import *
from warehouse.models import *
from production.models import *
from product.serializers import NewProjectSerializer, WorktimeTypeSerializer, AccessoryTypeSerializer, WoodSerializer, ElementSerializer, PaintsSerializer, CategorySerializer, CollectionSerializer, CustomerSerializer




class WorktimeSerializer(serializers.ModelSerializer):

    worktime = WorktimeTypeSerializer(read_only=True) 
    name = WorktimeTypeSerializer(read_only = True, many = True)

    class Meta:
        model = CatalogWorktime
        fields = '__all__'

class AccessoryTypeSerializer(serializers.ModelSerializer):

    type_choices = serializers.SerializerMethodField()
    class Meta:
        model = AccessoryType
        fields = '__all__'

    def get_type_choices(self, obj):
        return AccessoryType.choices

class AccessorySerializer(serializers.ModelSerializer):

    type = AccessoryTypeSerializer(read_only = True)
    type_id = serializers.PrimaryKeyRelatedField(queryset=AccessoryType.objects.all(),source='type', write_only=True)
    class Meta:
        model = CatalogAccessoryDetail
        fields = '__all__'

class CatalogElementSerializer(serializers.ModelSerializer):
    element = ElementSerializer(read_only = True)
    name = ElementSerializer(read_only = True, many = True)

    class Meta:
        model = CatalogElement
        fields = '__all__'


class ProductionStagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductionStage
        fields = '__all__'

class OrderProductionStageSerializer(serializers.ModelSerializer):
    stage = ProductionStagesSerializer(read_only = True, source='production_stage')
    
    class Meta:
        model = OrderProductionStage
        fields = ['stage', 'is_done']

class CatalogProductSerializer(serializers.ModelSerializer):

    worktimes = WorktimeSerializer(many=True, read_only=True, source = 'catalog_worktime')
    accessories = AccessorySerializer(many=True, read_only=True, source = 'catalog_accessories')
    elements = CatalogElementSerializer(many=True,read_only = True, source = 'catalog_elements')
    wood = WoodSerializer( read_only=True)
    paints = PaintsSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    collection = CollectionSerializer(read_only=True)
    production_stages = ProductionStagesSerializer(many=True, read_only=True)

    

    class Meta:
        model = CatalogProduct
        fields = [
            'id',
            'name',
            'category',
            'worktimes',
            'accessories',
            'elements',
            'wood',
            'paints',
            'category',
            'collection',
            'elements_margin',
            'accessories_margin',
            'additional_margin',
            'summary_with_margin',
            'summary_without_margin',
            'percent_elements_margin',
            'percent_accessories_margin',
            'percent_additional_margin',
            'elements_cost',
            'accessories_cost',
            'worktime_cost',
            'production_stages'
         
        ]

class GenericRelatedField(serializers.Field):

    def to_representation(self, value):
        if isinstance(value, CatalogProduct):
            return CatalogProductSerializer(value).data
        elif isinstance(value, NewProject):
            return NewProjectSerializer(value).data
        

    def to_internal_value(self, data):
        model = data.get("type")
        object_id = data.get("id")

        if not model or not object_id:
            raise serializers.ValidationError("type and id required")
        
        model_map = {
            "catalog_product": CatalogProduct,
            "new_project": NewProject
        }

        ModelClass = model_map.get(model.lower())

        if not ModelClass:
            raise serializers.ValidationError(f"Invalid type {model} Type 'catalog_product' or 'new_project'")


        try:
            return ModelClass.objects.get(id=object_id)
        except ModelClass.DoesNotExist:
            raise serializers.ValidationError(f"No {model} found with id {object_id}")

class ProductionSerializer(serializers.ModelSerializer):

    stages = OrderProductionStageSerializer(many=True, read_only=True, source='production')
    customer = CustomerSerializer(read_only=True) 
    order = GenericRelatedField()

    class Meta:
        model = Production
        fields = [
            "stages",
            "order",
            "status",
            "date_ordered",
            "date_of_delivery",
            "notes",
            "customer",
            "order_number"
         
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'status' in representation:
            representation['status'] = representation['status'].capitalize()
        return representation