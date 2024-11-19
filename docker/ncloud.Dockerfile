FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY ../requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY ../app /app/

# Entry script to wait for PostgreSQL to be ready
COPY ./scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the server
HEALTHCHECK --interval=5s CMD [ "./healthcheck.py" ]
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uwsgi", "--http", ":8000", "--home", "/usr/local/", "--chdir", "/app/", "-w", "config.wsgi"]