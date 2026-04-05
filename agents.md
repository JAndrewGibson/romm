# RomM: Agentic Documentation (agents.md)

This document is a comprehensive guide to the RomM (ROM Manager and Player) repository. It is designed to provide AI agents and human developers with a mental model of the project's architecture, technology stack, and development patterns.

---

## 🚀 Project Overview

RomM is a self-hosted ROM manager and player. It allows users to scan, enrich (with metadata), browse, and play their game collection through a responsive web interface.

**Key Features:**
- **In-browser Emulation:** Uses EmulatorJS and Ruffle.
- **Metadata Fetching:** Integrates with IGDB, Screenscraper, MobyGames, and SteamGridDB.
- **Multi-user Support:** Granular permissions and limited access for shared libraries.
- **Advanced Scanning:** Supports various naming schemes, multi-disk games, and custom tags.

---

## 🛠 Technology Stack

### Backend (Python 3.x)
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (High-performance ASGI framework).
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) (with [Alembic](https://alembic.sqlalchemy.org/) for migrations).
- **Database:** MariaDB (Primary) and Redis (Sessions/Caching).
- **Task Runner:** Manual background tasks and scheduled routines using FastAPI's lifespan and standard libraries.
- **Manager:** [uv](https://docs.astral.sh/uv/) (Fast Python package manager).

### Frontend (Node.js)
- **Framework:** [Vue 3](https://vuejs.org/) (Composition API).
- **Build Tool:** [Vite](https://vitejs.dev/).
- **State Management:** [Pinia](https://pinia.vuejs.org/).
- **UI Framework:** [Vuetify 3](https://vuetifyjs.com/) (Material Design).
- **API Client:** Axios (consuming generated types/services from OpenAPI).

---

## 📂 Repository Structure

The project is structured as a monorepo-style application:

```text
romm/
├── backend/            # FastAPI Backend
│   ├── adapters/       # Integration with external providers (IGDB, etc.)
│   ├── alembic/        # Database migration scripts
│   ├── config/         # Application settings and environment handling
│   ├── endpoints/      # API Route definitions
│   ├── handler/        # Business logic and service layers
│   ├── models/         # SQLAlchemy database models
│   ├── tasks/          # Background and scheduled tasks (Scanning, Metadata)
│   ├── watcher.py      # File system watcher for ROM library
│   └── main.py         # Entry point and application setup
├── frontend/           # Vue 3 Frontend
│   ├── src/
│   │   ├── components/ # Reusable UI components
│   │   ├── stores/     # Pinia state stores
│   │   ├── services/   # API client logic
│   │   ├── views/      # Page/View components
│   │   └── __generated__/# Types generated from OpenAPI
│   └── vite.config.js  # Vite configuration
├── docker/             # Docker deployment files
├── pyproject.toml      # Backend dependencies and metadata
├── package.json        # Frontend dependencies and scripts
└── uv.lock             # Python dependency lockfile
```

---

## 🧠 Backend Deep Dive

### 1. API Architecture
- **Routers:** All routers are registered in `backend/main.py`.
- **Naming:** Endpoints are grouped by domain (e.g., `endpoints/roms/`, `endpoints/platform.py`).
- **Middleware:** Includes CORS, CSRF protection, and Redis-based session management.

### 2. Database Models
- Located in `backend/models/`.
- **`rom.py`**: The core model tracking ROMs, their metadata, and user associations.
- **`platform.py`**: Defines supported gaming systems.
- **`user.py`**: User account and permission data.

### 3. Business Logic (Handlers)
- Logic is encapsulated in `backend/handler/`.
- **`handler/rom_handler.py`**: Logic for processing ROMs and their files.
- **`handler/auth/`**: Custom authentication logic (Hybrid basic + OAuth).

### 4. Background Tasks
- **Scanning:** Handled by `watcher.py` (real-time) and `tasks/scheduled/scan_library.py` (periodic).
- **Metadata:** Tasks for enriching ROMs with external data are in `tasks/`.

---

## 🎨 Frontend Deep Dive

### 1. State Management (Pinia)
- Stores are found in `frontend/src/stores/`.
- `auth.ts`: Tracks current user session and permissions.
- `favorites.ts`: Tracks user's favorite games.

### 2. Component Patterns
- **Vuetify:** Heavily used for responsive design and UI components.
- **Generated Services:** Frontend uses `openapi-typescript-codegen` to generate an API client in `src/__generated__`.

### 3. Dynamic Design
- Uses modern CSS features (gradients, smooth transitions).
- Responsive mobile and desktop layouts (Tailwind used sparingly alongside Vuetify).

---

## 🔄 Development Workflow

### **Adding a New Field to a ROM**
1.  **Backend Model**: Update `backend/models/rom.py`.
2.  **Migration**: Run `alembic revision --autogenerate -m "Add new field"`.
3.  **API Response**: Update the Pydantic schemas in `backend/endpoints/responses/` (if any) or ensure the model reflects in the OpenAPI output.
4.  **Frontend Update**: Run `npm run generate` in the `frontend` directory to update types/services.
5.  **UI Integration**: Add the new field to the relevant Vue component/view.

### **Testing & Linting**
- **Backend Tests:** Run `uv run pytest`.
- **Linting:** We use **Trunk**. Run `trunk fmt` and `trunk check` before committing.

---

## 🛠 Key Domain Logic Patterns

### **ROM Scanning Process**
1.  **Discovery:** Files are detected on disk.
2.  **Identification:** Search by hash or filename.
3.  **Metadata Enrichment:** Fetch from providers (ScreenScraper is a primary source).
4.  **Resource Generation:** Generate WebP covers and screenshots.

---

## 📝 Tips for AI Agents
- **Pathing**: Use absolute paths for file system operations when in doubt.
- **Dependencies**: Use `uv` for python dependencies and `npm` for frontend.
- **Migrations**: Always verify that database changes are accompanied by an Alembic migration.
- **Generated Types**: Don't manually edit anything in `frontend/src/__generated__`. Regenerate it using the backend openapi.json.
