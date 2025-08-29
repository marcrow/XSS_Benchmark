# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About bXSS Benchmark

This is a web application designed to evaluate and benchmark the effectiveness of blind XSS (Cross-Site Scripting) polyglot payloads against various real-world scenarios. It serves as both a security testing platform and XSS training environment.

**Important Security Note**: This application intentionally contains XSS vulnerabilities for testing purposes and should never be exposed publicly without proper security measures.

## Running the Application

```bash
# Start the full application stack
docker compose up --build

# Add hostname to /etc/hosts (required)
sudo echo 'xsslab_app 127.0.0.1' >> /etc/hosts
```

The application will be available at http://xsslab_app:9090

## Development Commands

```bash
# Extract scenarios from master YAML to individual files
bash scripts/extract_scenarios.sh

# Install Python dependencies (if running locally)
pip install -r app/requirements.txt

# Run the Flask app directly (requires PostgreSQL setup)
cd app && python app.py
```

## Architecture Overview

### Core Components

- **Flask Application** (`app/app.py`): Main web server with database connection retry logic
- **Database Models** (`app/models.py`): SQLAlchemy models for Scenario, Payload, and Result entities
- **Scenario Management**: YAML-based scenario definitions with database synchronization
- **Controllers**: Blueprint-based routing for different functionality areas
- **Headless Testing**: Playwright integration for automated XSS payload testing

### Database Structure

- **Scenarios**: XSS test scenarios with HTML/JS snippets and metadata
- **Payloads**: User-submitted XSS payloads for testing
- **Results**: Test outcomes linking payloads to scenarios with success metrics

### Scenario System

Scenarios are defined in YAML files (`app/scenarios/definitions/`) and automatically synchronized to the database on startup. Each scenario contains:
- HTML snippet with `{{ payload }}` template placeholder
- Optional JavaScript snippet
- Category and position metadata
- Template block identifier

### Key Directories

- `app/controllers/`: Flask blueprints for different routes
- `app/scenarios/definitions/`: Individual YAML scenario files
- `app/scenarios/TBD/`: Master scenarios YAML file
- `app/templates/`: Jinja2 HTML templates
- `app/static/`: CSS and JavaScript assets
- `migrations/`: Database migration scripts

## Testing XSS Payloads

### Manual Testing
1. Navigate to `/scenarios` page
2. Select a scenario to test
3. Add `?payload=<your-payload>` to the URL
4. Execute and observe results

### Automated Testing
Use the headless testing endpoint (`/auto_headless`) for systematic payload evaluation across multiple scenarios.

## Adding New Scenarios

1. Add scenario definition to `app/scenarios/TBD/scenarios.yaml`
2. Run `bash scripts/extract_scenarios.sh` to generate individual files
3. Restart application to sync new scenarios to database
4. New scenarios automatically appear in the web interface

## Container Configuration

- **Database**: PostgreSQL 15 with persistent volume
- **Application**: Python 3.12 with Playwright for browser automation
- **Networking**: Bridge network for container communication
- **Environment**: Production Flask mode with debug enabled
