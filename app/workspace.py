import os
from ariadne import convert_kwargs_to_snake_case
from google.cloud import firestore
from core import utils
from core import exceptions


# def workspace_by_id(self, workspace_id=None):
#     app = self.utils.dynamodb_get_item(
#         self.table_name, consistent_read=True, id=workspace_id, sortKey="Workspace"
#     )
#     if app is None:
#         raise exceptions.NotFoundError(
#             f"Workspace with ID {workspace_id} does not exist"
#         )
#     if app.get("active") is False:
#         raise exceptions.NotFoundError(
#             f"Workspace with ID {workspace_id} was deleted"
#         )
#     return app
#
#
# def workspace_by_tenant_id(self, tenant_id=None, app_id=None):
#     sort_key = ''
#     app = None
#     workspace_id = None
#     next_token = None
#     limit = None
#     data = ""
#     if tenant_id and app_id:
#         sort_key = "Workspace#{}#{}".format(tenant_id, app_id)
#     else:
#         raise exceptions.NotFoundError(
#             f"Workspace for Tenant ID {tenant_id} does not exist"
#         )
#     key_condition_expression = Key("sortKey").eq(sort_key) & Key("data").eq(sort_key)
#     items, next_token = self.utils.list_items_by_using_key_condition_expression(
#         table_name=self.table_name,
#         typename=sort_key,
#         limit=limit,
#         next_token=next_token,
#         key_condition_expression=key_condition_expression,
#         index_name="SortKeyGSI",
#     )
#     if items and len(items) > 0:
#         workspace_id = items[0]['id']
#         app = self.workspace_by_id(workspace_id=workspace_id)
#     return app

def resolve_create_workspace(obj, info, input):

    name = input.get("name")
    email = input.get("email")
    description = input.get("description")
    tenant_id = input.get("tenantId")
    app_id = input.get("appId")

    now = utils.iso_utc_now()

    print(now)
    print("obj: {}".format(obj))
    print("info: {}".format(info))
    print("input: {}".format(input))

    if not name:
        raise exceptions.GraphQLError("name is required to create an Workspace")
    if not email:
        raise exceptions.GraphQLError("email is required to create an Workspace")

    # workspace_exists = self.workspace_by_tenant_id(tenant_id=tenant_id, app_id=app_id)
    # if workspace_exists:
    #     return workspace_exists
    workspace_id = utils.make_short_id(utils.generate_unique_id())
    secrets = [utils.make_workspace_secret()]
    arguments = dict(
        data=workspace_id,
        workspace=workspace_id,
        name=name,
        email=email,
        description=description,
        secrets=secrets,
        createdAt=now,
        updatedAt=now,
        active=True,
        tenantId=tenant_id,
        appId=app_id,
        __typename="Workspace",
        sortKey="Workspace"
    )
    project_id = os.environ.get('PROJECT_NAME', None)
    print("project_id: {}".format(project_id))
    db = firestore.Client(project=project_id)
    # docs = db.collection('app-messaging').stream()
    # for doc in docs:
    #     print(f'{doc.id} => {doc.to_dict()}')
    app = db.collection('app-messaging').document(workspace_id).set(arguments)
    arguments['id'] = workspace_id
    print(app)
    #

    if app:
        workspace_id_n = "{}#Workspace#{}#{}".format(workspace_id, tenant_id, app_id)
        arguments_agency = dict(
            secrets=secrets,
            createdAt=now,
            updatedAt=now,
            active=True,
            __typename="Workspace#Agency"
            # sortkey=sortkey,
            # data=sortkey
        )
        app_agency = db.collection('app-messaging').document(workspace_id_n).set(arguments_agency)

    # {
    #     "id": "PX3mSkwbY4h#Workspace",
    #
    #     "active": true,
    #     "appId": "CxMkvJSCvbS",
    #     "createdAt": "2022-05-03T21:03:13.611493+00:00",
    #     "data": "PX3mSkwbY4h",
    #     "description": "testag23",
    #     "email": "testag2admin@testp.com",
    #     "name": "testag23",
    #     "secrets": [
    #         "ecd012b5506040508483c2298f6962b2"
    #     ],
    #     "tenantId": "6320",
    #     "updatedAt": "2022-05-03T21:03:13.611493+00:00",
    #     "workspace": "PX3mSkwbY4h",
    #     "__typename": "Workspace"
    # }
    #
    # {
    #     "id": "PX3mSkwbY4hWorkspace#6320#CxMkvJSCvbS",
    #     "active": true,
    #     "createdAt": "2022-05-03T21:03:13.611493+00:00",
    #     "data": "Workspace#6320#CxMkvJSCvbS",
    #     "secrets": [
    #         "ecd012b5506040508483c2298f6962b2"
    #     ],
    #     "updatedAt": "2022-05-03T21:03:13.611493+00:00",
    #     "__typename": "Workspace#Agency"
    # }



    #
    # # self.utils.get_event_repository().event_with_topic(None,
    # #                                                    'AppCreatedEvent',
    # #                                                    payload=app)
    # # self.utils.get_notification_repository().send_pubsub(
    # #     topic='AppCreatedEvent', payload=app)
    # return app
    print("hllllllrrrr")

    return utils.object_sanitizer(arguments)