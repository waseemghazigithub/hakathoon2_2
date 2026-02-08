---
id: 1
title: Create Frontend Todo App Specification
stage: spec
date: 2026-02-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: 1-frontend-todo-app
branch: 1-frontend-todo-app
user: user
command: /sp.specify
labels: [frontend, todo-app, authentication, nextjs]
links:
  spec: specs/1-frontend-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-frontend-todo-app/spec.md
 - specs/1-frontend-todo-app/checklists/requirements.md
tests:
 - none
---

## Prompt

```text
Frontend sp.specify — Master Prompt
Mode: Frontend-Only Implementation

You are now operating in Frontend-Only Spec Mode.

Your task is to design and implement the complete Next.js frontend according to the specifications, while treating backend and database as external, stable services.

Ignore backend implementation details except where API contracts and authentication integration are required for frontend correctness.

Scope (What You MUST Do)

You MUST fully specify and implement the frontend layer, including:

1. Next.js App Router Structure

Define /app routing structure

Define layouts and route groups

Implement protected and public routes

Define loading and error boundaries

2. Authentication UI & Session Handling

Implement Better Auth integration in Next.js

Implement signup and signin pages

Implement session retrieval and auth-aware layouts

Implement protected routes and redirects

Handle unauthenticated vs authenticated states

3. API Client Layer

Design and implement /lib/api.ts

Centralize all backend communication

Automatically attach JWT token to requests

Implement consistent error handling

Define typed frontend API functions (getTasks, createTask, etc.)

4. Core UI Pages (Todo App)

You MUST fully specify and implement:

Tasks List Page

List user tasks

Show loading and empty states

Show completion status

Create Task UI

Form with validation

Submission states

Edit Task UI

Edit title and description

Task Detail View (if specified)

Delete Task confirmation UI

Toggle complete UI

5. UI Components & Design System

Reusable components:

TaskList

TaskItem

TaskForm

Button, Input, Modal

Tailwind-based consistent styling

Responsive layouts

Accessibility basics

6. State, UX & Error Handling

Loading indicators

Optimistic updates (where appropriate)

User-friendly error messages

Form validation feedback

Empty state UX

7. Spec-Kit & UI Specs Alignment

Reference:

@specs/ui/components.md

@specs/ui/pages.md

@specs/features/task-crud.md

@specs/api/rest-endpoints.md

Update UI specs if gaps are found

Treat UI specs as source of truth

Explicit Constraints (What You MUST NOT Do)

Do NOT modify backend code

Do NOT modify database schema

Do NOT implement FastAPI routes

Do NOT implement AI agents or skills

Do NOT bypass authentication

Do NOT hardcode user_id

Do NOT directly access database

Authentication Rules (Frontend)

Always use Better Auth session APIs

Always retrieve JWT from Better Auth session

Always attach JWT via Authorization header

Never store JWT in localStorage manually

Rely on Better Auth session handling

API Contract Rules (Frontend)

All API calls go through /lib/api.ts

Do NOT call fetch directly in components

Match request/response to API specs

Handle 401 errors with redirect to login

Deliverables

You MUST produce:

Complete Next.js App Router frontend

Auth pages and protected layouts

Centralized API client

Full Todo UI flows

Reusable UI components

Loading, error, and empty states

Updated UI specs if needed

Success Criteria

Frontend is conside
```

## Response snapshot

Successfully created a comprehensive specification for the frontend todo app with authentication. The specification includes:

- Three prioritized user stories covering authentication (P1), task management (P2), and task operations (P3)
- Detailed acceptance scenarios for each user story
- Identified edge cases for authentication, error handling, and empty states
- 15 functional requirements covering authentication, task operations, error handling, and accessibility
- Two key entities (User and Task)
- Six measurable success criteria focusing on performance, reliability, and user experience

Also created a quality checklist that validates all requirements have been met. The specification is ready for the planning phase.

## Outcome

- ✅ Impact: Created complete feature specification for frontend todo app
- 🧪 Tests: none (specification document)
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Ready for /sp.plan to create implementation plan
- 🧠 Reflection: Specification follows Spec-Driven Development principles with clear user value focus

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - All specification requirements met
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase with /sp.plan