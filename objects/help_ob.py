import uuid
import requests
import json

from django.utils import timezone
from .models import *
from .help_ob import *

shop_url = 'quickstart-b4fa8ebd.myshopify.com'
access_token = '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' 
# shop_url = 'trialproject12.myshopify.com/'
# access_token = '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'
# Define the API endpoint URL
 
store_instances = Store.objects.get(organization_name="Mihir")


#for orders
# def process_order(object_type):
     
       
#     url = f'https://{shop_url}/admin/api/2024-01/{object_type}.json?status=any'

#     # Make the request with the access t-oken included in the headers
#     headers = {
#         'X-Shopify-Access-Token': access_token,
#         'Content-Type': 'application/json'
#     }

#     response = requests.get(url, headers=headers)
#     print(response.status_code,response.text)
#     data = response.json()
#     # print(data)
#     new_instance = Object(
#     store=store_instances,  # Replace your_store_instance with the actual Store instance
#     object_type=object_type,  # Assuming the object_type is "product"
#     data=data,  # Replace data with your actual JSON data
#     uuid=uuid.uuid4(),  # Generate a UUID for the version
#     backup_date=timezone.now().date()  # Set the backup_date to the current date/time
#     )

#     new_instance.save()

def process_order_id(object,id):
    url = f'https://{shop_url}/admin/api/2024-01/{object}/{id}.json?fields=id,line_items,transactions,tags'

    # Make the request with the access token included in the headers
    headers = {
        'X-Shopify-Access-Token': access_token,
    }

    response = requests.get(url, headers=headers)
    print(response.status_code,response.text)
    data = response.json()
    # print(data)
    new_instance = Object(
    store=store_instances,  # Replace your_store_instance with the actual Store instance
    object_type=object,  # Assuming the object_type is "product"
    data=data,  # Replace data with your actual JSON data
    uuid=uuid.uuid4(),  # Generate a UUID for the version
    backup_date=timezone.now().date()  # Set the backup_date to the current date/time
    )

    new_instance.save()

def create_obj(object_type,data):
    url = f'https://{shop_url}/admin/api/2024-01/{object_type}.json'
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }
    # print(data)
    response = requests.post(url, json=data, headers=headers)

    print(response.status_code,response.text)
    print(response.json())

 
def backup_data_id(object,id):
    url = f'https://{shop_url}/admin/api/2024-01/{object}/{id}.json'

    # Make the request with the access token included in the headers
    headers = {
        'X-Shopify-Access-Token': access_token,
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    # print(data)
    return response.status_code


def delete_shopify_data(object_type,data):
    url = f'https://{shop_url}/admin/api/2024-01/{object_type}/{data[object_type[:-1]]["id"]}.json'
    headers = {
        'X-Shopify-Access-Token': access_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.delete(url, headers=headers)
    print('blog deleted')
    print(response.status_code)

def restore_shopify_data(object_type , data):
    # print(data[object_type]["id"])
    # print("data" , data)
    url = f'https://{shop_url}/admin/api/2024-01/{object_type}/{data[object_type[:-1]]["id"]}.json'
    headers = {
        'X-Shopify-Access-Token': access_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    # print(response.status_code,response.text)
    return response

def restore(id):
    Obj = Object.objects.get(uuid=id)
    print(Obj.uuid)
    data = Obj.data
    object_type = Obj.object_type
    
    if object_type[:-1] in data:
    #   print(data)
      response = restore_shopify_data(object_type, data) 
      print(data)
      if response.status_code != 200:
            print(f'Creating {object_type}')
            # create_obj(object_type,data)
       
    else:
     for item in data[object_type]:
        # print(item)
        response = restore_shopify_data(object_type, {object_type[:-1]: item}) 
        # remove the last character as query 
        if response.status_code != 200:
            print(f'Creating {object_type}')
            create_obj(object_type, {object_type[:-1]: item})
        # print(response.status_code,response.text)
    


def process(object_type,data):
    if object_type[:-1] in data:
        #   print(data)
        item_id=data[object_type].get('id')
        res = backup_data_id(object_type, item_id)
        if res == 200:
            delete_shopify_data(object_type, data)

            print(f'Creating {object_type}')
            create_obj(object_type, data)
        else:
            create_obj(object_type, data)

    else:
        for item in data[object_type]:
            print(item)
            item_id = item.get("id")
            print(item_id)
            res=backup_data_id(object_type,item_id)
            if res==200:
                delete_shopify_data(object_type,{object_type[:-1]: item})
            # remove the last character as query

                print(f'Creating {object_type}')
                create_obj(object_type, {object_type[:-1]: item})
            else:
                create_obj(object_type, {object_type[:-1]: item})
            # print(response.status_code,response.text)

