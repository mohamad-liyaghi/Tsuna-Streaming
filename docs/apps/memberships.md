## Introduction
The "Memberships" application is responsible for managing user subscriptions and memberships in the Tsuna Streaming project.
<br>
There are three types of users in this project: Admin, Premium, and Normal.<br>
 Superusers are assigned to the "admin" role by default, while normal users are assigned to the "normal" role. Users can upgrade their membership by subscribing to a premium plan, which grants them additional privileges and features and become "premium".

## Models
The Memberships application has two models:

1. Membership - represents the different types of membership plans that users can subscribe to.
2. Subscription - contains information about a user's subscription to a membership plan.

## Views
The following views are available in the Memberships application:

1. Create Membership - allows admins to create new membership plans.
2. List of Memberships - displays a list of all available membership plans.
3. Update Membership and Delete - allows admins to update and delete existing membership plans.
4. Subscribe to Membership - allows users to subscribe to a membership plan.

## Features

### Deleting In-Use Memberships
An Exceptaion will be raised if an admin tries to delete a membership that is currently in use by users. 

### Email Notifications
Users will receive email notifications upon successful subscription to a membership plan. They will also be notified when their subscription has expired.

### Removing Invalid Memberships with Celery
A Celery task runs periodically to remove invalid memberships. An invalid membership is one that has expired and is no longer active.

## Tests
The Memberships application includes automated tests that you can run them by typing this command:

```
$ pytest memberships/
``` 