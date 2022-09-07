
from ariadne import ObjectType
viewer = ObjectType("Viewer")
listChannelConnection = ObjectType("ListChannelConnection")

from app.data import ListChannelConnection, channel

@viewer.field('channels')
def resolve_channels(viewer,info,**kwargs):
    print("viewer")
    print(viewer)

    print("info")
    print(info)
    print(info.parent_type)
    limit = kwargs.get("limit")
    nextToken = kwargs.get("nextToken")
    
    return ListChannelConnection

@listChannelConnection.field('items')
def resolve_items(viewer, *args):

    return channel