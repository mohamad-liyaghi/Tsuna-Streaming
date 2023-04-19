The Tsuna Streaming "core" app provides common functionality that is shared across different parts of the application.

### Models

- `BaseContentModel`: This is the base model for all content models, such as `Video` and `Music`. It contains common fields and methods across all subclasses.

- `BaseTokenModel`: This model has only one `Token` field that is shared across all other models. When an object is saved, `create_unique_token()` is called to generate a unique token specific to that model.

#### BaseContentModel methods

1. `get_content_model_by_name()`: Returns a content model (like `Video`) by its name.
2. `get_model_content_type()`: Returns the content type instance of a content model.
3. `get_model_content_type_id()`: Returns the content type ID of a content model.
4. `get_viewer_count()`: Returns the viewer count of a content object (total viewers in DB and cache).
5. `get_votes_count()`: Returns the vote count of a content object (total in DB and cache).
6. `save()`: Checks permissions for saving an object.

### Views

The "core" app includes two basic views for handling errors:
- `handler404(request, exception)`: Handles 404 errors by returning a custom error page.
- `handler500(request)`: Handles 500 errors by returning a custom error page.

## Celery

### `send_email`

There is a background task in the project responsible for sending custom email content to users.

## Utils

- `create_unique_token()`: This method generates a unique token for objects and is called within the save method of `BaseTokenModel`.