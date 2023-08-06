# Comments Application Documentation

## Description
The Comments application provides functionality for managing comments on content objects. Users can create, retrieve, update, and delete comments, as well as pin comments as channel staff. The application also includes exception handling for comment-related operations.

## Model

### Comment
The `Comment` model represents a comment made by a user on a content object. It includes the following fields:
- `parent`: The parent comment, if the comment is a reply to another comment.
- `user`: The user who made the comment.
- `body`: The content of the comment.
- `date`: The date the comment was created.
- `edited`: A flag indicating whether the comment has been edited.
- `pinned`: A flag indicating whether the comment is pinned by channel staff.
- `content_object`: The content object the comment is associated with.

## Exceptions

### CommentNotAllowed
The `CommentNotAllowed` exception is raised when a user attempts to perform an action on a comment that they are not allowed to perform. This exception is raised when a user attempts to perform an action on a comment that they do not own.

## Signals

### delete_object_comments_after_deleting
The `delete_object_comments_after_deleting` signal is triggered when an object is deleted. It deletes all comments associated with the deleted object. This signal ensures that comment records are properly cleaned up when an object is removed from the system.

## Views

### CommentListCreateView
The `CommentListCreateView` allows users to retrieve a list of comments for an object and create new comments. It handles the following HTTP methods:
- `GET`: Retrieves a list of comments for an object.
- `POST`: Creates a new comment or reply.

### CommentDetailView
The `CommentDetailView` allows users to retrieve, update, and delete a specific comment. It handles the following HTTP methods:
- `GET`: Retrieves a specific comment and its replies.
- `PUT`: Updates a specific comment by its owner.
- `PATCH`: Updates a specific comment by its owner.
- `DELETE`: Deletes a specific comment by its owner.

### CommentPinView
The `CommentPinView` allows channel staff to pin a comment. It handles the following HTTP methods:
- `PUT`: Pins a comment by channel staff.
- `PATCH`: Pins a comment by channel staff.

## Tests
Tests for the Comments application can be run with the following command:

```
pytest apps/comments
```