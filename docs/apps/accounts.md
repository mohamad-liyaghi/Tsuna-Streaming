# Accounts Application Docs

<h3>The "Accounts" application of the "Tsuna Streaming" project handles the Authentication and Membership purposes of the project.<br><br>
In this project, we have 3 types of users.<br><br>
Admins, Premium, Normal.<br><br>
Users must register, verify and then they can purchase website plans. <br><br>
This project is using <a href="https://docs.celeryq.dev/en/stable/">Celery</a> for dealing with heavy processes and also <a href="https://pypi.org/project/django-templated-mail/">django-templated-mail</a> for sending email. <a href="https://docs.pytest.org/en/7.2.x/">Pytest</a> for testing implementation.
</h3>
<hr>
<h3>This application consists of 3 parts.
 <b>Account</b>, <b>Token</b>, and <b>Subscription</b>.</h3>

<hr>

<h2>Authentication</h2>
<p>
This part contains the custom user model of the project and functionalities below:
</p>

<ol>
    <li>Register User</li>
    <li>Login User [jwt]</li>
    <li>Verify User</li>
    <li>Profile Page and update Profile.</li>
    <li>Delete extra deactivated users from the database. [Celery]</li>
    <li>Profile size limit. [validator]</li>
</ol>
<hr>

<h2>Token</h2>
<p>
Contains the Token model and some Signals related to creating tokens.
</p>

<ol>
    <li>Auto create signal after registering user. [signals]</li>
    <li>Email the token</li>
    <li>Auto delete invalid tokens [celery]</li>
</ol>
<hr>


<h2>Subscription</h2>
<p>
Provides membership service. <br>
There are 2 models in this section.
</p>

<h4>Plan</h4>
<ol>
    <li>Create a plan [Admin]</li>
    <li>List of plans</li>
    <li>Update a plan [Admin]</li>
    <li>Delete a plan [Admin]</li>
</ol>
<h4>Subscription</h4>
<ol>
    <li>Buy subscription</li>
    <li>Auto promote the user after buying a membership (via signals)</li>
    <li>Auto demote users after finishing their membership time [Celery]</li>
    <li>Notify by email</li>
</ol>

<hr>
<h3>Also there are some tests that you can run them by typing this command:</h3>

```
$ pytest
```
