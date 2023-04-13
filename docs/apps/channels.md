# Channels Application Docs

## Overview
The "Channels" application is responsible for managing user-created channels within the Tsuna Streaming project. The application allows users to create, edit, and delete their own channels, as well as view a list of all available channels. 

<hr>

## Views
The "Channels" application includes the following views:

- **Add Channel**: Allows users to create a new channel. Normal users are limited to creating up to 5 channels, while premium and admin users can create up to 10 channels.
- **List Channels**: Displays a list of all available channels.
- **Update Channel**: Allows users to edit an existing channel they own.
- **Channel Detail**: Displays detailed information about a specific channel.
- **Delete Channel**: Allows users to delete a channel they own.

## Signal
A signal is used to notify users when a new channel is created. This signal sends an email notification to the channel owner.

## Exceptions
Normal users can create up to 5 channels, while premium and admin users can create up to 10 channels. Attempting to exceed this limit will result in an exception being raised.


## Testing
The application's tests can be run using the following command: 

```
$ pytest v1/channels
```