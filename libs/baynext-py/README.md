# Baynext CLI

🚀 A powerful command-line interface for managing projects and teams via the Project Management API.

## Installation

```bash
pip install baynext
uvx baynext
```

Or install from source:

```bash
git clone <repository>
cd baynext
pip install -e .
```

## Quick Start

1. **Configure API URL** (if not using default localhost):
   ```bash
   baynext config --api-url https://your-api-server.com
   ```

2. **Register a new account**:
   ```bash
   baynext auth register --email user@example.com --username myuser
   ```

3. **Login**:
   ```bash
   baynext auth login --user user@example.com
   ```

4. **Create your first project**:
   ```bash
   baynext project create --name "My Project" --description "A cool project"
   ```

## Authentication Commands

```bash
# Register new user
baynext auth register --email user@example.com --username myuser --first-name John --last-name Doe

# Login and get token
baynext auth login --user user@example.com

# Check authentication status
baynext auth status

# Show current token
baynext auth token

# Logout
baynext auth logout
```

## User Commands

```bash
# Show current user info
baynext user me

# Update profile
baynext user update --first-name John --last-name Doe

# List user's projects
baynext user projects
```

## Project Commands

```bash
# Create project
baynext project create --name "My Project" --description "Project description"

# List all projects
baynext project list

# Show project details
baynext project show <project-id>

# Update project
baynext project update <project-id> --name "New Name" --description "New description"

# Delete project
baynext project delete <project-id>

# List project members
baynext project members <project-id>

# Add member to project
baynext project add-member <project-id> --email user@example.com --role editor

# Remove member from project
baynext project remove-member <project-id> <user-id>

# Leave a project
baynext project leave <project-id>
```

## Configuration

```bash
# Set API URL
baynext config --api-url https://api.example.com

# Show current config
baynext config --show
```

## Features

- 🔐 **Secure Authentication**: OAuth2 Bearer token authentication
- 👤 **User Management**: Register, login, profile management
- 📁 **Project Management**: Create, update, delete, and manage projects
- 👥 **Team Collaboration**: Add/remove members, role-based access control
- ⚙️ **Configuration**: Flexible API endpoint configuration
- 🎨 **Rich CLI**: Colorful output with emojis and clear formatting
- 🛡️ **Error Handling**: Comprehensive error messages and status codes

## Roles

- **Admin**: Full project management rights (add/remove members, update project)
- **Editor**: Can edit project content
- **Viewer**: Read-only access to project

## Example Workflow

```bash
# Setup
baynext config --api-url https://your-api.com
baynext auth register --email john@example.com --username john
baynext auth login --user john@example.com

# Create and manage project
baynext project create --name "Website Redesign" --description "Redesigning company website"
baynext project add-member <project-id> --email jane@example.com --role editor
baynext project members <project-id>

# Check your projects
baynext user projects
```

## Requirements

- Python 3.8+
- Active Project Management API server
- Network connectivity to API server

