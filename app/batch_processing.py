
from google.cloud import firestore
import os

from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

db = firestore.Client(project='graphql-gcp')

batch = db.batch()



def BatchOperation():
    # print("pagination_snippet_by_field")
    # pagination_snippet_by_field()
    # print("pagination_snippet_by_document_snappshot")
    # pagination_snippet_by_document_snappshot()
    print("pagination_snippet_by_document_id")
    pagination_snippet_by_document_id("L")


def pagination_snippet_by_field():
    cities_ref = db.collection(u'cities')
    first_query = cities_ref.order_by(u'name').limit(1)
    docs = first_query.stream()
    last_doc = list(docs)[-1]
    last_pop = last_doc.to_dict()[u'name']
    next_query = (
        cities_ref
        .order_by(u'name')
       .start_after({
            u'name': last_pop
        })
        .limit(2)
    )
    result = next_query.stream()
    for rs in result:
        print(f'{rs.id} => {rs.to_dict()}')
        

def pagination_snippet_by_document_snappshot():
    cities_ref = db.collection(u'cities')
    first_query = cities_ref.order_by(u'name').limit(1)
    docs = first_query.stream()
    last_doc = list(docs)[-1]
    
    next_query = (
        cities_ref
        .order_by(u'name')
       .start_after(last_doc)
        .limit(2)
    )
    result = next_query.stream()
    for rs in result:
        print(f'{rs.id} => {rs.to_dict()}')


def pagination_snippet_by_document_id(document_id):
    cities_ref = db.collection(u'cities')
    try:
        doc = cities_ref.document(document_id).get()
    except Exception as e:
        print(e)
        return
    print(doc.exists)
    if not doc.exists:
        return
        print(doc)
    
    next_query = (
        cities_ref
        .order_by(u'name')
        .start_after(doc)
        .limit(2)
    )
    result = next_query.stream()
    for rs in result:
        print(f'{rs.id} => {rs.to_dict()}')

# BatchOperation()