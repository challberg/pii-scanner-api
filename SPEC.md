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
- **Frontend**: React + Vite

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

## Frontend Pages

| Page | Route | Description |
|------|-------|-------------|
| Login | `/login` | User authentication |
| Register | `/register` | Create new account |
| Dashboard | `/dashboard` | Home page with search history |
| Scan Form | `/scan` | Submit PII for searching |
| Results | `/results/{id}` | View search results |

## Implementation Status

### Phase 1 (MVP) - Complete
- [x] User registration and authentication (email/password)
- [x] User submits PII: name, email, phone, address
- [x] Mock data broker service (5 sources)
- [x] Return results showing what data was found and where
- [x] User dashboard with search history (date/time)

### Phase 2 (Future)
- [ ] Real data broker API integration
- [ ] Automated monitoring and alerts
- [ ] Data removal requests
- [ ] Email notifications

## Next Steps

### 1. Database Setup (Production)
- [ ] Switch from SQLite to PostgreSQL
- [ ] Create PostgreSQL database (ElephantSQL/Supabase/local)
- [ ] Update `.env` with production `DATABASE_URL`
- [ ] Test database migrations

### 2. Real Data Broker Integration
- [ ] Research data broker APIs:
  - WhitePages Pro API
  - BeenVerified API
  - Spokeo API
  - Instant Checkmate API
- [ ] Implement `src/services/real_broker.py`
- [ ] Add API key management
- [ ] Update `src/services/__init__.py` factory
- [ ] Test with real data sources

### 3. Background Processing
- [ ] Add FastAPI BackgroundTasks or Celery
- [ ] Return search ID immediately on submit
- [ ] Poll endpoint for results status
- [ ] WebSocket or polling for frontend updates

### 4. Email Notifications
- [ ] Set up SMTP (SendGrid, Mailgun, AWS SES)
- [ ] Send results via email
- [ ] Optional: monitoring alerts
- [ ] Unsubscribe mechanism

### 5. Deployment
- [ ] Add Dockerfile
- [ ] Deploy to Railway/Render/Fly.io
- [ ] Set up CI/CD pipeline
- [ ] Environment configuration
- [ ] Domain setup

### 6. Security Hardening
- [ ] Add audit logging for all data access
- [ ] Adjust rate limits for production
- [ ] Input sanitization audit
- [ ] Add HTTPS enforcement
- [ ] Security headers (CSP, HSTS, etc.)

### 7. Additional Features
- [ ] Password reset flow
- [ ] Account deletion
- [ ] Export results (PDF/CSV)
- [ ] Bulk search capabilities
- [ ] Multi-user team accounts