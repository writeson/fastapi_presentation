# FastAPI Presentation
# Introduction

This repository contains an example of a FastAPI application used with a presentation about FastAPI. My goal is this repository is useful as an tool to help developers get up to speed to use the framework to create APIs.

# FastAPI

## What Is FastAPI

FastAPI is a modern, high-performance web framework for building APIs with Python. It is an asynchronous framework that can handle many requests concurrently. It also takes good advantage of type hints to aid with development.

## Why Use FastAPI

The framework has many features that make it attractive:

1. It has very high performance, comparable to NodeJS and Go
2. Developers will realize coding performance improvements as it's fast to code
3. FastAPI has great editor and IDE support
4. It's a robust platform for creating production-ready code
5. Based on open standards for APIs, OpenAPI, previously known as Swagger

## Who Is Using FastAPI

Companies like Microsoft, Uber, Netflix, Expedia Group, and Cisco use FastAPI.

# Example Application

The code that makes up the bulk of this repository is a FastAPI web application that creates CRUD REST APIs to access a database. Rather than create a database from scratch, the code uses the [Chinook database](https://www.sqlitetutorial.net/sqlite-sample-database/) from the [SQLite Tutorial](https://www.sqlitetutorial.net/) website. This is a great resource to learn SQL and has a download link to the database used in the example application.

The ERD (Entity Relationship Diagram) of the database looks like this:

![The ERD diagram of the Chinook database](docs/images/chinook_db_diagram.jpg)

 The database has tables with one-to-many, many-to-many, and self-referential hierarchical tables, which display FastAPIs abilities.

## REST Conventions

REST is more of a convention than a standardized protocol, and I use my convention to create the REST URL endpoints.

The endpoints define a collection of "things" and access to a single "thing." Because they are things, nouns are used as names. I am careful when naming things to avoid awkward plural and singular nouns.
* i.e., Read collection: HTTP GET /api/v1/artists - returns a collection of artists
* i.e., Read single item: HTTP GET /api/v1/artists/1 - returns a single artist with an id of 1

The CRUD behaviors are mapped to these HTTP method verbs:

| CRUD Method | HTTP Method | URL Endpoint         | Action on a thing         |
| :---------- | ----------- | -------------------- | ------------------------- |
| Create      | POST        | /api/v1/artists      | Create new thing          |
| Read        | GET         | /api/v1/artists      | Read collection of things |
| Read        | GET         | /api/v1/artists/{id} | Read singular thing       |
| Update      | PUT         | /api/v1/artists/{id} | Update entire thing       |
| Update      | PATCH       | /api/v1/artists/{id} | Partially update thing    |

> [!NOTE]
>
> In this application, there is no Delete functionality. It's generally a bad idea to delete data from a database. I prefer to have something like an `active` flag that can be True or False to include or exclude the item from the interface. To do this would have meant modifying the Chinook database to add an `active` flag. Doing that would have made it more difficult to reset the database back to its default state, so I chose not to add delete functionality to the API.



## SQLModels

## URL Endpoint Routes

## CRUD Operations

# Resources

[FastAPI Documentation](https://fastapi.tiangolo.com/)

[SQLite Tutorial](https://www.sqlitetutorial.net/)

This is a [YouTube](https://www.youtube.com/watch?v=pkILKAHScrc) video of a presentation I gave to a Python Users group about asynchronous coding. The first half is that presentation.



