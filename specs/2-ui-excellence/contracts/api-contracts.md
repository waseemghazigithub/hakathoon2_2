# API Contracts: UI Excellence Frontend

**Feature**: 2-ui-excellence
**Date**: 2026-02-06

## Overview

This document defines the API contracts that the frontend will interact with. These contracts specify the expected request/response formats for all API communications.

## Authentication Endpoints

### POST /api/auth/login
Authenticate user and return JWT token

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Successful Response (200):**
```json
{
  "success": true,
  "user": {
    "id": "string",
    "email": "string",
    "name": "string"
  },
  "token": "string"
}
```

**Error Response (401):**
```json
{
  "success": false,
  "error": "string"
}
```

### POST /api/auth/register
Register new user and return JWT token

**Request Body:**
```json
{
  "email": "string",
  "password": "string",
  "name": "string"
}
```

**Successful Response (201):**
```json
{
  "success": true,
  "user": {
    "id": "string",
    "email": "string",
    "name": "string"
  },
  "token": "string"
}
```

## Task Management Endpoints

### GET /api/tasks
Retrieve all tasks for the authenticated user

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Successful Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "completed": false,
      "createdAt": "string",
      "updatedAt": "string",
      "userId": "string"
    }
  ]
}
```

### POST /api/tasks
Create a new task for the authenticated user

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Request Body:**
```json
{
  "title": "string",
  "description": "string"
}
```

**Successful Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "string",
    "title": "string",
    "description": "string",
    "completed": false,
    "createdAt": "string",
    "updatedAt": "string",
    "userId": "string"
  }
}
```

### PUT /api/tasks/{id}
Update an existing task

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Request Body:**
```json
{
  "title": "string",
  "description": "string",
  "completed": "boolean"
}
```

**Successful Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "updatedAt": "string"
  }
}
```

### DELETE /api/tasks/{id}
Delete a task

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Successful Response (200):**
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

### PATCH /api/tasks/{id}/toggle-complete
Toggle the completion status of a task

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Successful Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "string",
    "completed": "boolean",
    "updatedAt": "string"
  }
}
```

## Error Responses

### General Error Format
```json
{
  "success": false,
  "error": "string",
  "message": "string"
}
```

### Common Status Codes
- 400: Bad Request - Invalid request format
- 401: Unauthorized - Missing or invalid JWT token
- 403: Forbidden - Insufficient permissions
- 404: Not Found - Resource does not exist
- 422: Unprocessable Entity - Validation error
- 500: Internal Server Error - Unexpected server error

## Headers

### Required Headers for Authenticated Requests
- `Authorization: Bearer {jwt_token}`
- `Content-Type: application/json`

### Response Headers
- `Content-Type: application/json`
- `Cache-Control: no-cache` (for sensitive data)