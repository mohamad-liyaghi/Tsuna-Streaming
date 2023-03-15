# Memberships Application Documentation

<h3>
The "Memberships" application is an integral part of the "Tsuna Streaming" project, responsible for managing user subscriptions and membership roles. By default we have three types of users in this project: Admin, Premium, and Normal.
<br><br>
By default, Superusers are assigned to the Admin role, while normal users are assigned to the Normal role. However, normal users have the ability to upgrade their membership by subscribing to a premium plan, which grants them additional privileges and features.
<br><br>
</h3>

<hr> <br>

<h3>
This application has 2 models. 
<ol>    
    <li>Membership</li>
    <li>Subscription</li>
    
</ol><hr>
</h3>


<h2>Membership</h2>
<p>
The Membership model represents the different types of membership plans that users can subscribe to. Admins have the ability to create, update, and delete different membership plans, and users can subscribe to them based on their needs.
</p>

<ol>
    <li>Allow admins to create, update, and delete membership plans.</li>
    <li>Provide a list of available memberships for users to choose from.</li>
    <li>Prevent deletion of memberships that are currently in use.</li>
    <li>IsAdmin permission for adding, updating, and deleting memberships.</li>
</ol>
<hr>


<h2>Subscription</h2>
<p>
When a user subscribes to a membership plan, a new subscription is created containing relevant information such as the expiration date. The user's role is upgraded to premium upon successful subscription. When the subscription token expires, Celery will automatically delete the subscription and notify the user. Additionally, the user's role will be changed back to normal.
</p>

<ol>
    <li>Allow users to subscribe to a membership plan.</li>
    <li>Notify users upon successful subscription.</li>
    <li>Notify users when their subscription has expired.</li>
    <li>Automatically delete invalid subscriptions using Celery.</li>
    <li>A permission system to check whether a user is currently subscribed to a premium plan or not.</li>
</ol>
<hr>

<h3>Also there are some tests that you can run them by typing this command:</h3>

```
$ pytest v1/memberships
```