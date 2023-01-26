# Channels Application Docs

<h3>
The "Channels" Application of "Tsuna Streaming" project handles channel creation, channel admins, and subscriber purposes.
<br><br>
This app is using <a href="redis.io">Redis</a> for caching stuff<br><br>
Admins, Premium, Normal.<br><br>

Users can create channels, also promote admins for performing actions based on their rights alongside the channel owner, also other users can subscribe to the channel to get new feeds.
</h3>
<hr>
<h3>This application consists of 3 parts.
 <b>Account</b>, <b>Token</b>, and <b>Subscription</b>.</h3>

<hr>
<h2>This app has three main purposes.</h2>


<h2>Channel</h2>
<p>
    Users can create for uploading videos.
    There is a limit for creating channels, Normal users can create 5 and premium users can create 10 channels.
</p>

<ol>
    <li>Create a Channel</li>
    <li>Update a Channel</li>
    <li>Delete a Channel</li>
    <li>User Channel List.</li>
    <li>Channel information Caching</li>
    <li>Send an email after creating a channel</li>
    <li>Channel creation limit</li>
</ol>
<hr>

<h2> Channel Admin</h2>
<p>
    Channels can have admins alongside the owners.
    Owners can promote admin and admin can perform an action based on given rights.
</p>

<ol>
    <li>Add Admin</li>
    <li>Update Admin rights</li>
    <li>Demote an admin</li>
    <li>Channel Admin List</li>
    <li>Send an email after promoting</li>
</ol>
<hr>


<h2>Subscribers</h2>
<p>
    Users can subscribe to a channel to get new feeds. <br>
    Also admins can block a user from accessing channels content.
</p>

<ol>
    <li>Check whether or not the user subscribed to a channel</li>
    <li>Subscribe/Unsubscribe a channel</li>
    <li>Channel Subscriber list</li>
    <li>Subscribed cahnnel list</li>
    <li>Block/Unblock a subscriber</li>
</ol>
<hr>
<h3>Also there are some tests that you can run them by typing this command:</h3>

```
$ pytest
```
