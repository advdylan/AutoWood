from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import *
from warehouse.models import *
from production.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PaintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paints
        fields = '__all__'


class WorktimeTypeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Worktimetype
        fields = '__all__'

class WorktimeSerializer(serializers.ModelSerializer):
    worktime = WorktimeTypeSerializer(read_only=True)  # Serialize the related Worktimetype model
    #worktime_id = serializers.PrimaryKeyRelatedField(queryset=Worktimetype.objects.all(), source='worktime', write_only=True)

    name = WorktimeTypeSerializer(read_only = True, many = True)
    class Meta:
        model = ProjectWorktime
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
        model = AccessoryDetail
        fields = '__all__'

class WoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wood
        fields = [
            'name',
            'density',
            'price'
        ]

class ElementSerializer(serializers.ModelSerializer):

    wood_type = WoodSerializer(read_only=True)
    wood_type_id = serializers.PrimaryKeyRelatedField(queryset=Wood.objects.all(), source='wood_type', write_only=True)
    class Meta:
        model = Element
        fields = '__all__'


class NewProjectElementSerializer(serializers.ModelSerializer):
    element = ElementSerializer(read_only = True)
    element_id = serializers.PrimaryKeyRelatedField(queryset=Element.objects.all(), source='element', write_only=True)
    
    class Meta:
        model = NewProjectElement
        fields = '__all__'
        
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = '__all__'

class BoardSerializer(serializers.ModelSerializer):

    wood_type = WoodSerializer( read_only=True)

    class Meta:
        model = Board
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer): 
    category = CategorySerializer(read_only=True)
    paints = PaintsSerializer(read_only=True)
    worktimes = WorktimeSerializer(many=True, read_only=True)
    accessories = AccessorySerializer(many=True, read_only=True)
    elements = ElementSerializer(many=True, read_only=True)
    collection = CollectionSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'paints',
            'worktimes',
            'accessories',
            'elements',
            'collection'
        ]
class ProductionStagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductionStage
        fields = '__all__'


        
class NewProjectSerializer(serializers.ModelSerializer):
    worktimes = WorktimeSerializer(many=True, read_only=True, source='project_worktime')
    accessories = AccessorySerializer(many=True, read_only=True, source='project_accessories')
    elements = NewProjectElementSerializer(many=True, read_only=True, source='project_elements')
    wood = WoodSerializer( read_only=True)
    paints = PaintsSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    collection = CollectionSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    image = ImageSerializer(many = True,read_only = True, source = 'images')
    document = DocumentSerializer(many = True,read_only = True, source = 'documents')
    production_stages = ProductionStagesSerializer(many = True, read_only=True)


    class Meta:
        model = NewProject
        fields = [
            'id',
            'name',
            'category',
            'customer',
            'paints',
            'worktimes',
            'accessories',
            'elements',
            'wood',
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
            'image',
            'document',
            'production_stages'
        ]