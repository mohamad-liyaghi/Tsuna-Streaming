# Accounts Application Documentation

Table of Contents:
- [Description](#description)
- [Models](#models)
  - [Account](#account)
  - [VerificationToken](#verificationtoken)
  - [AbstractAccountRole](#abstractaccountrole)
- [Views](#views)
  - [RegisterUserView](#registeruserview)
  - [VerifyUserView](#verifyuserview)
  - [ResendTokenView](#resendtokenview)
  - [LoginUserView](#loginuserview)
  - [ProfileView](#profileview)
- [Signals](#signals)
  - [create_verification_token](#create-verification-token)
  - [send_token_via_email](#send-token-via-email)
- [Celery Tasks](#celery-tasks)
  - [auto_delete_expired_tokens](#auto-delete-expired-tokens)
  - [auto_delete_deactive_users](#auto-delete-deactive-users)
- [Model Managers](#model-managers)
  - [VerificationTokenManager](#verificationtokenmanager)
- [Model Validators](#model-validators)
  - [validate_profile_size](#validate-profile-size)
- [Tests](#tests)

## Description
The Accounts application of the Tsuna Streaming project handles the creation, verification, and authentication of user accounts. It provides views for registration and login, and uses JWT tokens for authentication. Account verification is done via email, with the option to resend the verification token if it has expired.

## Models

### Account
The `Account` model represents a user account. The fields are as follows:

- `email`: A unique email address for the user.
- `picture`: Profile picture of the user.
- `first_name`: First name of the user.
- `last_name`: Last name of the user.
- `bio`: A short biography of the user.
- `is_active`: A boolean field indicating the active status of the user. Default value is `False`.

### VerificationToken
The `VerificationToken` model represents a verification token associated with a user account. The fields are as follows:

- `user`: A relationship to the `Account` model.
- `expire_at`: A datetime field representing the expiration date of the verification token.

### AbstractAccountRole
The `AbstractAccountRole` model represents a base class for account roles. It provides 3 methods for checking if the account has a specific role.
The methods are as follows:
- `is_admin()`: Checks if the account is a superuser.
- `is_premium()`: Checks if the account is a premium user.
- `is_normal()`: Checks if the account is a normal user.

## Views

### RegisterUserView
The `RegisterUserView` is responsible for registering a new account to the system. It accepts a POST request with the user's information.

- **Responses**:
  - `201 Created`: Successfully created the user account.
  - `400 Bad Request`: Invalid data in the request.
  - `403 Forbidden`: User is already authenticated.

### VerifyUserView
The `VerifyUserView` is responsible for verifying an account. It accepts a verification token.

- **Responses**:
  - `200 OK`: Successfully verified the user account.
  - `400 Bad Request`: Invalid data in the request.
  - `403 Forbidden`: Invalid verification token.
  - `404 Not Found`: User not found.

### ResendTokenView
The `ResendTokenView` is responsible for resending a verification token to the user if the previous one has expired.

- **Responses**:
  - `201 Created`: Successfully sent a new verification token to the user.
  - `400 Bad Request`: Invalid data in the request.
  - `403 Forbidden`: User is already authenticated.
  - `404 Not Found`: User not found.

### LoginUserView
The `LoginUserView` is responsible for logging in the user and returning a JWT token for future authentication.

- **Responses**:
  - `200 OK`: Return a JWT token for the user.
  - `400 Bad Request`: Invalid data in the request.
  - `403 Forbidden`: User is already authenticated.
  - `404 Not Found`: User not found.

### ProfileView
The `ProfileView` is responsible for retrieving and updating a user's public profile.

- **Responses**:
  - `200 OK`: Return the user's public profile.
  - `400 Bad Request`: Invalid data in the request.
  - `403 Forbidden`: User is not authenticated.
  - `404 Not Found`: User not found.

## Signals

### create_verification_token
This signal is triggered when a new user is created. It creates a verification token for the user.

### send_token_via_email
This signal is triggered when a new verification token is created. It sends the token to the user via email.

## Celery Tasks

### auto_delete_expired_tokens
This task is responsible for automatically deleting expired tokens after one day.

### auto_delete_deactive_users
This task is responsible for automatically deleting inactive users after one day.

## Model Managers

### VerificationTokenManager
The `VerificationTokenManager` includes a `verify` method for verifying a token.

## Model Validators

### validate_profile_size
This validator ensures the uploaded profile picture does not exceed 5MB in size.

## Tests
Tests for the Accounts application can be run with the following command:

```
pytest apps/accounts
```