# Core Module Documentation

Table of Contents:
- [Description](#description)
- [Models](#models)
  - [AbstractToken](#abstracttoken)
- [Celery Tasks](#celery-tasks)
  - [send_email](#send-email)
- [Utils](#utils)
  - [get_content_type_model](#get-content-type-model)
  - [ObjectSource](#objectsource)
- [Managers](#managers)
  - [BaseCacheManager](#basecachemanager)
- [Mixins](#mixins)
  - [ContentTypeModelMixin](#contenttypemodelmixin)
  - [ContentObjectMixin](#contentobjectmixin)

## Description
The Core module serves as the heart of the application, housing essential and reusable functions that contribute to the overall functionality of various components. It encapsulates core operations and utilities, making them easily accessible and maintainable throughout the project.

## Models

### AbstractToken
The `AbstractToken` model plays a crucial role in handling token generation for its subclasses. By utilizing a `UUIDField`, it efficiently manages the storage and retrieval of tokens. This abstraction allows for consistent and secure token handling across different subclasses, promoting code reusability and maintaining a uniform approach to token management throughout the application.

## Celery Tasks

### send_email
The `send_email` task takes `template_name`, `to_email`, and `body` as input and sends an email in the background using Celery.

## Utils

### get_content_type_model
The `get_content_type_model` function returns and caches the content type model of a given model.


### ObjectSource
The `ObjectSource` class is an Enum class that specifies whether an object is saved in cache or the database.

## Managers

### BaseCacheManager
The `BaseCacheManager` is a base manager that uses the `CacheService` to perform operations tasks in the cache.

## Mixins

### ContentTypeModelMixin
The `ContentTypeModelMixin` gets the content type id from url and returns the content type model.

### ContentObjectMixin
The `ContentObjectMixin` first retrieves the content type model and filter the object by id. It then returns the object if it exists, otherwise it raises a `Http404` exception.

## Services

### CacheService
The `CacheService` is a service that handles cache operations. It plays a crucial role in the caching of objects, allowing for efficient retrieval and storage of data. It also provides a consistent interface for performing cache operations, making it easier to maintain and update the cache.