The Comments app enables users to leave comments on uploaded contents, including videos, music, and other media files available on Tsuna Streaming platform. 

## Models

### `Comment`

The `Comment` model represents a comment made by a user on a particular piece of content. 

## Views

### `CommentListCreateView`

This view allows users to see all existing comments and create new ones or reply. The GET method returns a list of all comments for an object, sorted by creation date. The POST method creates/replies a new comment associated with the object specified in the url.

### `CommentDetailView`

This view allows users to see a single comment and its replies. It takes an `token` parameter which specifies the token of the comment to retrieve.

### `CommentPinView`

This view allows admins to pin a comment to the top of a list of comments. 

## Signals

When a user deletes an object (e.g., a video), the associated comments should be deleted as well. This behavior is implemented via a Celery task that removes all comments associated with the deleted object.

## Exceptions

If commenting is disabled for a particular content model, attempting to add a comment will raise a `CommentNotAllowed` exception.

## Tests

## Testing
The application's tests can be run using the following command: 

```
$ pytest apps/comments
```