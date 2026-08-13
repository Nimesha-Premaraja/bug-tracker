# Local Docker Compose ELK Integration Plan

## Scope

Integrate a local-only ELK observability stack into Docker Compose:

- Elasticsearch for log storage
- Kibana for search and visualization
- Filebeat to collect Docker container stdout/stderr
- Structured JSON Flask application logs
- Gunicorn access and error logs

This work excludes Helm/Kubernetes changes. Filebeat must not ingest user-uploaded files in `app/uploads`, including uploaded `.log` attachments.

## Implementation Plan

1. **Add structured application logging**
   - Add a reusable logging configuration module, or configure logging within `app/__init__.py`.
   - Write JSON logs to stdout with timestamp, severity, logger name, message, module/function, and exception information.
   - Configure Flask and Werkzeug loggers to use this format.
   - Retain and improve existing database initialization, user-loader, and health-check error events.
   - Make the log level configurable through an environment variable, defaulting to `INFO`.

2. **Enable Gunicorn access and error logging**
   - Update the image startup command or add a dedicated Gunicorn configuration file.
   - Send Gunicorn access logs to stdout and error logs to stderr.
   - Remove the Compose override that starts Flask's development server so the local container uses Gunicorn consistently.
   - Ensure application log records remain structured JSON when emitted through the production server.

3. **Extend `docker-compose.yml` with local ELK services**
   - Add a single-node Elasticsearch service with Elastic security disabled for local-only use.
   - Add a Kibana service connected to Elasticsearch and expose its local UI port.
   - Add a Filebeat service to harvest Docker container logs.
   - Use health checks and dependency conditions so Kibana and Filebeat start after Elasticsearch is ready.
   - Bind Elasticsearch and Kibana to localhost where practical.
   - Use a named volume to retain Elasticsearch data and add suitable local resource settings.
   - Mount only the Docker runtime log path/socket and configuration paths Filebeat requires.

4. **Create Filebeat configuration**
   - Add `filebeat/filebeat.yml`.
   - Use Docker autodiscovery or Docker container log inputs and restrict collection to the Compose `web` service.
   - Decode JSON application logs and preserve structured fields.
   - Enrich records with Docker/Compose container metadata and ECS-compatible fields.
   - Send events directly to Elasticsearch under a dedicated `bug-tracker-logs-*` index or data-stream pattern.
   - Configure Kibana setup support for the corresponding data view where supported.
   - Explicitly avoid all application upload paths and unrelated service logs.

5. **Update project documentation**
   - Document Docker Desktop memory prerequisites and the local-only, unauthenticated security posture.
   - Provide commands to start/rebuild the full stack, inspect service status, and stop or remove volumes.
   - Document Elasticsearch and Kibana URLs.
   - Explain how to generate HTTP/application/error events and create or select the Kibana data view.
   - Include validation commands for Filebeat, Elasticsearch, and indexed log events.

6. **Validate locally**
   - Start the complete Compose stack from a clean state.
   - Verify Elasticsearch health, Kibana availability, and Filebeat output/registry health.
   - Generate regular requests and a safe handled application error or health-check event.
   - Confirm Gunicorn access/error logs and JSON Flask application events appear in Elasticsearch/Kibana as searchable fields.
   - Confirm Docker metadata is attached and uploaded `.log` attachments are not indexed.
   - Run repository checks: `ruff check .` and `python -I -m compileall -q app config.py wsgi.py`.

## Expected Files

- `app/__init__.py` and/or a new application logging module
- `Dockerfile` and/or a new Gunicorn configuration file
- `docker-compose.yml`
- `filebeat/filebeat.yml` (new)
- `README.md`
