# Videos Application Documentation

## Description
The Videos application provides functionality for managing videos within a channel. Users can create, retrieve, update, and delete videos. The application includes a custom model for videos, along with a model validator and a signal for additional functionality. The provided views allow users to perform various operations on videos.

## Model

### Video
The `Video` model inherits from the `AbstractContent` model and represents a video within a channel. It includes the following fields:
- `user`: The user who uploaded the video.
- `channel`: The channel the video belongs to.
- Additional fields inherited from the `AbstractContent` model.

### Model Validator

#### validate_video_size
The `validate_video_size` validator checks if the size of the video file does not exceed the maximum limit. Premium users are allowed to upload videos twice as large as regular users.

## Signals

### notify_video_creation
The `notify_video_creation` signal is triggered when a new video is created. It sends an email notification to relevant parties to notify them about the newly created video.

## Views

### VideoListCreateView
The `VideoListCreateView` allows users to retrieve a list of videos in a channel and create new videos. It inherits from the `ContentListCreateView` and handles the following HTTP methods:
- `GET`: Retrieves a list of videos in a channel.
- `POST`: Creates a new video.

### VideoDetailView
The `VideoDetailView` allows users to retrieve, update, and delete a specific video. It inherits from the `ContentDetailView` and handles the following HTTP methods:
- `GET`: Retrieves a specific video.
- `PUT`: Updates a specific video by a channel admin.
- `PATCH`: Updates a specific video by a channel admin.
- `DELETE`: Deletes a specific video by channel admins.

Please refer to the individual view classes for more detailed documentation on their endpoints, request/response formats, and required permissions.

## Tests
Tests for the Videos application can be run with the following command:

```
pytest apps/videos
```