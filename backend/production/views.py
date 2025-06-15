import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from django.conf import settings

from product.pdf_generator_scripts.pdf_generator import get_data, get_catalog_data
from product.pdf_generator_scripts.elements_production import generate_elements_productionpdf
from product.pdf_generator_scripts.pricing_report import generate_report

from django.shortcuts import render
from product.models import *
from .models import *
from product.serializers import *
from production.serializers import *
from rest_framework import authentication, generics, mixins, permissions, status
from rest_framework.decorators import api_view, parser_classes
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from product.views import get_or_create_model_instance, is_image
from django.http import JsonResponse, HttpResponse, FileResponse
from django.db import transaction, IntegrityError, DatabaseError
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.contrib.contenttypes.models import ContentType
from production.EANCode import generate_barcode
from io import BytesIO


import datetime
import json

# Create your views here.


class CatalogProductListCreateAPIView(
    generics.ListCreateAPIView):
    queryset = CatalogProduct.objects.all()
    serializer_class = CatalogProductSerializer

catalog_product_list_create_view = CatalogProductListCreateAPIView.as_view()
class ProductionListCreateAPIView(
    generics.ListCreateAPIView):

    queryset = Production.objects.all()
    serializer_class = ProductionSerializer

production_list_create_view = ProductionListCreateAPIView.as_view()
class ProducttionStepsListCreateAPIView(
    generics.ListCreateAPIView):
    
    queryset = ProductionStage.objects.all()
    
    serializer_class = ProductionStagesSerializer
    

production_stages_create_view = ProducttionStepsListCreateAPIView.as_view()


class CatalogProductDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView
    ):

    queryset = CatalogProduct.objects.all()
    lookup_field = 'pk'
    serializer_class = CatalogProductSerializer

    def update(self, request, *args, **kwargs):
        data = json.loads(request.body)
        wood = get_or_create_model_instance(Wood, data["wood"])
        collection = get_or_create_model_instance(Collection, data["collection"])    
        paint = get_or_create_model_instance(Paints, data["paints"])
        category_name = get_or_create_model_instance(Category, data["category"])

        elements_margin = data["elements_margin"]
        accesories_margin = data["accesories_margin"]
        additional_margin = data["additional_margin"]
        summary_with_margin = data["summary_with_margin"]
        summary_without_margin=data["summary_without_margin"]
        percent_elements_margin = data["percent_elements_margin"]
        percent_accesories_margin = data["percent_accesories_margin"]
        percent_additional_margin = data["percent_additional_margin"]

        catalog_product = get_object_or_404(CatalogProduct, pk=data["id"])

        catalog_product.name = data["name"]
        catalog_product.category = category_name
        catalog_product.paints = paint
        catalog_product.wood = wood
        catalog_product.collection = collection
        catalog_product.percent_elements_margin = percent_elements_margin
        catalog_product.percent_accessories_margin = percent_accesories_margin
        catalog_product.percent_additional_margin = percent_additional_margin
        catalog_product.elements_margin = elements_margin
        catalog_product.accessories_margin = accesories_margin
        catalog_product.additional_margin = additional_margin
        catalog_product.summary_with_margin = summary_with_margin
        catalog_product.summary_without_margin = summary_without_margin
        catalog_product.elements_cost = data["elements_cost"]
        catalog_product.accessories_cost = data["accesories_cost"]
        catalog_product.worktime_cost = data["worktime_cost"]

        elements_data = data["elements"]

        production_stages_data = data["production_stages"]
        for stage in production_stages_data:

            new_stage,created = ProductionStage.objects.get_or_create(stage_name = stage["stage_name"])
            catalog_product.production_stages.add(new_stage)

        catalog_product.new_elements.clear()
        
        for element_data in elements_data:
            #print(element_data["element"]["wood_type"])
            wood_type = get_or_create_model_instance(Wood, element_data["element"]["wood_type"]["name"])


            element = Element(
                name=element_data["element"]["name"],
                dimX=element_data["element"]["dimX"],
                dimY=element_data["element"]["dimY"],
                dimZ=element_data["element"]["dimZ"],
                wood_type = wood_type,              
            )
            element.set_price()
            element.save()

            #print(element_data["quantity"])
            catalog_product_element = CatalogElement(
                catalog_product = catalog_product,
                element = element,
                quantity = element_data["quantity"]
                
            )

        

            catalog_product_element.save()
            catalog_product.new_elements.add(element)


        accesories_data = data["accessories"]
        catalog_product.accessories.clear()
        print(f" Accesories data: {accesories_data}")
        #print(data["type"]["name"])

        for accesory in accesories_data:
            accesorytype = get_or_create_model_instance(AccessoryType, accesory["type"]["name"])
            quantity = accesory["quantity"]

            acc = CatalogAccessoryDetail.objects.create(
                catalog_product = catalog_product,
                type = accesorytype,
                quantity = quantity
            )
            acc.save()

            print(acc)
            print(accesorytype)
            

            catalog_product.accessories.add(accesorytype)

        catalog_product.save()
        
        return JsonResponse({'message': 'Data updated'}, status=201)


    

    
catalog_product_detail_view= CatalogProductDetailAPIView.as_view()

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def save_catalog_product(request):

    
    name = request.POST.get('name')
    category = request.POST.get('category')
    wood = request.POST.get('wood')
    collection = request.POST.get('collection')
    paint = request.POST.get('paint')
    elements_margin = request.POST.get('elements_margin')
    accesories_margin = request.POST.get('accesories_margin')
    additional_margin = request.POST.get('additional_margin')
    summary_with_margin = request.POST.get('summary_with_margin')
    summary_without_margin = request.POST.get('summary_without_margin')
    

    elements_post = request.POST.get('elements')
    try:
        elements_data = json.loads(elements_post)
        print(elements_data)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format for elements'}, status=400)
    
    worktime_post = request.POST.get('worktime')
    try:
        worktime_data = json.loads(worktime_post)
        print(worktime_data)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format for worktime'}, status=400)
    
    accesories_post = request.POST.get('accesories')
    try:
        accesories_data = json.loads(accesories_post)
        print(accesories_data)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format for accesories'}, status=400)
    
    production_stages_post = request.POST.get('production_stages')
    print(production_stages_post)
    try:
        production_stages = json.loads(production_stages_post)
        print(production_stages)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format for production stages'}, status=400)


    percent_elements_margin = request.POST.get('percent_elements_margin')
    percent_accesories_margin = request.POST.get('percent_accesories_margin')
    percent_additional_margin = request.POST.get('percent_additional_margin')
    elements_cost = request.POST.get('elements_cost')
    accesories_cost = request.POST.get('accesories_cost')
    worktime_cost =  request.POST.get('worktime_cost')
    
    print(f"ProductionStages: {production_stages}")


    """ customer_post = request.POST.get('customer')

    try:
        customer_data = json.loads(customer_post)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format for customer data'}, status=400)
     """

    uploaded_files = []
    for key in request.FILES:
        uploaded_files.append(request.FILES[key])

    now = timezone.now()
    #print(name,category,wood,collection,paint,elements_margin,accesories_margin,additional_margin,summary_with_margin,summary_without_margin)

 
    try:
        with transaction.atomic():
            # Get or create related models
            wood = get_or_create_model_instance(Wood, wood)
            collection = get_or_create_model_instance(Collection, collection)    
            paint = get_or_create_model_instance(Paints, paint)
            category = get_or_create_model_instance(Category, category)

            #error handling for empty value first


            # Create the NewProject instance
            catalog_product = CatalogProduct.objects.create(
                name=name,    
                category=category,
                paints=paint,
                collection=collection,
                wood=wood,
                elements_margin=elements_margin,
                accessories_margin=accesories_margin,
                additional_margin=additional_margin,
                summary_with_margin=summary_with_margin,
                summary_without_margin=summary_without_margin,
                percent_elements_margin=percent_elements_margin,
                percent_accessories_margin=percent_accesories_margin,
                percent_additional_margin=percent_additional_margin,
                elements_cost = elements_cost,
                accessories_cost = accesories_cost,
                worktime_cost = worktime_cost,

                
            )
            #Handle files and images
            for file in uploaded_files:
                if(is_image(file)):
                    #print(f"Image detected: {file}")
                    
                    

                    image = Image.objects.create(
                        name = file.name,
                        image = file,
                        catalog_product = catalog_product,
                        date = now,
                        file_type = file.name.split('.')[1],
                        size = round((file.size)/1000000, 2)
                        
                    )
                else:
                    
                    
                    
                    #print(f"Document detected: {file}")
                    document= Document.objects.create(
                        name = file.name,
                        document = file,
                        catalog_product = catalog_product,
                        date = now,
                        file_type = file.name.split('.')[1],
                        size = round((file.size)/1000000, 2)
                    )

            
            # Handle elements
            #elements_data = elements_data
            for element_data in elements_data:
                wood_type = get_or_create_model_instance(Wood, element_data["element"]["wood_type"]["name"])

                element = Element.objects.create(
                    name=element_data["element"]["name"],
                    dimX=element_data["element"]["dimX"],
                    dimY=element_data["element"]["dimY"],
                    dimZ=element_data["element"]["dimZ"],
                    wood_type=wood_type
                )
                element.set_price()
                element.save()

                CatalogElement.objects.create(
                    catalog_product=catalog_product,
                    element=element,
                    quantity=element_data["quantity"]
                )

                catalog_product.new_elements.add(element)
            
            # Handle worktime
            
            for worktime in worktime_data:
                worktimetype = get_or_create_model_instance(Worktimetype, worktime["text"])
                duration = worktime.get("hours", 0) or 0
                workers = worktime["workers"]

                CatalogWorktime.objects.create(
                    catalog_product=catalog_product,
                    worktime=worktimetype,
                    duration=duration,
                    workers=workers
                )
            
            # Handle accessories
            
            for accessory in accesories_data:
                accessory_type = get_or_create_model_instance(AccessoryType, accessory["type"]["name"])
                quantity = accessory["quantity"]

                CatalogAccessoryDetail.objects.create(
                    catalog_product = catalog_product,
                    type = accessory_type,
                    quantity = quantity
                )

                catalog_product.accessories.add(accessory_type)

            # Handle production stages

            for stage in production_stages:
                print(f"Stage: {stage}")
                production_stage,created = ProductionStage.objects.get_or_create(stage_name=stage["stage_name"])
                print(production_stage)
                OrderProductionStage.objects.create(
                    catalog_product=catalog_product,
                    production_stage=production_stage,
                    is_done=False
                )
                catalog_product.production_stages.add()
            

            

            

            # Save the final project instance
            catalog_product.save()

        return JsonResponse({'message': 'Data saved', 'project_id': catalog_product.id}, status=201)

    except IntegrityError as e:
        # Log the error
        print(e)
        return JsonResponse({'error': str(e)}, status=500)

@api_view(["PATCH"])
def update_order(request):

    data = request.data.get("data", [])
    order_id = request.data.get("id")
    order_number = request.data.get("order_number")
    print(f"Order id: {order_id}")
    print(f"Data: {data}")

    
    if not data:
        return JsonResponse({"error": "No data provided"}, status=400)

  
    if order_id is not None:
        try:
            order = Production.objects.get(order_number=order_number)
        except Production.DoesNotExist:
            return JsonResponse({"Error": "Production Object does not exist"})

    print(order.order_number)

    required_keys = ['id', 'stage_name', 'shortcut']

    if all(all(k in item for k in required_keys) for item in data):
        #Stages case
        print(f"Data in more than one: {data}")
        print(f"Order: {order}")
        order_production_stages = OrderProductionStage.objects.filter(production=order)
        print(f"Order_production_stages with given id: {order_production_stages}")
        for stage in order_production_stages:
            print(stage)
        
        for instance in order_production_stages:
            for stage in data:

                instance_stage = instance.production_stage
                instance_name = str(instance_stage)
                data_stage = stage["stage"]["stage_name"]
                #print(stage["is_done"])
                
                if instance_name == data_stage:
                    instance.is_done = stage["is_done"]
                    instance.save()
                    #JsonResponse({"Success": f"Production {order} stages updated"},status=200)
                
        
        return JsonResponse({"Success": f"Production {order} stages updated"})
                    
    elif isinstance(data, dict) and "notes" in data:
        #Notes case

        new_note = data["notes"]
        order.notes = new_note
        order.save()

        return JsonResponse({"Success": f"Production {order} notes updated"})
    
    elif isinstance(data, str):
        #any string data case
        
        parsed_date = parse_datetime(data)
        if parsed_date:
            #Date case
            print(f"Succesed parsed date: {parsed_date}")
            order.date_of_delivery = parsed_date
            order.save()

            return JsonResponse({"Message" : f"Parsed date: {parsed_date}"})
        return JsonResponse({"error": "Invalid data format for date"}, status=400)
    
    return JsonResponse({f"error": "Invalid data"}, status=400)
        

@api_view(['GET'])
def generate_elements_production(request, pk):

    id = pk
    buffer = BytesIO()

    output_dir = os.path.join(settings.BASE_DIR, f'product/pdf_generator_scripts/reports/{id}')
    #output_dir = f"/home/dylan/AutoWood/AutoWood_Backend/product/pdf_generator_scripts/reports/{id}" #for local deploy
    raport_name = f"rozpiska_produkcja_{id}.pdf"

    try:
        project_data = get_catalog_data(id)
        generate_elements_productionpdf(output_dir, raport_name, project_data)

        with open(f"{output_dir}/{raport_name}", "rb") as file:
            buffer.write(file.read())

        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename=raport_name)
    
    except FileNotFoundError as e:
        return JsonResponse({'error': 'Report file not found'}, status=status.HTTP_404_NOT_FOUND)
    except RuntimeError as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def generate_pricing__report(request, pk):

    id = pk
    buffer = BytesIO()

    output_dir = os.path.join(settings.BASE_DIR, f'product/pdf_generator_scripts/reports/{id}')
    #output_dir_2 = f"AutoWood_Backend/product/pdf_generator_scripts/reports/{id}" #for local deploy
    raport_name = f"wycena_{id}.pdf"

    #print(f"output_dir: {output_dir}")
    #print(f"output_dir_2: {output_dir_2}")

    try:
        project_data = get_catalog_data(id)
        generate_report(output_dir, raport_name, project_data)
        #print(f"open : {output_dir}/{raport_name}")

        with open(f"{output_dir}/{raport_name}", "rb") as file:
            buffer.write(file.read())

        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename=raport_name)
    
    except FileNotFoundError as e:
        return JsonResponse({'error': 'Report file not found'}, status=status.HTTP_404_NOT_FOUND)
    except RuntimeError as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def generate_ean(request):

    data = request.data.get("data", [])
    order_id = request.data.get("id")
    order_number = request.data.get("order_number")
    print(f"Order id: {order_id}")
    buffer = BytesIO()

    order = Production.objects.get(order_number=order_number)

    try: 
        file_name,save_path = generate_barcode(order)
        print(file_name)
        with open(f"{save_path}.svg", "rb") as file:
            buffer.write(file.read())

        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename=file_name)

    except ValueError as err:
        print(err)


    #print(f"output_dir: {output_dir}")
    #print(f"output_dir_2: {output_dir_2}")

    return JsonResponse({"Success": f"Production {order} notes updated"})

    pass

@api_view(["POST"])
def update_production_stages(request): 

    data = request.data
    all_stages = ProductionStage.objects.all()
    ids_sent = []
    deleted_ids = data['deletedIDs']
    

    
    if(deleted_ids):
        for id in deleted_ids:
            ProductionStage.objects.filter(id=id).delete()

    for stage in data['data']:
        print(f"Stage: {stage}")
        if 'id' in stage:
            stage_id = stage['id']
            ids_sent.append(stage_id)
        else:
            print(f"Stage missing ID: {stage}")

            try:
                ProductionStage.objects.create(
                    stage_name = stage['stage_name'],
                    shortcut = stage['shortcut'] 
                )
            except ValueError as e:
                print(f"Error : {e}")
    


    return JsonResponse({"Data" : f"Data"}, status = 201)

@api_view(["POST"])
def add_newproject_to_production(request):

   
    print(request)
    order_id = request.data.get("id")
    print(request.data)
    print(f"Order id: {order_id}")

    #print(f"Status: {status}\ndate_ordered: {date_ordered}\ndate_of_delivery: {date_of_delivery}") 
    #print(f"Notes: {notes}\ncustomer: {customer}\ncontent_type: {content_type}\n")

    try:
        new_project = NewProject.objects.get(id=order_id)
        production_stages = new_project.production_stages.all()


        status = "Pending"
        date_ordered = parse_datetime(request.data.get("dataOrdered"))
        date_of_delivery = parse_datetime(request.data.get("dateOfDelivery"))
        notes = request.data.get("notes")
        customer_data = request.data.get("customer")

        customer, created = Customer.objects.get_or_create(
                name=customer_data["name"],
                phone_number=int(customer_data["phone_number"]),
                street=customer_data["street"],
                code=customer_data["code"],
                city=customer_data["city"],
                email=customer_data["email"]
            )

        content_type = ContentType.objects.get_by_natural_key('product', 'newproject')
        print(content_type)
        
        try:
            new_production_order = Production.objects.create(
                status = status,
                date_ordered = date_ordered,
                date_of_delivery = date_of_delivery,
                notes = notes,
                customer = customer,
                content_type = content_type,
                object_id = order_id
                
            )

            new_production_order.production_stages.set(production_stages)
            new_production_order.save()
        except ValueError as e:
            print(f"Error {e}")


    except NewProject.DoesNotExist:
        return JsonResponse({"Failure": f"NewProject of id {order_id} does not exist"}, status=400)


    return JsonResponse({"Success" : f"Production {request} added"})


@api_view(["POST"])
def add_catalogproduct_to_production(request):

   
    print(request)
    order_id = request.data.get("id")
    print(request.data)
    print(f"Order id: {order_id}")

    #print(f"Status: {status}\ndate_ordered: {date_ordered}\ndate_of_delivery: {date_of_delivery}") 
    #print(f"Notes: {notes}\ncustomer: {customer}\ncontent_type: {content_type}\n")

    try:
        catalog_product = CatalogProduct.objects.get(id=order_id)
        


        status = "Pending"
        date_ordered = parse_datetime(request.data.get("dataOrdered"))
        date_of_delivery = parse_datetime(request.data.get("dateOfDelivery"))
        notes = request.data.get("notes")
        customer_data = request.data.get("customer")
        production_stages_data = request.data.get("productionSteps")
        production_stages = []

        for production_stage in production_stages_data:
            print(f"production stage: {production_stage}")
            new_stage = ProductionStage.objects.get(id=production_stage["id"])
            production_stages.append(new_stage)



        customer, created = Customer.objects.get_or_create(
                name=customer_data["name"],
                phone_number=int(customer_data["phone_number"]),
                street=customer_data["street"],
                code=customer_data["code"],
                city=customer_data["city"],
                email=customer_data["email"]
            )

        content_type = ContentType.objects.get_by_natural_key('production', 'catalogproduct')
        print(content_type)
        
        try:
            new_production_order = Production.objects.create(
                status = status,
                date_ordered = date_ordered,
                date_of_delivery = date_of_delivery,
                notes = notes,
                customer = customer,
                content_type = content_type,
                object_id = order_id,
              
            )
       
            new_production_order.production_stages.set(production_stages)
            new_production_order.save()
        except ValueError as e:
            print(f"Error {e}")


    except NewProject.DoesNotExist:
        return JsonResponse({"Failure": f"NewProject of id {order_id} does not exist"}, status=400)


    return JsonResponse({"Success" : f"Production {request} added"})

    """ try: 
        order = Production.objects.get(id=order_id)
        print(order)
    except Production.DoesNotExist:
        return JsonResponse({"error:" "No order in the production list with this ID"}, status=status.HTTP_404_NOT_FOUND) """

  
@api_view(["GET"])
def ping(request):
    return JsonResponse({"Success" : "Database status OK"})   
    

