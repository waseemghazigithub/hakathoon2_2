---
id: 1
title: Update Constitution to Spec Driven Development Principles
stage: constitution
date: 2026-02-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution, spec-driven-development, governance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
Spec Constitution — Master Prompt
Role & Authority

You are operating under a Spec-Driven Development Constitution.
All design, implementation, refactoring, and decisions MUST be governed by the specifications defined in the /specs directory.

Specifications are the single source of truth.
Code, architecture, and behavior MUST conform to specs — not the other way around.

If a conflict exists between code and specs, the specs always win.

Governing Principles
1. Specs Are Law

All features MUST be implemented exactly as described in:

/specs/features/*

/specs/api/*

/specs/database/*

/specs/ui/*

No undocumented features may be added

No assumptions may override written specs

2. Architecture First

All implementation MUST align with:

System architecture specs

JWT-based authentication model

Monorepo structure

Layered CLAUDE.md guidance

SubAI Agent + Skills architecture

No shortcut, coupling, or architectural deviation is allowed without updating specs first.

3. Authentication & Security Are Mandatory

All backend endpoints MUST:

Require valid JWT authentication

Derive user identity ONLY from JWT

NEVER trust user_id from request input

Enforce user-level data isolation

Return 401 for unauthenticated access

Security rules defined in specs are non-negotiable.

4. API Contract Supremacy

All frontend and backend interactions MUST:

Follow /specs/api/rest-endpoints.md

Use documented request/response formats

Use JWT-based authentication headers

Maintain backward compatibility unless specs are updated

If frontend and backend disagree, specs decide.

5. Database Ownership & Integrity

All data access MUST:

Use SQLModel

Enforce foreign key ownership

Filter all user data by authenticated user

Follow /specs/database/schema.md

Maintain indexes and performance constraints

No direct database access outside ORM patterns.

6. Monorepo & Spec-Kit Compliance

All changes MUST:

Respect monorepo structure

Keep frontend and backend in their designated folders

Reference specs using @specs/...

Follow Root, Frontend, and Backend CLAUDE.md rules

Claude Code MUST be able to reason across the full stack.

7. Agentic Development Rules

All agents MUST:

Operate within their defined responsibilities

Respect agent boundaries (Frontend, Backend, Architecture, Testing, etc.)

Not perform out-of-scope work

Route cross-cutting concerns through Architecture Planner Agent

Use Skills abstraction for AI-driven behavior

Agents may NOT bypass skills or directly access restricted layers.

8. Change Management

If implementation requires behavior not covered by specs:

STOP implementation

Propose spec update

Update relevant spec files

Re-run implementation based on updated specs

No silent divergence between code and specs is allowed.

9. Testing & Validation

All features MUST:

Satisfy acceptance criteria in feature specs

Pass integration workflows

Enforce auth and data isolation

Maintain frontend-backend contract compatibility

Integration Tester Agent is authoritative for cross-service correctness.

10. Hackathon Evaluation Alignment

The system MUST demonstrate:

Clear spec-driven workflow

Stateless JWT authentication

Proper layering (UI, API, DB, Agents, Skills)

Extensible architecture for AI agents

Professional-grade separation of concerns

Architecture clarity and spec adherence are considered first-class success criteria.

Enforcement Statement (Hard Rule)

If a request, instruction, or implementation:

Conflicts with specs

Bypasses authentication

Breaks user isolation

Violates architecture

Introduces undocumented behavior

Then it MUST be rejected or corrected by updating specs first.

One-Line Constitution Summary (For Tools & Agents)

All system behavior, architecture, and implementation MUST be derived from and governed by Spec-Kit specifications; no code, agent, or feature may override or bypass written specs.
```

## Response snapshot

The project constitution has been successfully updated based on your input. Here's the summary:

## Constitution Update Summary

**New Version**: 1.0.0 (Initial version based on user input)
**Version Bump Rationale**: This is the first version of the constitution based on the Spec-Driven Development principles provided in your input. The constitution now reflects 10 core governing principles that will guide all development activities.

**Changes Made**:
- Replaced all template placeholder tokens with concrete values based on your input
- Created a comprehensive constitution with 10 governing principles:
  1. Specs Are Law
  2. Architecture First
  3. Authentication & Security Are Mandatory
  4. API Contract Supremacy
  5. Database Ownership & Integrity
  6. Monorepo & Spec-Kit Compliance
  7. Agentic Development Rules
  8. Change Management
  9. Testing & Validation
  10. Hackathon Evaluation Alignment
- Included enforcement statement and governance rules
- Added version tracking (Version: 1.0.0, Ratified: 2026-02-06)

**Files Updated**:
- `.specify/memory/constitution.md` (fully updated with new constitution)

**Consistency Check**:
- Verified compatibility with existing templates (plan, spec, tasks, ADR, checklist)
- No conflicts identified with dependent artifacts

**Suggested Commit Message**:
`docs: amend constitution to v1.0.0 (Spec-Driven Development principles)`

The constitution is now ready for use and will govern all future development activities according to the Spec-Driven Development approach you specified.

## Outcome

- ✅ Impact: Successfully updated constitution file with Spec-Driven Development principles
- 🧪 Tests: none (documentation update)
- 📁 Files: Updated .specify/memory/constitution.md with comprehensive governance document
- 🔁 Next prompts: Ready for development activities guided by new constitution
- 🧠 Reflection: Constitution now serves as authoritative source for all future development decisions

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - All template placeholders properly replaced
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementing features according to new constitution guidelines