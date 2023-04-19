# Introduction

The "Channel Subscribers" application is a part of the "Tsuna Streaming" project that handles the management of channel subscribers. Users can subscribe to channels, which will be saved in cache first and then inserted into the database using Celery. The `ChannelSubscriber` model is used for this application and there are some views for subscribing and showing list of subscribers.

# Models

- `ChannelSubscriber`: This is the only model of this app that represents a subscriber to a channel.

# Views

## SubscriberView

The `SubscriberView` allows users to subscribe or unsubscribe from a channel and show subscription status. It has three methods:

- `get`: Retrieves the subscription status for a given user and channel. Returns whether the user is currently subscribed to the channel or not
- `post`: This method handles subscription requests. It checks if the user is already subscribed to the channel. If not, it subscribes the user in cache and returns a success message. Otherwise, it returns an error message.
- `delete`: This method handles unsubscription requests. It removes the user from cache and returns a success message.

## SubscriberListView

The `SubscriberListView` provides a list of all the subscribers for a given channel. It has only one method:

- `get`: This method retrieves all the subscribers for a given channel and returns them in a JSON format.

# Celery

Celery is used to insert and delete subscribers from the database based on the data stored in cache. There are two tasks:

- `insert_subscribers`: This task inserts new subscribers into the database from cache.
- `delete_subscribers`: This task removes subscribers from the database based on the data stored in cache.

# Manager

The `ChannelSubscriberManager` class provides three methods:

- `get_from_cache`: This method checks both cache and database to retrieve a subscriber by user and channel.
- `subscribe_in_cache`: This method adds a subscriber to cache.
- `unsubscribe_in_cache`: This method removes a subscriber from cache.

# Signal

A signal is used to create a new subscriber after a channel is created.

# Tests
The application's tests can be run using the following command: 


```
$ pytest apps/channel_subscribers
```