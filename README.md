# Tsuna Streaming

## Introduction <a name="introduction"></a>
Tsuna Streaming is a powerful backend system that enables users to create channels and share various types of content, including videos and music. This platform allows users to follow their favorite channels, vote on content, and engage in discussions through comments. The system also keeps track of the number of viewers for each channel.

Channel owners have the ability to add administrators to their channels, granting them specific permissions to perform various tasks. This feature allows channel owners to delegate responsibilities and manage their channels more effectively.

Users can have two types of accounts: normal and premium. Premium users enjoy additional benefits, such as the ability to create twice as many channels as normal users and upload larger files. This distinction encourages users to upgrade to premium accounts, enhancing their experience on the platform.

To ensure optimal performance and transaction efficiency, the system employs a caching mechanism. Viewers and votes are initially stored in the cache and then periodically synchronized with the database.

With Tsuna Streaming, users can create, discover, and engage with a wide range of content, fostering a vibrant and interactive community.

## Backend <a name="backend"></a>
The backend of Tsuna Streaming is built using Django and Django REST Framework, incorporating modern technologies such as Docker, PostgreSQL, Redis, and Celery. This solid technology stack ensures efficient data management and a smooth user experience.
For detailed information about the Tsuna Streaming backend, please refer to the [Backend Docs](backend/README.md).

## Frontend <a name="frontend"></a>
The front-end of Tsuna Streaming is currently undergoing maintenance. We welcome contributions from front-end developers to help enhance and further develop the user experience.

## How to Run <a name="how-to-run"></a>
Follow these simple steps to run the Tsuna Streaming backend:

1. Clone the project repository:
    ```bash
    git clone https://github.com/mohamad-liyaghi/Tsuna-Streaming.git
    ```

2. Change to the project directory:
    ```bash
    cd tsuna-streaming/
    ```

3. To run the project in development mode using Docker-compose, execute the following command:
    ```bash
    docker-compose up --build
    ```

   If you want to run the project in production mode, use the following command instead:
    ```bash
    docker-compose -f docker-compose.prod.yml up --build
    ```

   This will build and start the containers required for the project to run in a production environment.

4. Access the Tsuna Streaming API in a web browser at `http://localhost:8000/`.

You're all set! Enjoy using Tsuna Streaming.
