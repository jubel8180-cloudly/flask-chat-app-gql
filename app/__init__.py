import datetime
from ariadne import make_executable_schema, load_schema_from_path, \
    snake_case_fallback_resolvers, ObjectType, ScalarType
from ariadne.asgi import GraphQL

from app.workspace import resolve_create_workspace
from app.queries import resolve_todos, resolve_todo, resolve_viewer,resolve_getUser,\
                        resolve_getWorkspace,resolve_getChannel,resolve_getTenantWorkspace,\
                        resolve_listUsers,resolve_listChannels,resolve_openConversation,resolve_create_message

from app.types import viewer, listChannelConnection

from app.subscription import subscription
# from app.mutations import mutation
# from app.queries import query
# from app.subscriptions import subscription

query = ObjectType("Query")
mutation = ObjectType("Mutation")

query.set_field("todos", resolve_todos)
query.set_field("todo", resolve_todo)
query.set_field("viewer", resolve_viewer)
query.set_field("getUser", resolve_getUser)
query.set_field("getWorkspace", resolve_getWorkspace)
query.set_field("getTenantWorkspace", resolve_getTenantWorkspace)
query.set_field("getChannel", resolve_getChannel)
query.set_field("listUsers", resolve_listUsers)
query.set_field("listChannels", resolve_listChannels)
query.set_field("openConversation", resolve_openConversation)

mutation.set_field("createWorkspace", resolve_create_workspace)
mutation.set_field("createMessage", resolve_create_message)

datetime_scalar = ScalarType("Datetime")

type_defs = load_schema_from_path("schema.graphql")

@datetime_scalar.serializer
def serialize_datetime(value):
    return value.isoformat()

@datetime_scalar.value_parser
def parse_datetime_value(value):
    return datetime.fromisoformat(value)
    
schema = make_executable_schema(
    type_defs, query, mutation, subscription, datetime_scalar, snake_case_fallback_resolvers,viewer,listChannelConnection
)
app = GraphQL(schema, debug=True)

