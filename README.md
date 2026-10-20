# Annalis

**Annalis** is a student-focused document sharing platform designed to facilitate the exchange of academic resources. It allows students to upload, share, preview, and track academic documents within a secure and organized environment.

## Description

Annalis solves the problem of scattered academic resources by providing a centralized hub where students can:

*   **Share Documents**: Upload lecture notes, past exams, and project reports (PDF, JPEG, PNG).
*   **Share Metadata**: Categorize documents by subject, sector, academic year, and school year for easy discovery.
*   **Preview Instantly**: View documents directly in the browser without downloading them first.
*   **Track Activity**: See which documents have been recently viewed by peers.
*   **Search & Filter**: Quickly find resources using filters for subject, title, or file type.

The application features secure authentication via **OAuth2/JWT** and is fully containerized for easy deployment.

## Figma Design

[Figma design for Annalis here](https://www.figma.com/design/8bWNCdG3WnCj3kfQ6wwQ4q/APP?node-id=7-23&t=0SBj8s9sRzPSEZXf-1)

## Getting Started

### Prerequisites

Ensure you have the following installed on your machine:

*   **Docker** & **Docker Compose** (v2.20+)
*   **Python 3.12+** (for local backend development)
*   **Node.js 22+** & **npm** (for local frontend development)

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/FuzeTea83/Annalis.git
    cd annalis
    ```

2.  **Configure Environment Variables**
    Copy the example environment file and set your secrets (especially database passwords):
    ```bash
    cp .env.example .env
    ```

3.  **Build Docker Images**
    ```bash
    docker compose build
    ```

### Executing the Application

#### One-Command Launch (Recommended)

You can now start the entire stack (Database, Backend, Frontend) with a single command. The backend will automatically handle database migrations on first startup.

```bash
docker compose up -d
```

This command will:
1.  Start the **MariaDB** database.
2.  Start the **Backend** server.
3.  Start the **Frontend** (Nginx + Vue.js app).

The application will be available at:
*   **Frontend**: `http://localhost:8080`

#### Local Development (Without Docker)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
# Ensure DATABASE_URL in .env points to your local DB or use Docker
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Architecture

The project consists of three main services:

| Service | Description | Technology |
|---|---|---|
| **db** | Relational database for storing users and document metadata | MariaDB 11 |
| **backend** | REST API for authentication, file management, and sharing | Python / FastAPI |
| **frontend** | Student-facing web interface | Vue 3 / Vite / Nginx |

## API Endpoints

The API is prefixed with `/api`. Authentication is required for most endpoints.

### Authentication
*   `POST /api/auth/register` : Create a new student account
*   `POST /api/auth/login` : Authenticate and receive a JWT token

### Documents
*   `POST /api/documents/upload` : Upload a new document (Multipart/Form-Data)
*   `GET /api/documents/view` : List and filter shared documents (paginated)
*   `GET /api/documents/{doc_id}/preview` : Stream a document for in-browser preview
*   `GET /api/documents/{doc_id}/download` : Download a document file
*   `GET /api/documents/recent` : Get documents recently viewed by the current user

### Viewing Logs

To debug issues, stream logs from specific services:

```bash
docker compose logs -f app
docker compose logs -f db
docker compose logs -f proxy
```

## Authors

*  **FuzeTea83** - [GitHub Profile](https://github.com/FuzeTea83)
*  **Hexako** - [GitHub Profile](https://github.com/Hexako)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

*   [FastAPI](https://fastapi.tiangolo.com/)
*   [Vue.js](https://vuejs.org/)
*   [SQLAlchemy](https://www.sqlalchemy.org/)
*   [Docker](https://www.docker.com/)