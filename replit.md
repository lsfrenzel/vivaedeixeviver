# Diário do Contador - Volunteer Activity Tracker

## Overview

A web application for tracking volunteer activities at the "Viva e Deixe Viver" association. The system allows volunteers to log their storytelling sessions at hospitals, track patient interactions, record books read, and view personalized dashboards with achievement medals based on volunteer hours.

The application is designed mobile-first to support volunteers filling out forms on-the-go at hospital locations. It emphasizes form efficiency, auto-completion features, and positive reinforcement through visual achievement tracking.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture

**Framework**: Flask (Python web framework)
- **Rationale**: Lightweight framework suitable for form-heavy applications with straightforward CRUD operations
- **Key Components**:
  - `app.py`: Application factory with database and authentication initialization
  - `routes.py`: Request handling and business logic
  - `models.py`: Database models using SQLAlchemy ORM
  - `main.py`: Entry point for running the application

**Authentication & Session Management**:
- Flask-Login for user session handling
- Werkzeug password hashing (generate_password_hash/check_password_hash)
- Session-based authentication with user defaults (state, hospital) pre-populated on login
- ProxyFix middleware for handling proxy headers in deployed environments

**Form Processing Strategy**:
- Server-side form validation
- Auto-population of user defaults (volunteer name, state, hospital)
- Date pre-filled with current date
- Support for complex nested data (patient demographics, books, locations) through JSON storage

### Data Storage

**Database**: SQLAlchemy with SQLite/PostgreSQL support
- **Connection Management**: Pool recycling (300s) and pre-ping for reliability
- **Schema Design**:
  - `voluntarios`: User accounts with authentication and default preferences
  - `hospitais`: Hospital reference data organized by state
  - `livros`: Book catalog with autocomplete support (title, author, publisher)
  - `diarios`: Activity logs with foreign key to volunteer, containing structured JSON for complex data

**Data Model Decisions**:
- JSON fields for flexible data structures (patient demographics by age/gender, multiple location checkboxes, multiple books per session)
- Relationship between volunteers and default hospital for form pre-population
- Date-based queries for dashboard statistics (monthly/yearly aggregations)

### Frontend Architecture

**Template Engine**: Jinja2 (Flask default)
- **Layout Pattern**: Base template with block inheritance
- **Key Templates**:
  - `base.html`: Navigation, flash messages, common structure
  - `login.html`: Authentication form
  - `nova_atuacao.html`: Main activity logging form (multi-section card layout)
  - `dashboard.html`: Statistics and achievement display
  - `confirmacao.html`: Post-submission confirmation with summary

**UI Framework**: Bootstrap 5 with Material Design principles
- **Rationale**: Mobile-first responsive framework with accessible form components
- **Form UX Optimizations**:
  - Large touch targets (btn-lg, form-control-lg) for mobile
  - Autocomplete with debounced search for book selection
  - Card-based sections for visual hierarchy
  - Sticky navigation for quick access during long forms

**JavaScript Enhancement**:
- `autocomplete.js`: Async book search with 300ms debounce
- Client-side book selection tracking before form submission
- Dynamic UI updates for adding/removing selected books
- Fallback to manual entry when book not found in database

**Design System** (per design_guidelines.md):
- Typography: Inter/Roboto font family with responsive scale
- Spacing: Tailwind-inspired units (4, 6, 8 for padding/margins)
- Layout: Max-width containers (max-w-2xl) for optimal form readability
- Color scheme: Primary blue with achievement medal variants (gold/silver/bronze gradients)

### External Dependencies

**Python Packages**:
- Flask: Web framework
- Flask-SQLAlchemy: ORM and database abstraction
- Flask-Login: User session management
- Werkzeug: Password hashing and utilities

**Frontend CDN Resources**:
- Bootstrap 5.3.0: UI framework
- Bootstrap Icons 1.11.0: Icon library

**Environment Variables**:
- `SESSION_SECRET`: Flask session encryption key
- `DATABASE_URL`: SQLAlchemy database connection string

**Development Tools**:
- `seed_data.py`: Database population script with sample hospitals, books, and test volunteer account

## Recent Changes

### November 19, 2025 - Initial Release
- Complete implementation of volunteer activity tracking system
- All core features implemented and tested:
  - ✅ User authentication with login/logout
  - ✅ Form with pre-filled date, period selection, and duration input
  - ✅ Patient tracking by age groups (0-3, 4-6, 7-9, 10-12, 13-15, 16-18 years) with gender breakdown
  - ✅ Location checkboxes for hospital areas
  - ✅ Book autocomplete with API integration
  - ✅ Manual book entry when not found in database
  - ✅ Qualitative report text field
  - ✅ Dashboard with statistics, medals (gold/silver/bronze), and monthly chart
  - ✅ Mobile-first responsive design
  - ✅ Database seeded with sample data

**Test Credentials**:
- Email: voluntario@teste.com
- Password: senha123

**Database Structure**:
- PostgreSQL database with 4 main tables
- All volunteer data persisted (authentication, activities, books, hospitals)
- JSON fields for flexible patient demographics and location tracking