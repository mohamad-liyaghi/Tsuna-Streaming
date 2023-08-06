# Channel Admins Application Documentation

Table of Contents:
- [Description](#description)
- [Models](#models)
  - [ChannelAdmin](#channeladmin)
  - [ChannelAdminPermission](#channeladminpermission)
- [Views](#views)
  - [AdminListCreateView](#adminlistcreateview)
  - [AdminDetailView](#admindetailview)
- [Signals](#signals)
  - [send_admin_promotion_email](#send-admin-promotion-email)
  - [create_admin_after_creating_channel](#create-admin-after-creating-channel)
  - [delete_admin_after_unsubscribing](#delete-admin-after-unsubscribing)
  - [create_permissions_for_admin](#create-permissions-for-admin)
- [Exceptions](#exceptions)
  - [SubscriptionRequiredException](#subscriptionrequiredexception)
- [Tests](#tests)

## Description
The Channel Admins application allows channel owners to promote users as admins for their channels. Admins have specific permissions within the channel. This application provides views for listing and creating admins, retrieving and updating admin permissions, and deleting admins.

## Models

### ChannelAdmin
The `ChannelAdmin` model represents an admin for a channel. The fields are as follows:

- `user`: A relationship to the `User` model.
- `promoted_by`: A relationship to the `User` model who promoted the admin.
- `channel`: A relationship to the `Channel` model.
- `date`: The date when the admin was promoted.

### ChannelAdminPermission
The `ChannelAdminPermission` model represents the permissions assigned to an admin. The fields represent the specific permissions available to admins.

## Views

### AdminListCreateView
The `AdminListCreateView` is responsible for listing all the admins for a channel and creating a new admin. It accepts GET and POST requests.

- **Responses**:
  - `200 OK`: Successfully retrieved the list of admins.
  - `201 Created`: Successfully created a new admin.
  - `400 Bad Request`: Invalid data in the request.
  - `401 Unauthorized`: User is not authenticated.
  - `403 Forbidden`: User does not have permission to perform the action.

### AdminDetailView
The `AdminDetailView` is responsible for retrieving, updating, and deleting an admin. It accepts GET, PUT, PATCH, and DELETE requests.

- **Responses**:
  - `200 OK`: Successfully retrieved or updated the admin.
  - `204 No Content`: Successfully deleted the admin.
  - `400 Bad Request`: Invalid data in the request.
  - `401 Unauthorized`: User is not authenticated.
  - `403 Forbidden`: User does not have permission to perform the action.
  - `404 Not Found`: Admin not found.

## Signals

### send_admin_promotion_email
This signal is triggered when a user is promoted as an admin. It sends an email notification to the user about their promotion.

### create_admin_after_creating_channel
This signal is triggered when a new channel is created. It automatically creates an admin for the channel, with the channel owner being the admin.

### delete_admin_after_unsubscribing
This signal is triggered when a user unsubscribes from a channel. It automatically deletes the admin associated with the user.

### create_permissions_for_admin
This signal is triggered when a new admin is created. It automatically creates permissions for the admin.

## Exceptions

### SubscriptionRequiredException
This exception is raised when a user tries to perform an action that requires a subscription to the channel.

## Tests
Tests for the Channel Admins application can be run with the following command:

```
pytest apps/channel_admins
```