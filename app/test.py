import datetime
import os
from google.cloud import firestore
from pprint import pprint
import os

from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

db = firestore.Client(project='graphql-gcp')

def pagination_snippet_by_document_snappshot():
    cities_ref = db.collection(u'cities')
    all_query = cities_ref.order_by(u'name',direction=firestore.Query.ASCENDING)
    d = all_query.get()
    print(len(d))
    # print(all_query.__sizeof__)
    first_query = cities_ref.order_by(u'name',direction=firestore.Query.ASCENDING).limit(10)
    docs = first_query.stream()
    last_doc = list(docs)[-1]
    next_query1 = (
        cities_ref
        .order_by(u'country',direction=firestore.Query.ASCENDING)
       .start_after(last_doc)
    )
    print(len(next_query1.get()))
    next_query = (
        cities_ref
        .order_by(u'country',direction=firestore.Query.ASCENDING)
       .start_after(last_doc)
        .limit(2)
    )
   
    # pprint(vars(next_query))
    
    result = next_query.stream()
    result = list(result)
    last_doc = result[-1]
    print(last_doc.id)
    for rs in result:
        print(f'{rs.id} => {rs.to_dict()}')

pagination_snippet_by_document_snappshot()

# for i in range(100):
#     data = {
#         u'name': u'Los Angeles ' + str(i),
#         u'state': u'CA ' + str(i),
#         u'country': u'USA ' + str(i)
#     }
#     # Add a new document in collection 'cities' with ID 'LA'
#     db.collection(u'cities').document(u'LA ' + str(i)).set(data) 

# city_ref = db.collection(u'cities').document(u'BJ')

# city_ref.set({
#     u'capital': True
# }, merge=True)

# data = {
#     u'stringExample': u'Hello, World!',
#     u'booleanExample': True,
#     u'numberExample': 3.14159265,
#     u'dateExample': datetime.datetime.now(tz=datetime.timezone.utc),
#     u'arrayExample': [5, True, u'hello'],
#     u'nullExample': None,
#     u'objectExample': {
#         u'a': 5,
#         u'b': True
#     }
# }

# db.collection(u'data').document(u'one').set(data)

# frank_ref = db.collection(u'users').document(u'frank')
# frank_ref.set({
#     u'name': u'Frank',
#     u'favorites': {
#         u'food': u'Pizza',
#         u'color': u'Blue',
#         u'subject': u'Recess'
#     },
#     u'age': 12
# })

# # Update age and favorite color
# frank_ref.update({
#     u'age': 13,
#     u'favorites.color': u'Red'
# })

    


