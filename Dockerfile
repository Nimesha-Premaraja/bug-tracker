# -------------------------
# Builder Stage
# -------------------------
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir \
    --prefix=/install \
    -r requirements.txt

# -------------------------
# Runtime Stage
# -------------------------
FROM python:3.11-slim

WORKDIR /app
RUN useradd --create-home --uid 1000 bugapp
COPY --from=builder /install /usr/local
COPY . .

RUN mkdir -p app/uploads \
    && chown -R bugapp:bugapp /app

USER bugapp
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "wsgi:app"]