import os
from google.cloud import firestore

def resolve_listUsers(obj, info, input):
    limit = input.get("limit")
    next_token = input.get("next_token")
    
    project_id = os.environ.get('PROJECT_NAME', None)
    db = firestore.Client(project=project_id)
    batch = db.batch()
    cities_ref = db.collection(u'users')
    if next_token == "":
        first_query = cities_ref.order_by(u'name').limit(limit)
        result = first_query.stream()
    
    else:
        doc = cities_ref.document(next_token).get()
        next_query = (
            cities_ref
            .order_by(u'name')
            .start_after(doc)
            .limit(limit)
            )
        result = next_query.stream()
    
    resultList = list(result)
    lastDoc = resultList[-1]
    availableMore = (
            cities_ref
            .order_by(u'name')
            .start_after(lastDoc)
            .limit(1)
           )
    next_token = ""
    if len(availableMore.get()) >= 1:
        next_token = lastDoc.id
    
    items = []
    for doc in resultList:
        _doc = doc.to_dict()
        items.append(_doc)

    obj = dict(
         items= items,
         next_token=next_token
    )
           
    return obj