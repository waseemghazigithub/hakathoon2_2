<!-- Sync Impact Report:
Version change: N/A → 1.0.0 (Initial version based on user input)
Modified principles: N/A (new constitution created from user input)
Added sections: All 10 governing principles and governance sections from user input
Removed sections: Template placeholder tokens
Templates requiring updates:
- ✅ plan-template.md: Constitution Check section will work with new principles
- ✅ spec-template.md: No direct constitution references to update
- ✅ tasks-template.md: No direct constitution references to update
- ✅ adr-template.md: No direct constitution references to update
- ✅ checklist-template.md: No direct constitution references to update
Follow-up TODOs: None
-->
# Spec Constitution

## Core Principles

### Specs Are Law
All features MUST be implemented exactly as described in: /specs/features/*, /specs/api/*, /specs/database/*, /specs/ui/*. No undocumented features may be added. No assumptions may override written specs.

### Architecture First
All implementation MUST align with: System architecture specs, JWT-based authentication model, Monorepo structure, Layered CLAUDE.md guidance, SubAI Agent + Skills architecture. No shortcut, coupling, or architectural deviation is allowed without updating specs first.

### Authentication & Security Are Mandatory
All backend endpoints MUST: Require valid JWT authentication, Derive user identity ONLY from JWT, NEVER trust user_id from request input, Enforce user-level data isolation, Return 401 for unauthenticated access. Security rules defined in specs are non-negotiable.

### API Contract Supremacy
All frontend and backend interactions MUST: Follow /specs/api/rest-endpoints.md, Use documented request/response formats, Use JWT-based authentication headers, Maintain backward compatibility unless specs is updated. If frontend and backend disagree, specs decide.

### Database Ownership & Integrity
All data access MUST: Use SQLModel, Enforce foreign key ownership, Filter all user data by authenticated user, Follow /specs/database/schema.md, Maintain indexes and performance constraints. No direct database access outside ORM patterns.

### Monorepo & Spec-Kit Compliance
All changes MUST: Respect monorepo structure, Keep frontend and backend in their designated folders, Reference specs using @specs/..., Follow Root, Frontend, and Backend CLAUDE.md rules. Claude Code MUST be able to reason across the full stack.

### Agentic Development Rules
All agents MUST: Operate within their defined responsibilities, Respect agent boundaries (Frontend, Backend, Architecture, Testing, etc.), Not perform out-of-scope work, Route cross-cutting concerns through Architecture Planner Agent, Use Skills abstraction for AI-driven behavior. Agents may NOT bypass skills or directly access restricted layers.

### Change Management
If implementation requires behavior not covered by specs: STOP implementation, Propose spec update, Update relevant spec files, Re-run implementation based on updated specs. No silent divergence between code and specs is allowed.

### Testing & Validation
All features MUST: Satisfy acceptance criteria in feature specs, Pass integration workflows, Enforce auth and data isolation, Maintain frontend-backend contract compatibility. Integration Tester Agent is authoritative for cross-service correctness.

### Hackathon Evaluation Alignment
The system MUST demonstrate: Clear spec-driven workflow, Stateless JWT authentication, Proper layering (UI, API, DB, Agents, Skills), Extensible architecture for AI agents, Professional-grade separation of concerns. Architecture clarity and spec adherence are considered first-class success criteria.

## Enforcement Statement (Hard Rule)
If a request, instruction, or implementation: Conflicts with specs, Bypasses authentication, Breaks user isolation, Violates architecture, Introduces undocumented behavior. Then it MUST be rejected or corrected by updating specs first.

## One-Line Constitution Summary
All system behavior, architecture, and implementation MUST be derived from and governed by Spec-Kit specifications; no code, agent, or feature may override or bypass written specs.

## Governance
For all development activities, the following governance rules apply: Specifications are the single source of truth. Code, architecture, and behavior MUST conform to specs — not the other way around. If a conflict exists between code and specs, the specs always win. All system behavior, architecture, and implementation MUST be derived from and governed by Spec-Kit specifications; no code, agent, or feature may override or bypass written specs.

**Version**: 1.0.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06
