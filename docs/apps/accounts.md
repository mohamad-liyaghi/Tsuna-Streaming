# Accounts Application Docs

<h3>The "Accounts" application of the "Tsuna Streaming" project handles 2things in the project.<br><br>
<ol>    
    <li>Authentication</li>
    <li>Token verification</li>
</ol><hr>


First, users should register on website, then verify their accounts via the link that has been sent by email. 
<br>
After verifying they can Login via JWT token.<br>
<br>

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



<hr>
<h3>Also there are some tests that you can run them by typing this command:</h3>

```
$ pytest v1/accounts
```
