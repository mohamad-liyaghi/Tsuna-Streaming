# Channel Subscribers Application Documentation

Table of Contents:
- [Description](#description)
- [Models](#models)
  - [ChannelSubscriber](#channelsubscriber)
- [Views](#views)
  - [SubscriberStatusView](#subscriberstatusview)
  - [SubscriberCreateView](#subscribercreateview)
  - [SubscriberDeleteView](#subscriberdeleteview)
  - [SubscriberListView](#subscriberlistview)
- [Model Managers](#model-managers)
  - [ChannelSubscriberManager](#channelsubscribermanager)
- [Services](#services)
  - [ChannelSubscriberService](#channelsubscriberservice)
- [Signals](#signals)
  - [create_subscriber_after_creating_channel](#create-subscriber-after-creating-channel)
- [Celery Tasks](#celery-tasks)
  - [insert_subscriber_from_cache_into_db](#insert-subscriber-from-cache-into-db)
  - [delete_unsubscribed_from_db](#delete-unsubscribed-from-db)
- [Tests](#tests)

## Description
The Channel Subscribers application allows users to subscribe to channels and follow their content. To optimize performance, subscribers are first created in the cache and then stored in the database using a Celery task. This application provides views for checking subscriber status, creating subscribers, deleting subscribers, and listing subscribers for a channel.

## Models

### ChannelSubscriber
The `ChannelSubscriber` model represents a subscriber for a channel. The fields are as follows:

- `channel`: A relationship to the `Channel` model.
- `user`: A relationship to the `User` model.
- `date`: The date when the subscriber was created.

## Views

### SubscriberStatusView
The `SubscriberStatusView` is responsible for checking whether a user is subscribed to a channel or not. It accepts a GET request.

- **Responses**:
  - `200 OK`: Return whether the user is subscribed or not.
  - `401 Unauthorized`: User is not authenticated.
  - `404 Not Found`: Channel not found.

### SubscriberCreateView
The `SubscriberCreateView` is responsible for creating a new subscriber for a channel. It accepts a POST request.

- **Responses**:
  - `200 OK`: Successfully created the subscriber.
  - `401 Unauthorized`: User is not authenticated.
  - `403 Forbidden`: User is already subscribed to this channel.
  - `404 Not Found`: Channel not found.

### SubscriberDeleteView
The `SubscriberDeleteView` is responsible for deleting a subscriber from a channel. It accepts a DELETE request.

- **Responses**:
  - `204 No Content`: Successfully deleted the subscriber.
  - `401 Unauthorized`: User is not authenticated.
  - `403 Forbidden`: User has not subscribed yet.
  - `404 Not Found`: Channel not found.

### SubscriberListView
The `SubscriberListView` is responsible for listing all the subscribers for a channel. It accepts a GET request.

- **Responses**:
  - `200 OK`: Successfully retrieved the list of subscribers.
  - `401 Unauthorized`: User is not authenticated.

## Model Managers

### ChannelSubscriberManager
The `ChannelSubscriberManager` is a model manager that inherits from the `BaseCacheManager` class. It provides methods for CRUD operations in the cache.

## Services

### ChannelSubscriberService
The `ChannelSubscriberService` is a service class that inherits from the `CacheService` class. It provides operations in the cache, such as creating and deleting subscribers.

## Signals

### create_subscriber_after_creating_channel
This signal is triggered when a new channel is created. It creates a new subscriber for the channel, with the subscriber being the channel owner.

## Celery Tasks

### insert_subscriber_from_cache_into_db
This task is responsible for inserting subscribers from the cache into the database.

### delete_unsubscribed_from_db
This task is responsible for deleting unsubscribed users from the database.

## Tests
Tests for the Channel Subscribers application can be run with the following command:

```
pytest apps/channel_subscribers
```