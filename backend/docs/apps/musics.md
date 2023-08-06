# Musics Application Documentation

## Description
The Musics application provides functionality for managing music tracks within a channel. Users can create, retrieve, update, and delete music tracks. The application includes a custom model for music tracks, along with a model validator and a signal for additional functionality. The provided views allow users to perform various operations on music tracks.

## Model

### Music
The `Music` model inherits from the `AbstractContent` model and represents a music track within a channel. It includes the following fields:
- `user`: The user who uploaded the music track.
- `channel`: The channel the music track belongs to.
- Additional fields inherited from the `AbstractContent` model.

### Model Validator

#### validate_music_size
The `validate_music_size` validator checks if the size of the music file does not exceed the maximum limit. Premium users are allowed to upload music tracks that are twice as large as those allowed for regular users.

## Signals

### notify_music_creation
The `notify_music_creation` signal is triggered when a new music track is created. It sends an email notification to relevant parties to notify them about the newly created music track.

## Views

### MusicListCreateView
The `MusicListCreateView` allows users to retrieve a list of music tracks in a channel and create new music tracks. It inherits from the `ContentListCreateView` and handles the following HTTP methods:
- `GET`: Retrieves a list of music tracks in a channel.
- `POST`: Creates a new music track.

### MusicDetailView
The `MusicDetailView` allows users to retrieve, update, and delete a specific music track. It inherits from the `ContentDetailView` and handles the following HTTP methods:
- `GET`: Retrieves a specific music track.
- `PUT`: Updates a specific music track by a channel admin.
- `PATCH`: Updates a specific music track by a channel admin.
- `DELETE`: Deletes a specific music track by channel admins.

Please refer to the individual view classes for more detailed documentation on their endpoints, request/response formats, and required permissions.

## Tests
Tests for the musics application can be run with the following command:

```
pytest apps/musics
```
