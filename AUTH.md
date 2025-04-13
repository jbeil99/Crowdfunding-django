# Authentication API Documentation

This document provides details about the authentication endpoints for the crowdfunding platform, including user registration, authentication, profile management, and account deletion.

## Table of Contents
- [JWT Authentication](#jwt-authentication)
- [User Registration](#user-registration)
- [User Management](#user-management)
- [Profile Management](#profile-management)
- [Account Deletion](#account-deletion)
- [Serializers](#serializers)

## JWT Authentication

The application uses Djoser with JWT tokens for authentication. Include the token in the header for authenticated requests:
```
Authorization: Bearer <your_token>
```

### Authentication Endpoints

- **URL**: `/auth/jwt/create/`
- **Method**: `POST`
- **Auth required**: No
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "secure_password"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

### Token Refresh

- **URL**: `/auth/jwt/refresh/`
- **Method**: `POST`
- **Auth required**: No
- **Request Body**:
  ```json
  {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

### Token Verification

- **URL**: `/auth/jwt/verify/`
- **Method**: `POST`
- **Auth required**: No
- **Request Body**:
  ```json
  {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {}
  ```

## User Registration

### Register New User

- **URL**: `/auth/users/`
- **Method**: `POST`
- **Auth required**: No
- **Request Body**:
  ```json
  {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "secure_password",
    "confirm_password": "secure_password",
    "mobile_phone": "01234567890",
    "profile_picture": "[binary file]"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "mobile_phone": "01234567890"
  }
  ```

### Activate User Account

- **URL**: `/auth/users/activation/`
- **Method**: `POST`
- **Auth required**: No
- **Request Body**:
  ```json
  {
    "uid": "MQ",
    "token": "abcdefg12345"
  }
  ```
- **Success Response**: `204 No Content`

## User Management

### Get Current User

- **URL**: `/auth/users/me/`
- **Method**: `GET`
- **Auth required**: Yes
- **Success Response**:
  ```json
  {
    "id": 1,
    "email": "john.doe@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "mobile_phone": "01234567890",
    "profile_picture": "http://example.com/media/profile_pictures/user1.jpg",
    "created_at": "2025-04-01T12:00:00Z"
  }
  ```

### Reset Password

- **URL**: `/auth/users/reset_password/`
- **Method**: `POST`
- **Auth required**: No
- **Request Body**:
  ```json
  {
    "email": "john.doe@example.com"
  }
  ```
- **Success Response**: `204 No Content`

### Confirm Password Reset

- **URL**: `/auth/users/reset_password_confirm/`
- **Method**: `POST`
- **Auth required**: No
- **Request Body**:
  ```json
  {
    "uid": "MQ",
    "token": "abcdefg12345",
    "new_password": "new_secure_password",
    "re_new_password": "new_secure_password"
  }
  ```
- **Success Response**: `204 No Content`

## Profile Management

### Update User Profile

- **URL**: `/api/profile/update`
- **Method**: `PATCH`
- **Auth required**: Yes
- **Request Body**:
  ```json
  {
    "username": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "mobile_phone": "01234567890",
    "date_of_birth": "1990-01-01",
    "facebook": "https://www.facebook.com/johndoe",
    "country": "Egypt",
    "profile_picture": "[binary file]"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "id": 1,
    "email": "john.doe@example.com",
    "username": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "mobile_phone": "01234567890",
    "profile_picture": "http://example.com/media/profile_pictures/user1.jpg",
    "date_of_birth": "1990-01-01",
    "facebook": "https://www.facebook.com/johndoe",
    "country": "Egypt",
    "created_at": "2025-04-01T12:00:00Z",
    "total_donations": 1500,
    "total_projects_donated": 5,
    "is_staff": false
  }
  ```

### Get User Donations

- **URL**: `/api/users/{user_id}/donations`
- **Method**: `GET`
- **Auth required**: Yes (Owner or Admin)
- **Success Response**:
  ```json
  {
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "amount": 500,
        "project": {
          "id": 1,
          "title": "Project Title",
          "thumbnail_url": "http://example.com/media/thumbnails/project1.jpg"
        },
        "created_at": "2025-04-01T12:00:00Z"
      }
    ]
  }
  ```

## Account Deletion

### Delete User Account

- **URL**: `/auth/users/delete`
- **Method**: `DELETE`
- **Auth required**: Yes
- **Request Body**:
  ```json
  {
    "current_password": "secure_password"
  }
  ```
- **Success Response**: `204 No Content`

