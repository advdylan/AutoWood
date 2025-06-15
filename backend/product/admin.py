from django.contrib import admin
from .models import *
from warehouse.models import *
from production.models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "paints", 
        "collection"
        )

admin.site.register(Product, ProductAdmin)

class BoardAdmin(admin.ModelAdmin):
    list_display=(
        "name",
        "dimX",
        "dimY",
        "dimZ",
        "wood_type",
        "quantity"
    )
admin.site.register(Board, BoardAdmin)

class WoodAdmin(admin.ModelAdmin):
    
    list_display = ("name", "density", "price")

admin.site.register(Wood,WoodAdmin)


class PaintAdmin(admin.ModelAdmin):
    list_display = ("name", "cost", "volume")

admin.site.register(Paints, PaintAdmin)

class WorktimetypeAdmin(admin.ModelAdmin):
    list_display = ("name", "cost")

admin.site.register(Worktimetype, WorktimetypeAdmin)


class AccessoryTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "weight", "price")

admin.site.register(AccessoryType, AccessoryTypeAdmin)

class ElementAdmin(admin.ModelAdmin):
    list_display = ("name", "dimX", "dimY", "dimZ", "wood_type", "price",)

admin.site.register(Element, ElementAdmin)
    
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "partners")

admin.site.register(Collection, CollectionAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")

admin.site.register(Category, CategoryAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "street", "code","city","email")

admin.site.register(Customer, CustomerAdmin)

class ImageAdmin(admin.ModelAdmin):
    list_display = ("name",'project', "image", "date")

admin.site.register(Image, ImageAdmin)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ("name",'project', "document", "date")

admin.site.register(Document, DocumentAdmin)

class ProjectWorktimeInline(admin.TabularInline):
    model = ProjectWorktime
    extra = 1

class AccessoryDetailInline(admin.TabularInline):
    model = AccessoryDetail
    extra = 1

class ElementsDetailInline(admin.TabularInline):
    model = NewProjectElement
    extra = 1
class NewProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectWorktimeInline, AccessoryDetailInline, ElementsDetailInline]
    list_display = ('id',
                    'name',
                    'category',
                    'collection',
                    'summary_with_margin',
                    'summary_without_margin', 
                    'percent_elements_margin',
                    'percent_accessories_margin',
                    'percent_additional_margin'
                    )
    search_fields = ('name',)

admin.site.register(NewProject,NewProjectAdmin)

class ProjectWorktimeAdmin(admin.ModelAdmin):
    list_display = ("project","worktime")

admin.site.register(ProjectWorktime,ProjectWorktimeAdmin)


class CatalogElementDetailInline(admin.TabularInline):
    model = CatalogElement
    extra = 1

class CatalogWorktimeDetailInline(admin.TabularInline):
    model = CatalogWorktime
    extra = 1

class CatalogAccessoryDetailInline(admin.TabularInline):
    model = CatalogAccessoryDetail
    extra = 1

class OrderProductionStageDetailInline(admin.TabularInline):
    model = OrderProductionStage
    extra = 1


class ProductionAdmin(admin.ModelAdmin):
    inlines = [OrderProductionStageDetailInline]

   

    list_display = (
        
        'status',
        'date_ordered',
        'date_of_delivery',
        'content_type',
        'object_id',
        'order'
    )



admin.site.register(Production, ProductionAdmin)


class ProductionStageAdmin(admin.ModelAdmin):
    list_display = (
        'stage_name','shortcut'

    )
admin.site.register(ProductionStage, ProductionStageAdmin)

class CatalogProductAdmin(admin.ModelAdmin):

    inlines = [CatalogElementDetailInline, CatalogAccessoryDetailInline, CatalogWorktimeDetailInline]
    
    list_display = (
        'name', 'category', 'paints', 'wood', 'collection',
        'worktime_cost', 'elements_cost','' 'elements_margin',
        'accessories_cost', 'accessories_margin', 'additional_margin',
        'summary_with_margin', 'summary_without_margin',
        'percent_elements_margin', 'percent_accessories_margin', 'percent_additional_margin'
    )
    
    raw_id_fields = ('worktimes', 'accessories', 'new_elements', 'document', 'image')

admin.site.register(CatalogProduct, CatalogProductAdmin)