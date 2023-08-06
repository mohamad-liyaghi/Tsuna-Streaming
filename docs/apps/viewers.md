# Viewers Application Documentation

## Description
The Viewers application is responsible for tracking viewer interactions with channels and content objects. It allows users to view and manage viewer records, and provides functionality to store viewer information in both the cache and the database.

When a viewer interacts with a content object, a viewer record is created, which includes the user, channel, date, and content object associated with the interaction. First, the viewer record is stored in the cache for efficient retrieval and processing. Then, a Celery task is triggered to insert the viewer record into the database for permanent storage.

The application also includes decorators to ensure that a viewer record exists before performing certain actions, as well as a signal to delete viewer records associated with a deleted object.

## Models

### Viewer
The `Viewer` model represents a viewer's interaction with a content object. It includes the following fields:
- `user`: The user associated with the viewer interaction.
- `channel`: The channel associated with the viewer interaction.
- `date`: The date of the viewer interaction.
- `content_object`: The content object associated with the viewer interaction.

## Manager

### ViewerManager
The `ViewerManager` is a manager class that inherits from `BaseCacheManager`. It provides functionality for managing viewer records in the cache. It includes methods for creating, retrieving, and updating viewer records.

## Decorators

### ensure_viewer_exists
The `ensure_viewer_exists` decorator checks if a viewer record does not exist and creates a new one in the cache if necessary. This decorator can be applied to functions or methods that require a viewer record to be present.

## Celery Tasks

### insert_viewer_into_db
The `insert_viewer_into_db` Celery task is responsible for inserting viewer records from the cache into the database.

## Signals

### delete_object_viewers_after_deleting
The `delete_object_viewers_after_deleting` signal is triggered when an object is deleted. It deletes all viewer records associated with the deleted object. This signal ensures that viewer records are properly cleaned up when an object is removed from the system.