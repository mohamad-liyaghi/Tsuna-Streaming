# Accounts Application Docs

<h3>The "Accounts" application of the "Tsuna Streaming" project handles 3 things in the project.<br><br>
<ol>    
    <li>Authentication</li>
    <li>Token verification</li>
    <li>Subscription</li>
    
</ol><hr>

In this project, we have 3 types of users.<br><br>
<ol>    
    <li>Superuser (Admins)</li>
    <li>Premium users.</li>
    <li>Normal Users.</li>
    
</ol><hr>

First, users should register on website, then verify their accounts via the link that has been sent by email. 
<br>
After verifying they can Login via JWT token.<br>
<br>

By default, users role is "Normal" but they can purchase subscription plans and become "Premium". <br><br>
</h3>

<hr>

<h2>Authentication</h2>
<p>
There is a custom Account model that inherits from AbstractUser model of Django.
This model is the main account model of this project.
<br>
When users register to website, they have 24 hours to verify their accounts, otherwise their account would be deleted by celery task.
</p>

<ol>
    <li>Register</li>
    <li>Verify by Token.</li>
    <li>Login via jwt</li>
    <li>User Profile Page and update Profile.</li>
    <li>Create unique user token [Signals].</li>
    <li>Delete extra deactivated users from the database. [Celery]</li>
    <li>Profile size validator.</li>
    <li>Throttling.</li>
</ol>
<hr>

<h2>Token Verification</h2>
<p>
When a user registers to website, a unique token will be created and sent by email. User can verify and activate their account by this token. Token gets expired and deleted after a while, so user can alway request for a new one.
<br> Users can only enter 5 invalid tokens at a time. After that they should wait until their token expires. This avoids spam requests.
</p>

<ol>
    <li>Auto create token after registering. [Signals]</li>
    <li>Send the token by email.</li>
    <li>Auto delete invalid tokens [celery]</li>
    <li>Token retry.</li>
</ol>
<hr>


<h2>Subscription</h2>
<p>
There are 2 models in this part. "Subscription" and "Plan".
<br> Admins can add a plan that has a price, normal users can buy this plans and become Premium users and enjoy the privileges.
</p>

<h4>Plan</h4>
<ol>
    <li>Create a plan [Only Admins]</li>
    <li>List of plans</li>
    <li>Update a plan [Only Admins]</li>
    <li>Delete a plan [Only Admins]</li>
    <li>Purchase a plan</li>
    <li>Change plan availability.</li>
    <li>Raise exception when trying to delete an in use plan</li>
    
</ol>

<h4>Subscription</h4>
<ol>
    <li>Auto promote the user after buying a plan (Overrided in Subscription save method)</li>
    <li>Auto demote users after plan deletion [Overrided in Subscription delete method]</li>
    <li>Delete expired subscriptions</li>
    <li>Notify user subscription by Email</li>
</ol>

<hr>
<h3>Also there are some tests that you can run them by typing this command:</h3>

```
$ pytest v1/accounts
```
