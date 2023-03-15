# Channel Admins Application Docs

<h3>
The "Admin" application of the "Tsuna Streaming" project handles the management of channels and content for administrators.
<br><br>
By default, the channel owner has full permission and can perform any kind of action within the channel. However, as owners are not always available, they can promote other users to be admins with customized access permissions.
<br><br>
When a channel gets created, an admin object will be created with full accesses. <br><br>

After creating an admin object, signals will automatically create new permissions for that admin based on the BaseContentModel subclasses. <br>
For example, when a user is promoted to an admin, a corresponding permission for the Video model will be created.
<br>

This Application has 2 models.
<ol>
    <li>Admin</li>
    <li>Permission</li>
</ol>
</h3>

<h2>Admin</h2>
<p>
The main Admin model of each channel. <br>
When a user creates a channel, an admin object with full permissions will automatically be created for the channel owner. The channel owner or admins with the 'add_admin' permission can promote other users to become admins.
</p>

<ol>
    <li>Add/Update/Delete Admin</li>
    <li>Avoid Promotion duplication</li>
    <li>Permission for retrieving list of Admins</li>
    <li>Admin permission mixin</li>
    <li>Notify after promoting [Signal]</li>
    <li>Delete admin after ubsubscribing [Signal]</li>
    <li>Create full permission admin after creating channel [Signal]</li>
    <li>SubscriptionRequiredException will be raised when attempting to promote a user who has not subscribed to the channel</li>
</ol>


<h2>Permission</h2>
<p>
All admins have general permissions that relate to channels, rather than specific Contents. After being promoted to an admin, signals create new permissions for that user to control each content model. <br>
For instance, a permission fro 'Video' model is created which checks whether users are allowed to perform certain actions on a videos.
</p>

<ol>
    <li>Update Admin permissions</li>
    <li>Create permission for admin [Signal]</li>
    <li>Create permission for admin task [celery]</li>
</ol>

<h3>Also there are some tests that you can run them by typing this command:</h3>

```
$ pytest v1/admins
```
