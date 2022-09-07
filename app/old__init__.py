import datetime
import logging
from ariadne import QueryType
from flask import Flask

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType, ScalarType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from app.workspace import resolve_create_workspace
from app.queries import resolve_todos, resolve_todo, resolve_viewer,resolve_getUser,\
                        resolve_getWorkspace,resolve_getChannel,resolve_getTenantWorkspace,\
                        resolve_listUsers,resolve_listChannels,resolve_openConversation

from app.types import viewer, listChannelConnection

def create_app():
    app = Flask(__name__)
    app.logger.setLevel(logging.DEBUG)
    app.debug = True
    # app.env= "development"
    # s_handler = logging.StreamHandler()
    # s_handler.setLevel(logging.DEBUG)
    # app.logger.addHandler(s_handler)

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
    # mutation.set_field("markDone", resolve_mark_done)
    # mutation.set_field("deleteTodo", resolve_delete_todo)
    # mutation.set_field("updateDueDate", resolve_update_due_date)

    datetime_scalar = ScalarType("Datetime")
    type_defs = load_schema_from_path("schema.graphql")
    
    schema = make_executable_schema(
        type_defs, query, mutation, datetime_scalar, snake_case_fallback_resolvers,viewer,listChannelConnection
    )
     
    @datetime_scalar.serializer
    def serialize_datetime(value):
        return value.isoformat()
    
    @datetime_scalar.value_parser
    def parse_datetime_value(value):
        return datetime.fromisoformat(value)

    @app.route("/graphql", methods=["GET"])
    def graphql_playground():
        return PLAYGROUND_HTML, 200

    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        data = request.get_json()
        # print("in data: {}".format(data))

        success, result = graphql_sync(
            schema,
            data,
            context_value=request,
            debug=app.debug
        )
        print("in result: {}".format(result))

        status_code = 200 if success else 400
        return jsonify(result), status_code

    return app