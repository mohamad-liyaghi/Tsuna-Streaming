# Channels Application Documentation

Table of Contents:
- [Description](#description)
- [Models](#models)
  - [Channel](#channel)
- [Views](#views)
  - [ChannelListCreateView](#channellistcreateview)
  - [ChannelDetailView](#channeldetailview)
- [Signals](#signals)
  - [notify_channel_creation](#notify-channel-creation)
- [Tests](#tests)

## Description
The Channels application empowers users to create personalized channels and add content to them. It offers the flexibility for users to subscribe to channels of their interest and even appoint administrators for their own channels. To ensure a balanced system, the application strictly adheres to channel creation limits based on user roles: normal users are entitled to create up to 5 channels, whereas premium users enjoy the privilege of creating up to 10 channels. This approach promotes engagement and active participation while maintaining a fair and seamless user experience.
## Models

### Channel
The `Channel` model represents a channel created by users. The fields are as follows:

- `title`: Title of the channel.
- `description`: Description of the channel.
- `avatar`: Avatar image for the channel.
- `thumbnail`: Thumbnail image for the channel.
- `owner`: The user who owns the channel (foreign key to the `User` model).
- `date_created`: Date when the channel was created.
- `is_verified`: A boolean field indicating if the channel is verified.

## Views

### ChannelListCreateView
- Description: List channels that the user is the owner or an admin.
- HTTP Methods:
  - GET: List channels owned or administered by the user.
  - POST: Create a new channel.
- Responses:
  - 200 OK: List of channels owned or administered by the user.
  - 201 Created: Successfully created a new channel.
  - 400 Bad Request: Invalid data in the request.
  - 401 Unauthorized: Authentication required.
  - 403 Permission Denied: User is not authorized to perform the operation.

### ChannelDetailView
- Description: Retrieve, update, or delete a specific channel.
- HTTP Methods:
  - GET: Retrieve the details of a channel.
  - PUT: Update the channel information [Channel staff only].
  - PATCH: Update the channel information [Channel staff only].
  - DELETE: Delete a channel [Channel staff only].
- Responses:
  - 200 OK: Detail page of the channel.
  - 204 No Content: Successfully deleted the channel.
  - 400 Bad Request: Invalid data in the request.
  - 401 Unauthorized: Authentication required.
  - 403 Permission Denied: User is not authorized to perform the operation.
  - 404 Not Found: Channel not found.

## Signals

### notify_channel_creation
- Description: Notify relevant users when a new channel is created [by email].

## Tests

Tests for the Channels application can be found in the `channels/tests` directory. The tests cover various scenarios and functionalities of the Channel models, views, and signals. To run the tests, you can use the following command:

```
pytest apps/channels
```

