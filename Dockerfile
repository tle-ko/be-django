FROM python:3.9-slim

# Set up vitual environment and install requirements
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN apt update && \
    pip install --upgrade pip

# Install dependencies
COPY requirements.txt /requirements.txt

RUN apt install -y gcc libpq-dev postgresql
RUN pip install -r /requirements.txt

# Copy the app
COPY app /app
WORKDIR /app

EXPOSE 8000

# Run the server
HEALTHCHECK --interval=5s CMD [ "./healthcheck.py" ]
ENTRYPOINT ["./entrypoint.sh"]
