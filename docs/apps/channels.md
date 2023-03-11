# Channels Application Docs

<h3>
The "Channels" application in the "Tsuna Streaming" project is responsible for handling the creation and management of user channels, as well as facilitating channel subscriptions by other users.

<hr>

<h3>The "Channels" application consists of two main components:</h3>

<ul>
<li><b>Channel Creation:</b> This component allows users to create and manage their own channels. Users can provide basic information such as channel name, description, and profile picture, as well as add social media links to promote their content.</li>

<li><b>Channel Subscription:</b> This component allows viewers to subscribe to channels they are interested in following. Viewers can receive notifications when new videos are uploaded to subscribed channels, making it easier to stay up-to-date on the latest content.</li>
</ul>

<hr>


<h2>Channel</h2>
<p>
    The "Channels" application includes a Channel model that is used to represent user channels in the project. By default, normal users are limited to creating up to five channels. However, if they promote their accounts, they can create up to ten channels.
    <br>
    Channels can also have admins. These users have administrative privileges for a particular channel and can perform actions based on their assigned permissions. For example, admins may be able to edit or delete videos. This allows channel owners to delegate tasks and collaborate with other users in managing their channels.

</p>

<ol>
    <li>Create/Update/Delete Channel</li>
    <li>User Channel List.</li>
    <li>Channel information [Caching]</li>
    <li>Send an email after creating a channel [Signal]</li>
    <li>Channel creation exceptions</li>
</ol>
<hr>


<h2>Subscriber</h2>
<p>
    The "Channels" application also includes a Subscriber model that is used to represent user subscriptions to channels in the project.
</p>

<ol>
    <li>Subscription status</li>
    <li>Subscribe/Unsubscribe a channel</li>
    <li>Channel Subscriber list</li>
    <li>Subscribed channels list</li>
    <li>Block/Unblock a subscriber</li>
    <li>Auto create subscriber after creating a channel [Signal]</li>
    <li>Avoid from subscribe duplication [Exception]</li>
</ol>
<hr>

<h3>Also there are some tests that you can run them by typing this command:</h3>

```
$ pytest v1/channels
```
