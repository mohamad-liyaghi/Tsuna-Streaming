# Membership Application Documentation

## Description
The Membership application of the Tsuna Streaming project manages membership plans and subscriptions for users. It allows administrators to create, update, and delete membership plans, while normal users can subscribe to these plans. Premium users have more privileges than normal users, such as higher limits for channel creation and video size.

## Models

### Membership
The `Membership` model represents a membership plan available for users. The fields are as follows:

- `title`: Title of the membership plan.
- `description`: Description of the membership plan.
- `price`: Price of the membership plan.
- `active_months`: Number of months the membership plan remains active.
- `is_available`: A boolean field indicating if the membership plan is currently available for users.
- `__check_in_use()`: A private method to check if the membership plan is in use. It raises `MembershipInUserError` if the plan is in use by any user and cannot be deleted.

### Subscription
The `Subscription` model represents a user's subscription to a membership plan. The fields are as follows:

- `user`: A relationship to the user who subscribed.
- `membership`: A relationship to the subscribed membership plan.
- `start_date`: Start date of the subscription.
- `end_date`: End date of the subscription.
- `is_active()`: A method to check if the subscription is currently active.

## Views

### MembershipListCreateView
- Description: List all Membership Plans and allow admins to create new ones.
- HTTP Methods:
  - GET: List all available Membership Plans.
  - POST: Create a new Membership Plan [Admin only].
- Responses:
  - 200 OK: List of all Membership Plans.
  - 201 Created: Successfully created a new Membership Plan.
  - 401 Unauthorized: Authentication required.
  - 403 Forbidden: User does not have admin privileges.

### MembershipDetailView
- Description: View details of a specific Membership Plan and allow admins to update or delete it.
- HTTP Methods:
  - GET: Retrieve the details of a Membership Plan.
  - PUT: Update a Membership Plan [Admin only].
  - PATCH: Update a Membership Plan [Admin only].
  - DELETE: Delete a Membership Plan [Admin only].
- Responses:
  - 200 OK: Detail page of a Membership Plan.
  - 204 No Content: Successfully deleted a Membership Plan.
  - 401 Unauthorized: Authentication required.
  - 403 Forbidden: User does not have admin privileges.
  - 404 Not Found: Membership Plan not found.

### MembershipSubscribeView
- Description: Allow normal users to subscribe to a membership plan.
- HTTP Methods:
  - POST: Subscribe to a membership plan [Normal users only].
- Responses:
  - 201 Created: Successfully created a new subscription.
  - 401 Unauthorized: Authentication required.
  - 403 Forbidden: User is not a normal user.
  - 404 Not Found: Membership Plan not found.

## Celery Beat Tasks

### auto_delete_invalid_subscription
- Description: Automatically delete expired subscriptions.

## Signals

### notify_user_subscription
- Description: Notify a user by email when a new subscription is created for them.

### notify_user_plan_expiration
- Description: Notify a user by email when their subscription has expired.

## Tests

The tests for the Membership application can be found in the `memberships/tests` directory. The tests cover various scenarios and functionalities of the Membership models, views, signals, and Celery Beat tasks. To run the tests, you can use the following command:

```
pytest memberships/tests
```