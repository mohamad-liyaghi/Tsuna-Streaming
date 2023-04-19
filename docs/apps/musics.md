## Overview
The "Musics" application is a part of the "Tsuna Streaming" project that handles the music management system. This application allows users to upload, view and manage musics on their channel or any other channels they have permission to. 

## Model
The main model used in this application is the `Music` model. This model holds all the information related to a video uploaded by a user. 
Same as `Video` model, this model inherits from BaseContentModel.

## Views
The following views are supported by the application:

### Channel Musics List/Create
This view allows users to view all the musics uploaded on a channel, as well as create new musics for that channel.

### Music Detail/Update/Delete
This view allows users to view, for admins to update and delete musics.

## Signals
The application sends a signal to notify the channel owner when a new music is added to their channel.

## Permissions
The application has permissions for views to ensure that only authorized users can perform actions on musics.

## Mixin
The application uses a mixin to get the channel object before executing a view. This ensures that the channel exiests.


## Tests
The Musics application includes automated tests that you can run them by typing this command:

```
$ pytest apps/musics/
``` 