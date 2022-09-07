import json
import os
from typing import Callable
from ariadne import ObjectType, convert_kwargs_to_snake_case
import datetime
from google.cloud import firestore, pubsub_v1
from pkg_resources import working_set
from core import utils
from concurrent import futures

mutation = ObjectType("Mutation")

project_id = "graphql-gcp"
topic_id = "app-messaging"

def resolve_todos(obj, info):
    try:
        #todos = [todo.to_dict() for todo in Todo.query.all()]
        todos = [{"id": "Paris", "description": "The city of lights", "completed": True, "dueDate":"2022-07-14"},
                 {"id": "Paris2", "description": "The city of joy", "completed": True, "dueDate":"2022-07-14"}]
        payload = {
            "success": True,
            "todos": todos
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

def resolve_viewer(obj, info):
    try:
        userProfile = {
                "title": "user",
                "display_name": "shaker ahmed",
                "phone": "891231232",
                "skype": "",
                "status_text": "",
                "status_emoji": "",
                "status_expiration": utils.iso_utc_now(),
                "avatar_hash": "", # Not sure if I want this yet? These would be hardcoded Avatars.
                "email": "shaker@gmail.com",
                "image_original": "", # This is the original image with original huge size
                "image24": "", # Resized image 24x24
                "image32": "", # Resized image 32x32
                "image48": "" # Resized image 48x48
            }
        viewer = {
            "id":15,
            "workspace": "100",
            "username": "shaker",
            "full_name": "shaker ahmed",
            "device_tokens": ["token1","token2"],
            "team": "development",
            "profile": userProfile,
            "role": "role1",
            "tz": "tz1", # 	A human-readable string for the geographic timezone-related region this user has specified in their account.
            "tz_label": "tz_label", # Describes the commonly used name of the tz timezone.
            "tz_offset": "tz_offset", # Indicates the number of seconds to offset UTC time by for this user's tz.
            "avatar_url": "avatar_url", # Deprecated use profile.imageOriginal
            "is_admin": True, # Indicates whether the user is an Admin of the current workspace.
            "is_owner": True, # 	Indicates whether the user is an Owner of the current workspace.
            "is_primary_owner": True, # Indicates whether the user is the Primary Owner of the current workspace.
            "is_restricted": False,
            "is_active": True,
            "updated": utils.iso_utc_now(), # An AWSDateTime indicating when the user object was last updated.
            "locale": "utc+6", # 	Contains a IETF language code that represents this user's chosen display language. Useful for localizing your apps.
            "location_filter_on": "washington",
            "location_id": "1212",
            "location_ids": ["12212",'123123','12312312321']
        } 
        payload = viewer      
    except Exception as error:
        payload = {
            "errors": [str(error)]
        }
    return payload

def resolve_getUser(obj, info,input):
    # print("user_id")
    # print("user_id")
    # print(input.get("userId"))
    try:
        userProfile = {
                "title": "user",
                "display_name": "shaker ahmed",
                "phone": "891231232",
                "skype": "",
                "status_text": "",
                "status_emoji": "",
                "status_expiration": utils.iso_utc_now(),
                "avatar_hash": "", # Not sure if I want this yet? These would be hardcoded Avatars.
                "email": "shaker@gmail.com",
                "image_original": "", # This is the original image with original huge size
                "image24": "", # Resized image 24x24
                "image32": "", # Resized image 32x32
                "image48": "" # Resized image 48x48
            }
        user = {
            "id":15,
            "workspace": "100",
            "team": "development",
            "profile": userProfile,
            "deleted":False,
            "role": "role1",
            "is_active": True,
            "location_filter_on": "washington",
            "location_id": "1212",
            "location_ids": ["12212",'123123','12312312321'],
            "tz": "tz1", # 	A human-readable string for the geographic timezone-related region this user has specified in their account.
            "tz_label": "tz_label", # Describes the commonly used name of the tz timezone.
            "tz_offset": "tz_offset", # Indicates the number of seconds to offset UTC time by for this user's tz.
            "avatar_url": "avatar_url", # Deprecated use profile.imageOriginal
            "is_admin": True, # Indicates whether the user is an Admin of the current workspace.
            "is_owner": True, # 	Indicates whether the user is an Owner of the current workspace.
            "is_primary_owner": True, # Indicates whether the user is the Primary Owner of the current workspace.
            "is_restricted": False,
            "is_bot": False, # Indicates whether the user is actually a bot user.
            "is_stranger": False,
            "updated": utils.iso_utc_now(), # An AWSDateTime indicating when the user object was last updated.
            "locale": "utc+6", # 	Contains a IETF language code that represents this user's chosen display language. Useful for localizing your apps.
            "last_active_at":utils.iso_utc_now()
        }  
        payload = user     
    except Exception as error:
        payload = {
            "errors": [str(error)]
        }
    return payload

@convert_kwargs_to_snake_case
def resolve_todo(obj, info, todo_id):
    try:
        todo = {"id": "Paris", "description": "The city of lights", "completed": True, "dueDate": "2022-07-14"}
        # print("todo_id : {}".format(todo_id))
        payload = {
            "success": True,
            "todo": todo
        }

    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": [f"Todo matching id {todo_id} not found"]
        }

    return payload

def resolve_getWorkspace(self,info, input):
    workspace_id = input.get("id")
    app = self.utils.dynamodb_get_item(
          self.table_name, consistent_read=True, id=workspace_id, sortKey="Workspace"
      )
    if app is None:
        raise Exception.NotFoundError(
            f"Workspace with ID {workspace_id} does not exist"
        )
    if app.get("active") is False:
        raise Exception.NotFoundError(
          f"Workspace with ID {workspace_id} was deleted"
        )
    return app

def resolve_getTenantWorkspace(obj, info, input):
    tenant_id = input.get("tenantId")
    app_id = input.get("appId")
    
    now = utils.iso_utc_now()
    
    workspace = dict(
        id="10",
        name="jhon",
        email="jhon@gmail.com",
        description="tets description",
        secrets="",
        created_at= now,
        updated_at=now,
        active=True,
        tenant_id="123",
        app_id="app-1",
        __typename="Workspace"
    )
    return workspace

def resolve_getChannel(obj, info, input):
    channel_id = input.get("channelId")
    
    now = utils.iso_utc_now()
    
    channel = dict(
        id="15",
        name="channel",
        workspace="workspace",
        name_normalized="namenormalized",
        description="description",
        is_private= False, # means the conversation is privileged between two or more members. Meet their privacy expectations.
        is_read_only= False, # means the conversation can't be written to by typical users. Admins may have the ability.
        is_archived= True, # indicates a conversation is archived. Frozen in time.
        is_channel= False, # indicates whether a conversation is a public channel. Everything said in a public channel can be read by anyone else belonging to a workspace. is_private will be false. Check both just to be sure, why not?
        is_group=True, # means the channel is a private channel. is_private will also be true.
        is_im=False, # means the conversation is a direct message between two distinguished individuals or a user and a bot. Yes, it's an is_private conversation.
        is_mpim=True, # represents an unnamed private conversation between multiple users. It's an isPrivate kind of thing.
        is_member=True, # indicates the user or bot user making the API call is itself a member of the conversation.
        read_only=True,
        created_at=now,
        last_read=now, # is the timestamp for the last message the calling user has read in this channel.
        unread_count_display= 12,
        member_count=12,
        message_count=3,
        __typename="Channel"
    )

    return channel 

def getUser():
    userProfile = {
                "title": "user",
                "display_name": "shaker ahmed",
                "phone": "891231232",
                "skype": "",
                "status_text": "",
                "status_emoji": "",
                "status_expiration": utils.iso_utc_now(),
                "avatar_hash": "", # Not sure if I want this yet? These would be hardcoded Avatars.
                "email": "shaker@gmail.com",
                "image_original": "", # This is the original image with original huge size
                "image24": "", # Resized image 24x24
                "image32": "", # Resized image 32x32
                "image48": "" # Resized image 48x48
            }
    user = {
            "id":15,
            "workspace": "100",
            "team": "development",
            "profile": userProfile,
            "deleted":False,
            "role": "role1",
            "is_active": True,
            "location_filter_on": "washington",
            "location_id": "1212",
            "location_ids": ["12212",'123123','12312312321'],
            "tz": "tz1", # 	A human-readable string for the geographic timezone-related region this user has specified in their account.
            "tz_label": "tz_label", # Describes the commonly used name of the tz timezone.
            "tz_offset": "tz_offset", # Indicates the number of seconds to offset UTC time by for this user's tz.
            "avatar_url": "avatar_url", # Deprecated use profile.imageOriginal
            "is_admin": True, # Indicates whether the user is an Admin of the current workspace.
            "is_owner": True, # 	Indicates whether the user is an Owner of the current workspace.
            "is_primary_owner": True, # Indicates whether the user is the Primary Owner of the current workspace.
            "is_restricted": False,
            "is_bot": False, # Indicates whether the user is actually a bot user.
            "is_stranger": False,
            "updated": utils.iso_utc_now(), # An AWSDateTime indicating when the user object was last updated.
            "locale": "utc+6", # 	Contains a IETF language code that represents this user's chosen display language. Useful for localizing your apps.
            "last_active_at":utils.iso_utc_now()
        }  
    
    return user

@convert_kwargs_to_snake_case
def resolve_listUsers(obj, info, input):
    limit = input.get("limit")
    next_token = input.get("next_token")
    
    project_id = os.environ.get('PROJECT_NAME', None)
    db = firestore.Client(project=project_id)
    batch = db.batch()
    cities_ref = db.collection(u'cities')
    if next_token == "":
        first_query = cities_ref.limit(limit)
        result = first_query.stream()
    
    else:
        doc = cities_ref.document(next_token).get()
        next_query = (
            cities_ref
            .start_after(doc)
            .limit(limit)
            )
        result = next_query.stream()
    
    resultList = list(result)
    lastDoc = resultList[-1]
    availableMore = (
            cities_ref
            .start_after(lastDoc)
            .limit(1)
           )
    next_token = ""
    if len(availableMore.get()) >= 1:
        next_token =  lastDoc.id
    
    items = []
    for doc in resultList:
        _doc = doc.to_dict()
        items.append(_doc)
    print("items")
    print(items)
    print()
    user = getUser()
    # obj = dict(
    #      items= items,
    #      next_token=next_token
    # )
    obj = dict(
         items= [user],
         next_token=next_token
    )
           
    return obj


def resolve_listChannels(obj, info, input):
    limit = input.get("limit")
    next_token = input.get("nextToken")
    
    now = utils.iso_utc_now()
    
    channel = dict(
        id="15",
        name="channel",
        workspace="workspace",
        name_normalized="namenormalized",
        description="description",
        is_private= False, # means the conversation is privileged between two or more members. Meet their privacy expectations.
        is_read_only= False, # means the conversation can't be written to by typical users. Admins may have the ability.
        is_archived= True, # indicates a conversation is archived. Frozen in time.
        is_channel= False, # indicates whether a conversation is a public channel. Everything said in a public channel can be read by anyone else belonging to a workspace. is_private will be false. Check both just to be sure, why not?
        is_group=True, # means the channel is a private channel. is_private will also be true.
        is_im=False, # means the conversation is a direct message between two distinguished individuals or a user and a bot. Yes, it's an is_private conversation.
        is_mpim=True, # represents an unnamed private conversation between multiple users. It's an isPrivate kind of thing.
        is_member=True, # indicates the user or bot user making the API call is itself a member of the conversation.
        read_only=True,
        created_at=now,
        last_read=now, # is the timestamp for the last message the calling user has read in this channel.
        unread_count_display= 12,
        member_count=12,
        message_count=3,
        __typename="Channel"
    )
    
    obj = dict(
         items= [channel],
         next_token="token12"
    )
           
    return obj

def resolve_openConversation(obj, info, input):
    channel_id = input.get("channelId")
    user_ids = input.get("userIds")
    
    now = utils.iso_utc_now()
    
    channel = dict(
        id="15",
        name="channel",
        workspace="workspace",
        name_normalized="namenormalized",
        description="description",
        is_private= False, # means the conversation is privileged between two or more members. Meet their privacy expectations.
        is_read_only= False, # means the conversation can't be written to by typical users. Admins may have the ability.
        is_archived= True, # indicates a conversation is archived. Frozen in time.
        is_channel= False, # indicates whether a conversation is a public channel. Everything said in a public channel can be read by anyone else belonging to a workspace. is_private will be false. Check both just to be sure, why not?
        is_group=True, # means the channel is a private channel. is_private will also be true.
        is_im=False, # means the conversation is a direct message between two distinguished individuals or a user and a bot. Yes, it's an is_private conversation.
        is_mpim=True, # represents an unnamed private conversation between multiple users. It's an isPrivate kind of thing.
        is_member=True, # indicates the user or bot user making the API call is itself a member of the conversation.
        read_only=True,
        created_at=now,
        last_read=now, # is the timestamp for the last message the calling user has read in this channel.
        unread_count_display= 12,
        member_count=12,
        message_count=3,
        __typename="Channel"
    )

    return channel 

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)
publish_futures = []
def get_callback(
    publish_future: pubsub_v1.publisher.futures.Future, data: str
) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
    def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
        try:
            # Wait 60 seconds for the publish call to succeed.
            print(publish_future.result(timeout=60))
        except futures.TimeoutError:
            print(f"Publishing {data} timed out.")

    return callback

@mutation.field("createMessage")
@convert_kwargs_to_snake_case
def resolve_create_message(obj, info, content, sender_id, recipient_id):
    print("call create message")
    try:
        message = {
            "content": content,
            "sender_id": sender_id,
            "recipient_id": recipient_id
        }
       
        data_str = json.dumps(message)
        data = data_str.encode("utf-8")
        
        publish_future = publisher.publish(topic_path, data)
        # Non-blocking. Publish failures are handled in the callback function.
        publish_future.add_done_callback(get_callback(publish_future, data_str))
        publish_futures.append(publish_future)
        print(datetime.datetime.now())
        futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

        print(f"Published messages with error handler to {topic_path}.")
      
        print(datetime.datetime.now())
        return {
            "success": True,
            "message": message
        }
    except Exception as error:
        return {
            "success": False,
            "errors": [str(error)]
        }
