# Introduction

`Tsuna Streaming` is a streaming system API that allows users to create their own channels, upload videos and music, and share them with others. Once users register, they can easily add content to their channels.

One of the key features of Tsuna Streaming is its flexible `Administration system`. Channel owners can easily promote other users as admins with custom permissions, allowing multiple people to collaborate on a single channel based on their permissions.

Premium users have access to additional features, such as the ability to upload larger files and create more channels than non-premium users. Users can subscribe to a membership plan in order to become premium members and unlock these exclusive privileges.

In addition to uploading and sharing media, Tsuna Streaming allows users to `subscribe` to channels, follow their favorite creators, and engage with uploaded content through `voting` and leaving `comments`.


To ensure the smooth functioning of this streaming system, <a href="docs.celeryq.dev">`Celery`</a> is used for background tasks, <a href="http://pytest.org/">`Pytest`</a> for testing, <a href="redis.io/">`Redis`</a> for caching, and <a href="docker.com/">`Docker`</a> for containerization.


<hr>

# Apps and project structure
<hr>

## Authentication and Memberships on Tsuna Streaming

### Accounts
The `Accounts` application in this project is responsible for authentication purposes. When users register, their accounts remain inactive until they verify them using a token sent to their email. Once activated, users can authorize themselves using a JWT token. You can find more information on the `Accounts` application in the <a href="https://github.com/mohamad-liyaghi/Tsuna-Streaming/blob/main/docs/apps/accounts.md">Accounts Docs</a>.<br>

### Memberships
The `Memberships` application in this project is responsible for managing user subscriptions and memberships. Once users register, they are limited in performing some actions. For example, they can only create up to 5 channels. They can view the membership plans that admins have created beforehand and subscribe to one of them to take advantage of the benefits. Once the plan expires, a celery task demotes and notifies the user. For more information, refer to the <a href='https://github.com/mohamad-liyaghi/Tsuna-Streaming/blob/main/docs/apps/memberships.md'>Documentation</a>.

<hr>

## Channel Management on Tsuna Streaming

### Channels
The `Channels` application plays a crucial role in the Tsuna Streaming project by facilitating the management of user-generated channels. This application allows users to create, edit, and delete their own channels, as well as browse through a comprehensive list of all available channels. 

While regular users can create up to 5 channels, premium users are granted the ability to create up to 10 channels, providing them with greater flexibility and control. For more details on the features and functionalities of this application, please refer to the <a href="https://github.com/mohamad-liyaghi/Tsuna-Streaming/blob/main/docs/apps/channels.md">documentation</a>.

### Channel Subscribers
The `Channel Subscribers` application another component of the Tsuna Streaming project. Users have the ability to subscribe to channels, which are initially saved in cache and then inserted into the database using Celery. The ChannelSubscriber model is implemented for this application, with several views available for subscribing and displaying the list of subscribers.

For more detailed information regarding the features and functionalities of this application, please refer to the <a href='https://github.com/mohamad-liyaghi/Tsuna-Streaming/blob/main/docs/apps/channel_subscribers.md'>documentation</a>.

### Channel Admins
The `Channel Admin` application is a vital component of the Tsuna Streaming project, which enables administrators to efficiently manage channels and content. Once a user creates a channel, administrators can promote subscribers as admins with customized permission levels for accessing or altering content details.

Upon being promoted, a background task automatically generates permissions for each content model, such as `videos` and `music`, for that particular admin. For more in-depth information regarding the features and functionalities of this application, please refer to the <a href='https://github.com/mohamad-liyaghi/Tsuna-Streaming/blob/main/docs/apps/channel_admins.md'>documentation</a>.

<hr>

## Managing Content on Tsuna Streaming

Tsuna Streaming's <a href='https://github.com/mohamad-liyaghi/Tsuna-Streaming/blob/main/docs/apps/core.md'>Core</a> module has a base model called `BaseTokenModel` that serves as the foundation for all content models. It contains common fields and methods.

### Videos
The `Videos` application is responsible for managing user-uploaded videos. The main model used is `Video`, which inherits from `BaseContentModel` providing all necessary functionalities. Admins can add, update, and delete videos for a channel based on their permissions, while users can view published videos. For more details, check out the <a href='https://github.com/mohamad-liyaghi/Tsuna-Streaming/blob/main/docs/apps/videos.md'>documentation</a>.

### Music
Similar to the `Videos` application, the `Music` application uses a model that inherits from `BaseContentModel`. All functionalities are the same as those of the `Videos` application. You can refer to the official <a href='https://github.com/mohamad-liyaghi/Tsuna-Streaming/blob/main/docs/apps/musics.md'>documentation</a>  for more information.

<hr>


## Votes, Views and Comments

### Vote
The `Votes` application manages the essential functionality of Upvoting/Downvoting for all content models through a single, generic `Vote` model. This application implements a caching mechanism to store votes temporarily before inserting them into the database via a celery task.

The application provides several methods for retrieving votes from both cache and the database while also allowing for the insertion of new votes into cache. For more detailed information about this application, please refer to the <a href='https://github.com/mohamad-liyaghi/Tsuna-Streaming/blob/main/docs/apps/votes.md'>documentation</a>.

### Comments
The `Comments` application within the "Tsuna Streaming" project enables users to leave comments on objects that allows commenting. Also users can vote a comment or even reply on that. Its primary purpose is to provide a commenting feature for various content models, using a single, generic `Comment` model.

By utilizing this application, users can add comments to different content models with ease. For more information about the "Comments" application, including usage instructions and available methods, please see the <a href='https://github.com/mohamad-liyaghi/Tsuna-Streaming/blob/main/docs/apps/comments.md'>documentation</a>.

### Viewers
The `Viewers` application of the Tsuna Streaming project serves the purpose of tracking viewers of an object. It stores viewer information in cache before inserting it into the database. Admins can access the list of all viewers of an object.

The application includes a decorator that is used to decorate detail pages for adding viewing purposes.

To ensure consistent tracking, there is a dedicated task responsible for inserting viewer data into the database. If you require additional information about the "Viewers" application, please consult the <a href='https://github.com/mohamad-liyaghi/Tsuna-Streaming/blob/main/docs/apps/viewers.md'>documentation</a>.


<hr>

# How to run?
To use Tsuna Streaming, you'll first need to clone the project from GitHub. Open your terminal and run the following command:

```
git clone https://github.com/mohamad-liyaghi/Tsuna-Streaming.git
```

Once the cloning process is complete, navigate into the project directory using the `cd` command:

```
cd Tsuna-Streaming
```

Next, you'll need to configure the environment variables in the `.env` files. You can customize settings such as the database username and email address to suit your needs.

For local development, run the following command to start the Docker containers:

```
docker-compose -f docker/local/docker-compose.yml up --build
```

If you're running Tsuna Streaming in production, use the following command instead:

```
docker-compose -f docker/production/docker-compose.yml up --build
```

Once the Docker containers are up and running, you can access Tsuna Streaming by navigating to `localhost:8000` in your web browser. 

# Tests
You can run tests by running this command:

```
pytest
```

That's it! You're now ready to use Tsuna Streaming.