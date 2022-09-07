import asyncio
import datetime
from logging import exception
from google.api_core import retry
from tkinter import E
from ariadne import convert_kwargs_to_snake_case, SubscriptionType


subscription = SubscriptionType()


from concurrent.futures import TimeoutError
import json
from tokenize import String
from google.cloud import pubsub_v1


project_id = "graphql-gcp"
subscription_id = "app-messaging-sub"
# Number of seconds the subscriber should listen for messages
timeout = 4

from asgiref.sync import sync_to_async
NUM_MESSAGES = 1

def blocking_function(seconds: int,subscriber,subscription_path):
    try:
        response = subscriber.pull(
            request={"subscription": subscription_path, "max_messages": NUM_MESSAGES}, retry=retry.Retry(deadline=300),
        )
        return response
    except Exception as e:
        print(e)
    return f"Finished in {seconds} seconds"

@subscription.source("messages")
@convert_kwargs_to_snake_case        
async def messages_source(obj, info, user_id):
    while True:
        print(datetime.datetime.now())
        with  pubsub_v1.SubscriberClient() as subscriber:
            subscription_path = subscriber.subscription_path(project_id, subscription_id)
            response = {}
            response = await sync_to_async(blocking_function)(5,subscriber,subscription_path)
            
            if not "received_messages" in response or len(response.received_messages) == 0:
                continue

            ack_ids = []
   
            for received_message in response.received_messages:
                message = received_message.message.data
                msg = message.decode('ascii')
                dictMessage = json.loads(msg)
                if dictMessage["recipient_id"] == user_id:
                   yield dictMessage
                print(dictMessage)
                
                ack_ids.append(received_message.ack_id)
               

            # Acknowledges the received messages so they will not be sent again.
            if len(ack_ids) > 0:
                subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": ack_ids}
                )
            
            print(
                f"Received and acknowledged {len(response.received_messages)} messages from {subscription_path}."
            )
    
@subscription.field("messages")
@convert_kwargs_to_snake_case
async def messages_resolver(message, info, user_id):
    return message