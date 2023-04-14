## Overview
The "Videos" application is a part of the "Tsuna Streaming" project that handles the video management system. This application allows users to upload, view and manage videos on their channel or any other channels they have permission to. 

## Model
The main model used in this application is the `Video` model. This model holds all the information related to a video uploaded by a user. 

## Views
The following views are supported by the application:

### Channel Videos List/Create
This view allows users to view all the videos uploaded on a channel, as well as create new videos for that channel.

### Video Detail/Update/Delete
This view allows users to view, admins to update and delete videos.

## Throttling
To avoid spamming requests for videos, the application implements throttling which limits the number of requests one can make within a certain period of time.

## Signals
The application sends a signal to notify the channel owner when a new video is added to their channel.

## Permissions
The application has permissions for views to ensure that only authorized users can perform actions on videos.

## Mixin
The application uses a mixin to get the channel object before executing a view. This ensures that the channel exiests.

## Manager
The application includes a manager method that retrieves only published videos.


## Tests
The Videos application includes automated tests that you can run them by typing this command:

```
$ pytest v1/videos/
``` 