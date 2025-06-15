from django.db import models
from decimal import Decimal, InvalidOperation
from django.apps import apps





class Wood(models.Model):
    name = models.CharField(max_length=20)
    density = models.FloatField(help_text="Density in kg/m3")
    price = models.DecimalField(help_text="Price in zl/m3", max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.name}"


class Paints(models.Model):
    name = models.CharField(max_length=30)
    cost = models.FloatField(blank=True,null=True)
    volume = models.DecimalField(help_text="litr", blank=True, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Element(models.Model):
    name = models.CharField(max_length=200)
    dimX = models.IntegerField(help_text="Dimension in milimeters")
    dimY = models.IntegerField(help_text="Dimension in milimeters")
    dimZ = models.IntegerField(help_text="Dimension in milimeters")
    wood_type = models.ForeignKey(Wood, on_delete=models.CASCADE)
    price = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=2)

    
    
    def set_price(self):
        try:
            
            volume = Decimal(int(self.dimX) / 1000) * Decimal(int(self.dimY) / 1000) * Decimal(int(self.dimZ) / 1000)
            self.price = volume * self.wood_type.price
        
        except InvalidOperation as e:
            print(f"Invalid operation: {e}")

    def __str__(self):
        return f"{self.name}"

        
class Collection(models.Model):
    firms = (
        ("Visby", "Visby"),
        ("Seart", "Seart"),
        ("Desiq", "Desiq"),
    )
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    partners = models.CharField(max_length=200, blank=True, choices=firms)

    def __str__(self):
        if(self.partners):
            return f"{self.name} | {self.partners}"
        else:
            return f"{self.name}"
    
class Category(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f"{self.name}"
    
    def get_absolute_url(self):
        return f'/{self.slug}'
    

    

class Worktimetype(models.Model):
    name = models.CharField(max_length=30)
    cost = models.FloatField(help_text="Cost of one hour worktime")

    def __str__(self):
        return f"{self.name}"
    
    

class AccessoryType(models.Model):

    choices = [
        ("Prowadnice", "Prowadnice"),
        ("Złącza", "Złącza"),
        ("Zawiasy", "Zawiasy")]

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True, null=True)
    weight = models.DecimalField(blank=True, max_digits=5, decimal_places=2, null=True)
    price = models.DecimalField(blank=True, max_digits=8, decimal_places=2, null=True)
    type = models.CharField(max_length = 50, choices=choices,)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"
    class Meta:
        db_table = 'product_accesory_type'

def images_user_directory_path(instance, filename):
    # This will save the image in a directory named after the user's id
    string = f'new_projects/{instance.project.id}/images/{filename}'
    return string

def documents_user_directory_path(instance, filename):
    # This will save the documents in a directory named after the user's id
    string = f'new_projects/{instance.project.id}/documents/{filename}'
    return string
class Customer(models.Model):

    name = models.CharField(max_length=60, blank=True, null=True)
    phone_number = models.IntegerField(null=True)
    street = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=15, null=True)
    city = models.CharField(max_length = 40, null=True)
    email = models.EmailField(max_length=60,null=True)

    def __str__(self):
        return f"{self.name}"




class NewProject(models.Model):
    
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    paints = models.ForeignKey(Paints, on_delete=models.CASCADE)
    worktimes = models.ManyToManyField(Worktimetype,through='ProjectWorktime', blank=True)
    accessories = models.ManyToManyField(AccessoryType, through='AccessoryDetail', blank=True)
    new_elements = models.ManyToManyField(Element, through='NewProjectElement',blank=True)
    wood = models.ForeignKey(Wood, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    document = models.ManyToManyField('Document', blank=True)
    image = models.ManyToManyField('Image',blank=True)
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
    production_stages = models.ManyToManyField('production.ProductionStage', blank=True)

    def __str__(self):
        return self.name
    
class Document(models.Model):
    
    name = models.CharField(max_length=100)
    document = models.ImageField(upload_to=documents_user_directory_path)
    project = models.ForeignKey(NewProject, on_delete=models.CASCADE, related_name='documents', null=True)
    date = models.DateTimeField()
    file_type = models.CharField(max_length=3,null=True)
    size = models.DecimalField(decimal_places=2, max_digits=7, null=True)



class Image(models.Model):
    
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to=documents_user_directory_path)
    project = models.ForeignKey(NewProject, on_delete=models.CASCADE, related_name='images', null=True)
    date = models.DateTimeField()
    file_type = models.CharField(max_length=3, null=3)
    size = models.DecimalField(decimal_places=2, max_digits=7, null=True)
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    paints = models.ForeignKey(Paints, on_delete=models.CASCADE)
    elements = models.ManyToManyField(Element)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    class Meta: 
        ordering = ('category', 'name')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self): 
        return f'/{self.category.name}/{self.name}'

class ProjectWorktime(models.Model):
    project = models.ForeignKey(NewProject, on_delete=models.CASCADE, related_name="project_worktime")
    worktime = models.ForeignKey(Worktimetype, on_delete=models.CASCADE)
    duration = models.FloatField(default=0)
    workers = models.IntegerField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=10)

    def save(self, *args, **kwargs):
        self.cost = self.worktime.cost
        super().save(*args, **kwargs)
    

class AccessoryDetail(models.Model):
    project = models.ForeignKey(NewProject, on_delete=models.CASCADE, related_name="project_accessories")
    type = models.ForeignKey(AccessoryType, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    
class Balance(models.Model):
    balance = models.DecimalField(blank=True, max_digits=7, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    

class NewProjectElement(models.Model):
    project = models.ForeignKey(NewProject, on_delete=models.CASCADE, related_name='project_elements')
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.project.name} - {self.quantity}"