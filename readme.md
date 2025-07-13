## Running the Project with Docker

This project includes a Docker setup for easy deployment and development. Below are the instructions and details specific to this project:

### Requirements & Versions
- **Python Version:** 3.9 (as specified in the Dockerfile: `python:3.9-slim-buster`)
- **Dependencies:** All Python dependencies are installed from `requirements.txt` inside a virtual environment during the build process.

### Environment Variables
- The Docker setup supports environment variables via a `.env` file. If your project requires environment variables, ensure you have a `.env` file in the project root. Uncomment the `env_file` line in `docker-compose.yml` if needed.

### Build and Run Instructions
1. **Build and start the application:**
   ```sh
   docker compose up --build
   ```
   This will build the image and start the `python-app` service.

2. **Accessing the application:**
   - The application will be available at [http://localhost:8000](http://localhost:8000) by default.

### Ports
- **8000:** Exposed by the container and mapped to the host (as per `docker-compose.yml` and Dockerfile). The app runs with Uvicorn on this port.

### Special Configuration
- The application runs as a non-root user (`appuser`) for improved security.
- Uploaded files are stored in `/app/uploaded_files` inside the container.
- No external services (databases, cache, etc.) are configured by default. If you add such services, update `docker-compose.yml` accordingly.

### Notes
- If you need to persist uploaded files or other data, consider adding Docker volumes.
- For custom networks or additional services, uncomment and configure the relevant sections in `docker-compose.yml`.

---

*This section was updated to reflect the current Docker-based setup for this project.*