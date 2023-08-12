# Tsuna Streaming Backend

## Table of Contents
1. [Introduction](#introduction)
2. [Technologies](#technologies)
3. [Applications](#applications)
    - [Core](#core)
    - [Accounts](#accounts)
    - [Memberships](#memberships)
    - [Channels](#channels)
    - [ChannelSubscribers](#channelsubscribers)
    - [ChannelAdmins](#channeladmins)
    - [Contents](#contents)
    - [Videos](#videos)
    - [Musics](#musics)
    - [Votes](#votes)
    - [Comments](#comments)
    - [Viewers](#viewers)

## Introduction <a name="introduction"></a>
The Tsuna Streaming backend is a powerful system that allows users to create channels, share videos and music, and engage with other users through voting and commenting. Channel owners can add administrators, and users can follow channels to stay updated. The backend efficiently tracks viewership and votes, utilizing caching for transaction efficiency. With user management, content sharing, and engagement features, the Tsuna Streaming backend provides a seamless and interactive experience for users.

Tsuna Streaming supports 3 user roles: `admin`, `premium`, and `normal`.
Each of this roles has different permissions and access to the platform. <br>
Eg: `premium` users can create more channels than `normal` users.<br>

## Technologies <a name="technologies"></a>
The Tsuna Streaming platform utilizes the following technologies:
1. Django
2. Django REST Framework
3. Docker
4. PostgreSQL
5. Redis
6. Celery
7. Swagger
8JWT

## Applications <a name="applications"></a>
The project is structured into ten main applications and two modules.

### Core <a name="core"></a>
The `core` module is a fundamental part of the project and houses common functions and classes that are utilized throughout the platform. It includes models such as `AbstractToken` for generating unique tokens.The module also provides celery tasks for sending emails and pytest fixtures for testing API endpoints. For more detailed information, please refer to the [Full Document](docs/apps/core.md).

### Accounts <a name="accounts"></a>
The `Accounts` application is responsible for managing user accounts and their verification process. It includes models such as `Account` for storing user information and `VerificationToken` for generating and managing verification codes. The application provides views for user registration, email verification, resending verification codes, and generating JWT tokens for authentication. It also includes signals for generating verification codes and sending verification emails. Additionally, there are Celery Beat tasks for deleting expired verification codes and deactivated users. The application offers custom manager methods for verifying codes and utility functions for generating unique verification codes. It also defines exceptions for handling various scenarios related to user accounts and verification. For more detailed information, please refer to the [Full Document](docs/apps/accounts.md).

### Memberships <a name="memberships"></a>
The `Memberships` application is responsible for managing user subscriptions and memberships. It consists of two models: `Membership` and `Subscription`. Administrators can create available plans, which users can then subscribe to. A Celery task handles the promotion/demotion of users based on the start and end dates of their subscriptions. This task ensures that users are granted the appropriate privileges and benefits when their subscription starts and that they are demoted or have privileges revoked when their subscription ends. For more detailed information, please refer to the [Full Document](docs/apps/memberships.md).   

### Channels <a name="channels"></a>
The `Channels` application is responsible for managing user-created channels. Once a user is verified, they can create channels to share their content. Normal users can create up to 5 channels, while premium users can create up to 10 channels. For more detailed information, please refer to the [Full Document](docs/apps/channels.md). 

### Channel Subscribers <a name="channelsubscribers"></a>
The `Channel Subscribers` application is responsible for handling channel subscriptions and unsubscriptions. Once a channel is created, users can explore its content and choose to subscribe if interested. To optimize efficiency, subscription records are initially stored in a cache, and a recurring Celery Beat task periodically transfers them to the main database. Similarly, when users decide to unsubscribe, the corresponding record is removed from the cache, and a Celery Beat task deletes it from the database. This approach minimizes direct database load while ensuring the integrity of subscription records. For more detailed information, please refer to the [Full Document](docs/apps/channel_subscribers.md).

### Channel Admins <a name="channeladmins"></a>
The `Channel Admins` application allows channel owners to promote subscribed users as admins, granting them specific permissions to perform actions within the channel. Once a user has subscribed to a channel, the channel owner has the authority to designate certain users as admins. Admins are then empowered to carry out actions based on the permissions granted to them. For instance, users with the "add" permission can upload and add videos to the channel. By assigning admins with appropriate permissions, channel owners can delegate responsibilities and enhance collaboration within the channel, fostering a more dynamic and interactive environment for content creation and management. For more detailed information, please refer to the [Full Document](docs/apps/channel_admins.md).

### Contents <a name="contents"></a>
The `Contents` module is responsible for facilitating code reusability and sharing common models and views among other content-related modules. At its core is the `AbstractContent` model, which acts as a base model for both videos and music. By utilizing this abstract model, common fields and functionalities such as title, description, creation date, and author information are shared, reducing redundancy and promoting consistency in content management. This modular approach streamlines development, enhances code organization, and ensures efficient management of various content types throughout the system. For more detailed information, please refer to the [Full Document](docs/apps/contents.md).

### Videos <a name="videos"></a>
The `Videos` application is dedicated to handling the creation, retrieval, updating, and deletion (CRUD) operations for videos within a channel. It provides a comprehensive set of functionalities for managing video content specific to a channel. Channel owners and admins with the necessary permissions are empowered to perform various actions, including creating new videos, editing existing videos, deleting videos, and carrying out other relevant tasks related to video content management. By offering these capabilities, the `Videos` application ensures that channel owners and authorized admins have full control over the video content within their channels, enabling them to curate and maintain a dynamic video library. For more detailed information, please refer to the [Full Document](docs/apps/videos.md).

### Musics <a name="musics"></a>
The `Musics` application is responsible for facilitating the CRUD operations for music content within a channel. It provides a dedicated set of functionalities for managing music-related content associated with a channel. Channel owners and authorized admins with the required permissions can leverage these features to perform actions such as creating new music tracks, updating existing music files, deleting music content, and executing other tasks relevant to music management within the channel. By offering these capabilities, the `Musics` application empowers channel owners and admins to curate and maintain a diverse collection of music content, ensuring an engaging and immersive experience for channel subscribers interested in music. For more detailed information, please refer to the [Full Document](docs/apps/musics.md).

### Votes <a name="votes"></a>
The `Votes` feature enables users to express their opinions on published content by upvoting or downvoting it. Once content is published, users have the ability to indicate their preference through voting. To optimize efficiency, the voting system initially stores the votes in a cache, minimizing direct interactions with the main database. This approach helps to improve performance and reduce database load. Periodically, a process or task retrieves the votes from the cache and persists them in the main database. By utilizing this caching mechanism, the voting functionality ensures a smooth and responsive user experience while maintaining the integrity and accuracy of the vote records. For more detailed information, please refer to the [Full Document](docs/apps/votes.md).

### Comments <a name="comments"></a>
The `Comments` application is responsible for managing user-generated comments on published content. It provides functionalities that allow users to engage in discussions, provide feedback, and share their thoughts on specific pieces of content. Users can post comments, view existing comments, reply to comments, and perform actions such as editing or deleting their own comments. The application fosters an interactive environment where users can actively participate in conversations and contribute to the overall engagement and community interaction around the content. By facilitating user-generated discussions and feedback, the `Comments` application enhances the user experience and promotes a sense of community within the platform. For more detailed information, please refer to the [Full Document](docs/apps/comments.md).

### Viewers <a name="viewers"></a>
The `Viewers` application is responsible for tracking and recording user views on content. When a user retrieves or accesses a piece of content, a viewer record is initially saved in a cache to optimize performance. This caching mechanism minimizes direct interactions with the main database. After that, a Celery task is scheduled to insert the viewer record into the main database. By employing this approach, the `Viewers` application efficiently manages and records user views, providing valuable insights into content popularity and engagement. This helps content creators and administrators gain a better understanding of user behavior and preferences, enabling them to make informed decisions and optimize the platform's content strategy.For more detailed information, please refer to the [Full Document](docs/apps/viewers.md).

