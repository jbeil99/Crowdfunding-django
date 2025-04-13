# Crowdfunding API Documentation

This document provides details about the API endpoints for a crowdfunding platform where users can create projects, donate to projects, comment, rate, and report inappropriate content.
## Documentation Structure
This project's documentation is split into multiple files:
- [Main API Documentation](README.md) - Projects, comments, ratings and other core features
- [Authentication Documentation](AUTH.md) - User registration, authentication and profile management

## Table of Contents
- [Authentication](#authentication)
- [Projects](#projects)
- [Comments](#comments)
- [Ratings](#ratings)
- [Reports](#reports)
- [Donations](#donations)
- [Categories](#categories)

## Authentication

Most endpoints require authentication using JWT tokens. Include the token in the header:
```
Authorization: Bearer <your_token>
```

Public endpoints (GET methods) generally don't require authentication.

## Projects

### List Projects
- **URL**: `/api/projects`
- **Method**: `GET`
- **Auth required**: No
- **Query Parameters**:
  ```
  ?is_featured=true
  ?category=1
  ?user_id=5
  ?limit=10
  ?is_top=true
  ?latest=true
  ?search=keyword
  ?tags=tag1,tag2
  ```
- **Success Response**:
  ```json
  {
    "count": 20,
    "next": "http://example.com/api/projects?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "title": "Project Title",
        "details": "Project description...",
        "images": [],
        "total_target": 10000,
        "start_time": "2025-05-01T00:00:00Z",
        "end_time": "2025-06-01T00:00:00Z",
        "user": 1,
        "tags": ["tech", "education"],
        "is_featured": false,
        "rating": 4.5,
        "total_donations": 2500,
        "category": 1,
        "thumbnail_url": "http://example.com/media/thumbnails/project1.jpg",
        "is_active": true,
        "created_at": "2025-04-01T12:00:00Z",
        "category_detail": {
          "id": 1,
          "title": "Technology",
          "description": "Tech projects"
        },
        "backers_count": 15,
        "review_count": 8,
        "is_accepted": true
      }
    ]
  }
  ```

### Create Project
- **URL**: `/api/projects`
- **Method**: `POST`
- **Auth required**: Yes
- **Request Body**:
  ```json
  {
    "title": "New Project",
    "details": "This is a detailed description of the project...",
    "total_target": 15000,
    "start_time": "2025-05-01T00:00:00Z",
    "end_time": "2025-07-01T00:00:00Z",
    "tags": ["innovation", "sustainability"],
    "category": 3,
    "thumbnail": "[binary file]"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "id": 5,
    "title": "New Project",
    "details": "This is a detailed description of the project...",
    "created_at": "2025-04-13T14:30:00Z",
    "images": [],
    "total_target": 15000,
    "start_time": "2025-05-01T00:00:00Z",
    "end_time": "2025-07-01T00:00:00Z",
    "owner": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com"
    },
    "tags": ["innovation", "sustainability"],
    "is_featured": false,
    "total_donations": 0,
    "category": {
      "id": 3,
      "title": "Sustainability",
      "description": "Projects focused on environmental sustainability"
    },
    "thumbnail": "http://example.com/media/thumbnails/newproject.jpg",
    "backers_count": 0,
    "review_count": 0,
    "is_active": true,
    "is_accepted": false,
    "rating": 0
  }
  ```

### Get Project Details
- **URL**: `/api/projects/<id>/`
- **Method**: `GET`
- **Auth required**: No
- **Success Response**:
  ```json
  {
    "id": 1,
    "title": "Project Title",
    "details": "Project description...",
    "created_at": "2025-04-01T12:00:00Z",
    "images": [
      {
        "id": 1,
        "image_url": "http://example.com/media/projects/image1.jpg",
        "title": "Project Image 1",
        "uploaded_at": "2025-04-01T12:00:00Z"
      }
    ],
    "total_target": 10000,
    "start_time": "2025-05-01T00:00:00Z",
    "end_time": "2025-06-01T00:00:00Z",
    "owner": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com"
    },
    "tags": ["tech", "education"],
    "is_featured": false,
    "total_donations": 2500,
    "category": {
      "id": 1,
      "title": "Technology",
      "description": "Tech projects"
    },
    "thumbnail": "http://example.com/media/thumbnails/project1.jpg",
    "backers_count": 15,
    "review_count": 8,
    "is_active": true,
    "is_accepted": true,
    "rating": 4.5
  }
  ```

### Update Project
- **URL**: `/api/projects/<id>/`
- **Method**: `PUT` or `PATCH`
- **Auth required**: Yes (Owner or Admin)
- **Request Body** (`PATCH` - partial update example):
  ```json
  {
    "title": "Updated Title",
    "total_target": 20000
  }
  ```
- **Success Response**:
  ```json
  {
    "id": 1,
    "title": "Updated Title",
    "details": "Project description...",
    "created_at": "2025-04-01T12:00:00Z",
    "images": [...],
    "total_target": 20000,
    "start_time": "2025-05-01T00:00:00Z",
    "end_time": "2025-06-01T00:00:00Z",
    "owner": {...},
    "tags": ["tech", "education"],
    "is_featured": false,
    "total_donations": 2500,
    "category": {...},
    "thumbnail": "http://example.com/media/thumbnails/project1.jpg",
    "backers_count": 15,
    "review_count": 8,
    "is_active": true,
    "is_accepted": true,
    "rating": 4.5
  }
  ```

### Delete Project
- **URL**: `/api/projects/<id>/`
- **Method**: `DELETE`
- **Auth required**: Yes (Admin only)
- **Success Response**: `200 OK`
  ```json
  {
    "id": 1,
    "title": "Project Title",
    "details": "Project description...",
    "images": [...],
    "total_target": 10000,
    "start_time": "2025-05-01T00:00:00Z",
    "end_time": "2025-06-01T00:00:00Z",
    "user": 1,
    "tags": ["tech", "education"],
    "is_featured": false,
    "rating": 4.5,
    "total_donations": 2500,
    "category": 1,
    "thumbnail_url": "http://example.com/media/thumbnails/project1.jpg",
    "is_active": true,
    "created_at": "2025-04-01T12:00:00Z",
    "category_detail": {...},
    "backers_count": 15,
    "review_count": 8,
    "is_accepted": true
  }
  ```

### Mark Project as Featured
- **URL**: `/api/projects/<id>/featured`
- **Method**: `PATCH`
- **Auth required**: Yes (Admin only)
- **Request Body**:
  ```json
  {
    "is_featured": true
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "id": 1,
    "title": "Project Title",
    "details": "Project description...",
    "images": [...],
    "total_target": 10000,
    "start_time": "2025-05-01T00:00:00Z",
    "end_time": "2025-06-01T00:00:00Z",
    "user": 1,
    "tags": ["tech", "education"],
    "is_featured": true,
    "rating": 4.5,
    "total_donations": 2500,
    "category": 1,
    "thumbnail_url": "http://example.com/media/thumbnails/project1.jpg",
    "is_active": true,
    "created_at": "2025-04-01T12:00:00Z",
    "category_detail": {...},
    "backers_count": 15,
    "review_count": 8,
    "is_accepted": true
  }
  ```

### Cancel Project
- **URL**: `/api/projects/<id>/cancel`
- **Method**: `PATCH`
- **Auth required**: Yes (Owner or Admin)
- **Success Response**: `200 OK`
  ```json
  {
    "message": "Project successfully canceled"
  }
  ```

## Comments

### List Project Comments
- **URL**: `/api/projects/<id>/comments`
- **Method**: `GET`
- **Auth required**: No
- **Success Response**:
  ```json
  {
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "body": "This is a great project!",
        "user": {
          "id": 2,
          "username": "jane_smith",
          "email": "jane@example.com"
        },
        "created_at": "2025-04-05T10:15:00Z",
        "project": 1
      }
    ]
  }
  ```

### Add Comment to Project
- **URL**: `/api/projects/<id>/comments`
- **Method**: `POST`
- **Auth required**: Yes
- **Request Body**:
  ```json
  {
    "body": "I'm excited about this project!"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "id": 6,
    "body": "I'm excited about this project!",
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com"
    },
    "created_at": "2025-04-13T15:20:00Z",
    "project": 1
  }
  ```

### Get Comment Details
- **URL**: `/api/comments/<id>`
- **Method**: `GET`
- **Auth required**: No
- **Success Response**:
  ```json
  {
    "id": 1,
    "body": "This is a great project!",
    "user": {
      "id": 2,
      "username": "jane_smith",
      "email": "jane@example.com"
    },
    "created_at": "2025-04-05T10:15:00Z",
    "project": 1
  }
  ```

### Delete Comment
- **URL**: `/api/comments/<id>`
- **Method**: `DELETE`
- **Auth required**: Yes (Owner or Admin)
- **Success Response**: `200 OK`
  ```json
  {
    "id": 1,
    "body": "This is a great project!",
    "user": {
      "id": 2,
      "username": "jane_smith",
      "email": "jane@example.com"
    },
    "created_at": "2025-04-05T10:15:00Z",
    "project": 1
  }
  ```

## Ratings

### List Project Ratings
- **URL**: `/api/projects/<id>/ratings`
- **Method**: `GET`
- **Auth required**: No
- **Success Response**:
  ```json
  {
    "count": 8,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "rate": 5.0,
        "user": {
          "id": 2,
          "username": "jane_smith",
          "email": "jane@example.com"
        },
        "created_at": "2025-04-03T09:45:00Z",
        "project": 1
      }
    ]
  }
  ```

### Rate a Project
- **URL**: `/api/projects/<id>/ratings`
- **Method**: `POST`
- **Auth required**: Yes
- **Request Body**:
  ```json
  {
    "rate": 4.5
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "id": 9,
    "rate": 4.5,
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com"
    },
    "created_at": "2025-04-13T15:30:00Z",
    "project": 1
  }
  ```

### Get Rating Details
- **URL**: `/api/projects/ratings/<id>`
- **Method**: `GET`
- **Auth required**: No
- **Success Response**:
  ```json
  {
    "id": 1,
    "rate": 5.0,
    "user": {
      "id": 2,
      "username": "jane_smith",
      "email": "jane@example.com"
    },
    "created_at": "2025-04-03T09:45:00Z",
    "project": 1
  }
  ```

### Delete Rating
- **URL**: `/api/projects/ratings/<id>`
- **Method**: `DELETE`
- **Auth required**: Yes (Owner or Admin)
- **Success Response**: `200 OK`
  ```json
  {
    "id": 1,
    "rate": 5.0,
    "user": {
      "id": 2,
      "username": "jane_smith",
      "email": "jane@example.com"
    },
    "created_at": "2025-04-03T09:45:00Z",
    "project": 1
  }
  ```

## Reports

### List Project Reports
- **URL**: `/api/projects/<id>/reports`
- **Method**: `GET`
- **Auth required**: Yes (Admin only)
- **Success Response**:
  ```json
  {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "reason": "Inappropriate content",
        "user": {
          "id": 3,
          "username": "alice_jones",
          "email": "alice@example.com"
        },
        "created_at": "2025-04-10T08:20:00Z",
        "project": 1
      }
    ]
  }
  ```

### Report a Project
- **URL**: `/api/projects/<id>/reports`
- **Method**: `POST`
- **Auth required**: Yes
- **Request Body**:
  ```json
  {
    "reason": "Misleading information"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "id": 3,
    "reason": "Misleading information",
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com"
    },
    "created_at": "2025-04-13T15:40:00Z",
    "project": 1
  }
  ```

### List Comment Reports
- **URL**: `/api/comments/<id>/reports`
- **Method**: `GET`
- **Auth required**: Varies (Public for specific report, Admin for all)
- **Success Response**:
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "reason": "Offensive language",
        "user": {
          "id": 3,
          "username": "alice_jones",
          "email": "alice@example.com"
        },
        "created_at": "2025-04-11T14:20:00Z",
        "comment": 2
      }
    ]
  }
  ```

### Report a Comment
- **URL**: `/api/comments/<id>/reports`
- **Method**: `POST`
- **Auth required**: Yes
- **Request Body**:
  ```json
  {
    "reason": "Spam content"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "id": 2,
    "reason": "Spam content",
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com"
    },
    "created_at": "2025-04-13T15:45:00Z",
    "comment": 2
  }
  ```

### Delete Report
- **URL**: `/api/projects/reports/<id>` or `/api/comments/reports/<id>`
- **Method**: `DELETE`
- **Auth required**: Yes (Owner or Admin)
- **Success Response**: `200 OK`
  ```json
  {
    "id": 1,
    "reason": "Inappropriate content",
    "user": {
      "id": 3,
      "username": "alice_jones",
      "email": "alice@example.com"
    },
    "created_at": "2025-04-10T08:20:00Z",
    "project": 1
  }
  ```

## Donations

### List Project Donations
- **URL**: `/api/projects/<id>/donations`
- **Method**: `GET`
- **Auth required**: No
- **Success Response**:
  ```json
  {
    "count": 15,
    "next": null,
    "previous": null,
    "results": [
      {
        "amount": 500,
        "project": {
          "id": 1,
          "title": "Project Title",
          "details": "Project description...",
          "images": [],
          "total_target": 10000,
          "start_time": "2025-05-01T00:00:00Z",
          "end_time": "2025-06-01T00:00:00Z",
          "user": 1,
          "tags": ["tech", "education"],
          "is_featured": false,
          "rating": 4.5,
          "total_donations": 2500,
          "category": 1,
          "thumbnail_url": "http://example.com/media/thumbnails/project1.jpg",
          "is_active": true,
          "created_at": "2025-04-01T12:00:00Z",
          "category_detail": {...},
          "backers_count": 15,
          "review_count": 8,
          "is_accepted": true
        },
        "user": {
          "id": 2,
          "username": "jane_smith",
          "email": "jane@example.com"
        },
        "created_at": "2025-04-05T11:30:00Z"
      }
    ]
  }
  ```

### Make a Donation
- **URL**: `/api/projects/<id>/donations`
- **Method**: `POST`
- **Auth required**: Yes
- **Request Body**:
  ```json
  {
    "amount": 100
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "amount": 100,
    "project": {
      "id": 1,
      "title": "Project Title",
      "details": "Project description...",
      "images": [],
      "total_target": 10000,
      "start_time": "2025-05-01T00:00:00Z",
      "end_time": "2025-06-01T00:00:00Z",
      "user": 1,
      "tags": ["tech", "education"],
      "is_featured": false,
      "rating": 4.5,
      "total_donations": 2600,
      "category": 1,
      "thumbnail_url": "http://example.com/media/thumbnails/project1.jpg",
      "is_active": true,
      "created_at": "2025-04-01T12:00:00Z",
      "category_detail": {...},
      "backers_count": 16,
      "review_count": 8,
      "is_accepted": true
    },
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com"
    },
    "created_at": "2025-04-13T15:50:00Z"
  }
  ```

### Get Donation Details
- **URL**: `/api/projects/donation/<id>`
- **Method**: `GET`
- **Auth required**: No
- **Success Response**:
  ```json
  {
    "amount": 500,
    "project": {
      "id": 1,
      "title": "Project Title",
      "details": "Project description...",
      "images": [],
      "total_target": 10000,
      "start_time": "2025-05-01T00:00:00Z",
      "end_time": "2025-06-01T00:00:00Z",
      "user": 1,
      "tags": ["tech", "education"],
      "is_featured": false,
      "rating": 4.5,
      "total_donations": 2600,
      "category": 1,
      "thumbnail_url": "http://example.com/media/thumbnails/project1.jpg",
      "is_active": true,
      "created_at": "2025-04-01T12:00:00Z",
      "category_detail": {...},
      "backers_count": 16,
      "review_count": 8,
      "is_accepted": true
    },
    "user": {
      "id": 2,
      "username": "jane_smith",
      "email": "jane@example.com"
    },
    "created_at": "2025-04-05T11:30:00Z"
  }
  ```

## Categories

### List Categories
- **URL**: `/api/category`
- **Method**: `GET`
- **Auth required**: No
- **Success Response**:
  ```json
  [
    {
      "id": 1,
      "title": "Technology",
      "description": "Tech projects",
      "created_at": "2025-03-15T09:00:00Z"
    },
    {
      "id": 2,
      "title": "Art & Culture",
      "description": "Creative projects related to art and culture",
      "created_at": "2025-03-15T09:05:00Z"
    }
  ]
  ```

### Create Category
- **URL**: `/api/category`
- **Method**: `POST`
- **Auth required**: Yes (Admin only)
- **Request Body**:
  ```json
  {
    "title": "Education",
    "description": "Projects focused on educational initiatives and learning"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "id": 3,
    "title": "Education",
    "description": "Projects focused on educational initiatives and learning",
    "created_at": "2025-04-13T16:00:00Z"
  }
  ```