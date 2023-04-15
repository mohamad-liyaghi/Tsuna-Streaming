The "Votes" application of the "Tsuna Streaming" project handles the Upvoting/Downvoting action in this project.

## Model: Vote
The `Vote` model is a generic model that can be used in all models and allows users to Upvote/Downvote an object.

## Views
The "Votes" application provides two views for handling votes - `VoteView` and `VoteListView`.

### VoteView
The `VoteView` allows users to create, retrieve, and delete their own votes. It supports the following methods:
- `GET`: Check vote status.
- `POST`: Create a new vote.
- `DELETE`: Delete a vote.

### VoteListView
The `VoteListView` allows users to list all votes for a given object. It supports only the `GET` method.

## Tasks
As per the design, the application uses Celery for inserting votes from cache to the database. The task is performed asynchronously to allow for better performance. The following Celery task is used in the "Votes" application:
- **insert_vote_into_db**: This task inserts all the votes stored in the cache into the database.

## Signals
- **delete_object_votes_after_deleting**: This signal removes all votes associated with an object when it is deleted.

## Manager
The "Votes" application's manager is responsible for handling interactions with cache. It provides the following method:
- **get_from_cache**: This method retrieves a vote from the cache/db.
- **create_in_cache**: This method creates a new vote in cache so Celery inserts it into db.

## Tests
This application includes automated tests that you can run them by typing this command:

```
$ pytest v1/votes/
``` 