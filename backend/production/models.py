from django.db import models
from product.models import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.core.validators import MinValueValidator, DecimalValidator

# Create your models here.
class CatalogProduct(models.Model):

    
    
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    paints = models.ForeignKey(Paints, on_delete=models.CASCADE)
    worktimes = models.ManyToManyField(Worktimetype,through='CatalogWorktime', blank=True)
    accessories = models.ManyToManyField(AccessoryType, through='CatalogAccessoryDetail', blank=True)
    new_elements = models.ManyToManyField(Element, through='CatalogElement',blank=True)
    wood = models.ForeignKey(Wood, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    document = models.ManyToManyField(Document, blank=True)
    image = models.ManyToManyField(Image,blank=True)
    worktime_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    elements_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    elements_margin = models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)
    accessories_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    accessories_margin = models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)
    additional_margin = models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)
    summary_with_margin = models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)
    summary_without_margin = models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)
    percent_elements_margin = models.IntegerField(blank=True, null=True)
    percent_accessories_margin = models.IntegerField(blank=True, null=True)
    percent_additional_margin = models.IntegerField(blank=True, null=True)
    production_stages = models.ManyToManyField('ProductionStage', blank=True) 


    def __str__(self):
        return f"{self.name} | {self.category} | {self.collection}"

class Production(models.Model):

    class Meta:
        ordering = ['date_ordered']

    production_stages = models.ManyToManyField('ProductionStage', through='OrderProductionStage', blank=True, related_name="production_stages")
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default="pending")
    date_ordered = models.DateField()
    date_of_delivery = models.DateField(blank=True, null=True)
    notes = models.CharField(max_length=150, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name="productions_customer")
    
    # Generic relation to link to either NewProject or CatalogProduct
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(validators=[MinValueValidator(0)]) 
    order = GenericForeignKey('content_type', 'object_id')
    order_number = models.CharField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_delivery_date_after_order(self):
        return self.date_of_delivery >= self.date_ordered

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)


    def generate_order_number(self):
        
        order_id_part = str(self.object_id).zfill(3)
        now = timezone.now()
        date_part = now.strftime('%m%y')

        
        order_number = f"{order_id_part}{date_part}"
      
        return f"{order_number}"
    
    def __str__(self):
        return f"Production for {self.order} (Status: {self.status})"
class ProductionStage(models.Model):    

    stage_name = models.CharField(max_length=100)
    shortcut = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.stage_name}"
class OrderProductionStage(models.Model):
    
    production = models.ForeignKey('Production', on_delete=models.CASCADE, related_name='order_stages')
    production_stage = models.ForeignKey(ProductionStage, on_delete=models.CASCADE, related_name='order_assignments')
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.production_stage} - {'Done' if self.is_done else 'Pending'}"  
class CatalogAccessoryDetail(models.Model):
    catalog_product = models.ForeignKey(CatalogProduct, on_delete=models.CASCADE, related_name="accessories_of_catalog_product")
    type = models.ForeignKey(AccessoryType, on_delete=models.CASCADE, related_name="accessory_type_model")
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Catalog Accessory Name: {self.catalog_product.name}\nQuantity:{self.quantity}"
class CatalogElement(models.Model):
    catalog_product = models.ForeignKey(CatalogProduct, on_delete=models.CASCADE, related_name="element_of_catalog_product")
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name="element_type_model")
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Catalog Element Name: {self.catalog_product.name}\nQuantity:{self.quantity}"
class CatalogWorktime(models.Model):
    catalog_product = models.ForeignKey(CatalogProduct, on_delete=models.CASCADE, related_name="worktime_of_catalog_product")
    worktime = models.ForeignKey(Worktimetype, on_delete=models.CASCADE, related_name="worktime_type_model")
    duration = models.FloatField(default=0, validators=[MinValueValidator(0)])
    workers = models.IntegerField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=10, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"Worktime of {self.catalog_product.name} of type {self.worktime.name}\nDuration:{self.duration} Workers:{self.workers} Cost:{self.cost}"

    def save(self, *args, **kwargs):
        self.cost = self.worktime.cost
        super().save(*args, **kwargs)