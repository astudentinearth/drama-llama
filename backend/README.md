# Backend Service

The backend service for the Groowy application, built with Spring Boot and Java.

## Overview

This backend provides RESTful APIs for:
- User authentication and authorization
- Job listings and applications management
- Company profiles and management
- User profiles and CV handling
- Learning roadmap and AI interactions
- File uploads (CVs)

## Technology Stack

- **Framework**: Spring Boot 3.x
- **Language**: Java 17+
- **Database**: PostgreSQL
- **Security**: Spring Security with Argon2 password encoding
- **Build Tool**: Maven
- **Authentication**: Session-based authentication

## Architecture

The backend follows a layered architecture:

- **Controllers**: REST API endpoints (`/api/*`)
- **Services**: Business logic layer
- **Repositories**: Data access layer
- **DTOs**: Data transfer objects for API communication
- **Entities**: JPA entities for database mapping

## Key Components

### Authentication & Authorization
- Session-based authentication using Spring Security
- Role-based access control (MEMBER, RECRUITER)
- Argon2 password hashing for security

### Core Modules
- **Auth**: User registration, login, logout, and session management
- **Jobs**: Job listings, applications, and management
- **Company**: Company profiles and job management for recruiters
- **Profile**: User profiles and CV management
- **Roadmap**: Learning sessions and AI interactions (proxied to AI service)
- **Upload**: File upload handling for CVs

### AI Service Integration
The roadmap functionality proxies requests to an external AI service for:
- Learning session management
- AI chat interactions
- Quiz generation and management
- Graduation project handling

## Database Schema

The application uses PostgreSQL with the following main entities:
- `users` - User accounts and authentication
- `user_roles` - User role assignments
- `companies` - Company information
- `job_listings` - Job postings
- `job_applications` - Job applications
- `user_profiles` - User profile information
- `cvs` - CV file references

## Configuration

Key configuration properties:
- Database connection settings
- AI service URL and API key
- Security settings
- File upload configurations

## API Documentation

For detailed API endpoint documentation, see [API.md](./API.md).

## Development

### Prerequisites
- Java 17 or higher
- Maven 3.6+
- PostgreSQL database

### Running the Application

1. Configure database connection in `application.properties`
2. Run database migrations (SQL files in `src/main/resources/db/`)
3. Start the application:
   ```bash
   mvn spring-boot:run
   ```

### Building

```bash
mvn clean package
```

## Dependencies

Key dependencies include:
- Spring Boot Starter Web
- Spring Boot Starter Security
- Spring Boot Starter Data JPA
- Spring Boot Starter Validation
- PostgreSQL Driver
- ModelMapper for DTO conversion
