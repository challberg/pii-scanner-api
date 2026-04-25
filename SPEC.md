# PII Scanner API

## Project Overview
**Name**: PII Scanner API
**Type**: SaaS Security Tool
**Core Functionality**: Allow users to submit PII and receive reports on where their personal data appears on data broker sites and public records.
**Target Users**: Anyone concerned about their online privacy and data exposure.

## Functionality Specification

### Phase 1 (MVP)
- [x] User registration and authentication (email/password)
- [x] User submits PII: name, email, phone, address
- [ ] System queries approved data broker APIs for user data
- [x] Return results showing what data was found and where
- [x] User dashboard with search history

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

## API Endpoints

### Authentication (`/auth`)
| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/auth/register` | POST | Create new account | No |
| `/auth/login` | POST | Get JWT token | No |
| `/auth/me` | GET | Get current user | Yes |

### PII Scanning (`/pii`)
| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/pii/scan` | POST | Submit PII for searching | Yes |
| `/pii/searches` | GET | List past searches | Yes |
| `/pii/searches/{id}` | GET | Get specific search result | Yes |