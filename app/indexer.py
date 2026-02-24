import json
import meilisearch
import os
from app.search.client import get_client

index = get_client().index('products')

with (open('data/products.json')) as file:
    products = json.load(file)

task = index.add_documents(products)
index.wait_for_task(task.task_uid)


searchable_attributes = ['name', 'description','brand','country']
filterable_attributes = ['price', 'country', 'brand', 'inStock']
sortable_attributes = ['price']
typo_parameters = {'minWordSizeForTypos' : { 'oneTypo' : 4, 'twoTypos' : 9} }

task = index.update_searchable_attributes(searchable_attributes)
index.wait_for_task(task.task_uid)

task = index.update_filterable_attributes(filterable_attributes)
index.wait_for_task(task.task_uid)

task = index.update_sortable_attributes(sortable_attributes)
index.wait_for_task(task.task_uid)

task = index.update_typo_tolerance(typo_parameters)
index.wait_for_task(task.task_uid)



