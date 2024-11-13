#!/usr/bin/env python
import requests


def healthcheck():
    try:
        response = requests.get(f"http://localhost:8000/healthcheck/")
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


if __name__ == "__main__":
    if healthcheck():
        exit(0)
    else:
        exit(1)
