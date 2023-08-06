# Votes Application Documentation

## Description
The Votes application provides functionality for users to vote on content objects. Votes are initially created in the cache for efficient retrieval and processing, and then stored in the database for permanent storage. The application includes views for checking vote status, creating and deleting votes, listing users who voted on an object, and handling related signals and Celery tasks.

## Models

### Vote
The `Vote` model represents a user's vote on a content object. It includes the following fields:
- `user`: The user who made the vote.
- `choice`: The choice of the vote (e.g., upvote, downvote).
- `channel`: The channel associated with the vote.
- `date`: The date the vote was made.
- `content_object`: The content object the vote is associated with.

## Views

### VoteStatusView
The `VoteStatusView` allows users to check if they have voted on an object or not. It handles the following HTTP methods:
- `GET`: Checks the vote status for a user on an object.

### VoteCreateView
The `VoteCreateView` allows users to create a vote for an object. It handles the following HTTP methods:
- `POST`: Creates a vote for an object.

### VoteDeleteView
The `VoteDeleteView` allows users to delete their vote for an object. It handles the following HTTP methods:
- `DELETE`: Deletes a user's vote for an object.

### VoteListView
The `VoteListView` allows users to retrieve a list of users who voted on an object. It handles the following HTTP methods:
- `GET`: Retrieves a list of users who voted on an object.


## Signals

### delete_vote_after_deleting_object
The `delete_vote_after_deleting_object` signal is triggered when an object is deleted. It deletes all votes associated with the deleted object. This signal ensures that vote records are properly cleaned up when an object is removed from the system.

## Celery Tasks

### remove_object_votes
The `remove_object_votes` Celery task is responsible for removing votes associated with a deleted object from the cache.

### insert_vote_into_db
The `insert_vote_into_db` Celery task is responsible for inserting votes from the cache into the database.

### delete_unvoted_from_db
The `delete_unvoted_from_db` Celery task is responsible for deleting unvoted records from the database.

## Tests
Tests for the Votes application can be run with the following command:

```
pytest apps/votes
```