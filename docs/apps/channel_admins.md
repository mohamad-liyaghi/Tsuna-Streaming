# Introduction:
The "Channel Admins" application is a part of the "Tsuna Streaming" project that handles the management of channels and content for administrators. By default, the channel owner has full permission and can perform any kind of action within the channel. However, as owners are not always available, they can promote other users to be admins with customized access permissions.

# Models:
The app uses two models - `ChannelAdmin` and `ChannelAdminPermission`. 

- `ChannelAdmin` model is the main admin model for each channel. When a user creates a channel, an admin object with full permissions will automatically be created for the channel owner. The channel owner or admins with the 'add_admin' permission can promote other users to become admins.

- `ChannelAdminPermission` model stores information about the permission assigned to the admin. It contains a foreign key to the `ChannelAdmin` model as well as fields to store the permission type and the time when the permission was granted.

# Views:
- `add_admin` Admins can promote other users with this view

- `list_admins` List of admins of a channel.

- `update_admin` Update an admins common permissions.

- `update_admin_permission` Update an admins specific permissions.

- `delete_admin` Delete an admin.

# Signals:
The app uses signals to perform certain actions. 

- When a new channel admin is added, the app sends a notification to the admin user. 

- When a user unsubscribes from a channel, the app removes their corresponding entries from the `ChannelAdmin` and `ChannelAdminPermission` models.

- When an admin object or channel gets created, signal creates permission for each ContentModel.

# Exceptions:
The app has one exception: `SubscriptionRequiredException`.

`SubscriptionRequiredException` exception is raised if the user trying to add an admin is not a subscribed member of the channel.

`DuplicatePromotionException` exception is raised if the user is getting promoted twice.

## Tests
The application's tests can be run using the following command: 

```
$ pytest apps/channel_admins
```