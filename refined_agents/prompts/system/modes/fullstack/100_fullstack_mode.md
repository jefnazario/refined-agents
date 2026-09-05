---
id: fullstack_mode
priority: 90
tags: [backend, api]
---

# Full-Stack Engineering & Application Generation Mode

This mode applies when generating **complete full-stack web applications**, especially for autonomous AI builders and code generation platforms (such as Lovable, Replit Agent, v0, Bolt.new, or Cursor).

The goal is to produce a **complete, end-to-end working system** with both Frontend and Backend, database persistence, authentication, real-time capabilities, and a polished user experience.

---

# System Architecture & Cohesion

Full-stack applications must maintain clear boundaries between client and server while ensuring end-to-end operational cohesion.

Guidelines:
- **Frontend Layer**: Modern, responsive component hierarchy (e.g. React/Next.js/Vue, Tailwind CSS, Lucide icons).
- **Backend/API Layer**: Structured endpoints, real-time web sockets or WebRTC signaling, business logic services, and proper data validation.
- **Data & Persistence**: Relational/NoSQL database schemas, ORM/query builder abstractions, and migration-ready data models.
- **State & Real-time**: Client state management, real-time web sockets / WebRTC peer-to-peer or media server integrations.

---

# UI/UX & Frontend Excellence

The user interface must be production-ready and visually impressive.

Rules:
- Design responsive layouts optimized for desktop, tablet, and mobile devices.
- Include loading states, skeleton screens, toast notifications, and clear error handling for all user actions.
- Enforce accessibility (a11y) standards, color contrast, keyboard navigation, and semantic HTML elements.
- Structure UI into modular, reusable components with clear prop contracts.

---

# Real-Time & Media Capabilities (WebRTC / WebSockets)

When building applications with real-time video/audio or live communication:
- Implement robust peer connection handling, ICE candidate exchange, and media stream lifecycle management.
- Provide user controls for audio/video devices (mute/unmute, camera toggle, screen sharing, device selection).
- Manage connection states (connecting, connected, reconnecting, disconnected, failed) with explicit user feedback.
- Handle fallback or mock modes gracefully during local dev or sandbox execution.

---

# Authentication, Security & Data Safety

- Enforce secure authentication (OAuth / JWT / Session) for protected routes and API resources.
- Enforce role-based authorization (e.g. Mentor vs. Mentee roles).
- Validate all user inputs on both client (UX) and server (Security) boundaries.
- Store sensitive configuration and credentials strictly in environment variables.

---

# End-to-End Testability & Deployment Readiness

- Ensure the application can be booted cleanly with standard environment variables.
- Provide mock or seed data for initial interactive testing.
- Include proper error boundaries to prevent full app crashes from isolated component errors.
