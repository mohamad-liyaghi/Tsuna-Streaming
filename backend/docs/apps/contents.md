# Contents Module Documentation

Table of Contents:
- [Description](#description)
- [Module Structure](#module-structure)
- [Models](#models)
  - [AbstractContent](#abstractcontent)
  - [ContentVisibility](#contentvisibility)
- [Managers](#managers)
  - [BaseContentManager](#basecontentmanager)
- [Serializers](#serializers)
  - [ContentDetailMethodSerializer](#contentdetailmethodserializer)
- [Views](#views)
  - [ContentListCreateView](#contentlistcreateview)
  - [ContentDetailView](#contentdetailview)

## Description
The `contents` module provides functionality related to content management. It includes models for representing content, managers for querying content objects, and views for creating, listing, retrieving, updating, and deleting content.

## Module Structure
The `contents` module consists of the following components:
- Models: Contains the data models used for representing content and content visibility.
- Managers: Contains a manager class for querying content objects.
- Views: Contains view classes for handling content-related HTTP requests.

## Models

### AbstractContent
The `AbstractContent` model serves as a base model for representing content. It includes the following fields:
- `title`: The title of the content.
- `description`: A description of the content.
- `file`: The file associated with the content.
- `thumbnail`: The thumbnail image associated with the content.
- `visibility`: The visibility of the content, which can be either "Private" or "Published".
- `is_updated`: A flag indicating whether the content has been updated.
- `allow_comment`: A flag indicating whether comments are allowed on the content.
- `date`: The date of the content.

### ContentVisibility
The `ContentVisibility` enum represents the visibility options for content. It has two possible values:
- `Private`: Indicates that the content is private.
- `Published`: Indicates that the content is published.

## Managers

### BaseContentManager
The `BaseContentManager` is a manager class that provides a method for querying published content objects. It includes the following method:
- `published()`: Returns a queryset of published content objects.


## Serializers

### ContentDetailMethodSerializer
The `ContentSerializer` is a base serializer which provides following fields:
- `viewers_count`: The number of viewers of the content.
- `content_type_id`: The content type id of the content's model

## Views

### ContentListCreateView
The `ContentListCreateView` is a core view configuration for creating and listing content. It handles the following HTTP methods:
- `GET`: Retrieves a list of content objects.
- `POST`: Creates a new content object.

### ContentDetailView
The `ContentDetailView` is a core view configuration for retrieving, updating, and deleting a specific content object. It handles the following HTTP methods:
- `GET`: Retrieves a specific content object.
- `PUT`: Updates a specific content object.
- `DELETE`: Deletes a specific content object.
