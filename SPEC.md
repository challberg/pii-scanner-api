# PII Scanner API

## Project Overview
**Name**: PII Scanner API
**Type**: SaaS Security Tool
**Core Functionality**: Allow users to submit PII and receive reports on where their personal data appears on data broker sites and public records.
**Target Users**: Anyone concerned about their online privacy and data exposure.

## Functionality Specification

### Phase 1 (MVP)
- [ ] User registration and authentication (email/password)
- [ ] User submits PII: name, email, phone, address
- [ ] System queries approved data broker APIs for user data
- [ ] Return results showing what data was found and where
- [ ] User dashboard with search history

### Phase 2 (Future)
- [ ] Automated monitoring and alerts
- [ ] Data removal requests
- [ ] Email notifications

## Tech Stack
- **Backend**: Python/FastAPI
- **Database**: PostgreSQL
- **Frontend**: React (future)

## Security Requirements
- All PII encrypted at rest and in transit
- No secrets stored in code (use environment variables)
- Rate limiting on all endpoints
- Input validation and sanitization
- Audit logging for all data access

## Data Sources (Phase 1)
- Approved data broker APIs only
- Public records searches where available
- No direct scraping of websites