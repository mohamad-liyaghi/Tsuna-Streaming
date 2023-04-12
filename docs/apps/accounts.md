# Accounts Application Documentation
## Overview

The accounts application is an essential part of the project, which handles user registration, account activation, authentication, and user roles. The application ensures that the user's are authenticated, and only verified users can perform actions.

## User Registration

Creating an account is a smooth and straightforward process for users. Once the user submits the registration form, their account will be temporarily deactivated until they verify it using the token sent to their email address.

## Account Verification

A token is generated and sent to the user's email address after successful registration. The user must verify their account using the token to activate their account.

## Authentication

After account verification, the user can log in using the JWT (JSON Web Token) authentication method, which ensures the user's privacy and security.

<hr>

## Models

This application is comprised of two models:

1. Account - This is the primary model for user accounts within the project. It inherits from the AbstractUser model in Django and includes custom fields for role management and informations.

2. Token - This model is responsible for generating and storing verification tokens for new user accounts. When a user registers, a unique token is generated and sent to their email address. The user must then use this token to verify their account and activate it.

Together, these two models provide a robust framework for user registration and account management within the project.

## User Roles

By default, new users are assigned the 'n' (normal) role, while superusers are assigned the 'a' (admin) role. Superusers have more privileges and access to the system.

## Throttling

To avoid spamming, there is throttling in place. Users are restricted from sending multiple requests within a specified time.


## Token Expiration

To keep the system secure, the application uses celery-beat to remove all expired tokens and deactivated users automatically.


## Signals

In the user registration process, the application will generate a unique token for each newly registered user, which will be stored in the database. This is achieved by using a signal that listens for the post_save event on the Account model.

Once the token has been generated and saved, another signal will be triggered, this time to send the token to the user via email. This email will include instructions for the user to verify their account by clicking on a link, which will confirm their identity as the owner of the email address used during registration.

By utilizing these signals, the application ensures that the user registration process is secure and streamlined, with minimal input required from the user to activate their account.

## Tests

There are some tests that you can run by typing this command: 

```
$ pytest v1/accounts
```