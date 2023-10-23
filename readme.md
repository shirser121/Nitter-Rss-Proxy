# Nitter-Rss-Proxy

[![Build Status](https://img.shields.io/travis/shirser121/repo.svg)](https://travis-ci.org/user/repo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

`Nitter-Rss-Proxy` is a proxy server designed to integrate seamlessly with Nitter's RSS feeds. It offers optimal performance and reliability by employing FastAPI and Redis.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Code Structure](#api-endpoints)
- [Dependencies](#dependencies)
- [Credits](#-credits)
- [Contribution](#How-to-Contribute)
- [License](#-license)

---

## Features

- **FastAPI Integration**: Builds a robust web server using FastAPI.
- **Redis Integration**: Utilizes Redis for efficient caching and data management.
- **Docker Support**: Includes Docker configurations for streamlined deployment.

---

## Prerequisites

- Docker (Version: xx.xx)
- Redis (Version: xx.xx)

---

## Installation & Setup

### Using Docker

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/Nitter-Rss-Proxy.git
    ```

2. **Build the Docker Image**

    ```bash
    docker build -t nitter-rss-proxy:latest .
    ```

3. **Deploy Using Docker-Compose**

    ```bash
    docker-compose up -d
    ```

## 🌍 Environment Variables

The project uses environment variables for configuration. Below is a list of environment variables used by the project along with their default values.

| Variable                        | Description                                      | Default Value                  |
| ------------------------------- | ------------------------------------------------ | ------------------------------ |
| `BASE_URL`                      | The base URL for the status API.                 | `https://status.d420.de/api/v1/instances` |
| `REDIS_HOST`                    | The hostname of your Redis instance.             | `localhost`                    |
| `REDIS_PORT`                    | The port number on which Redis is running.       | `6379`                         |
| `REDIS_CACHE_DURATION_SECONDS`  | Cache duration for Redis in seconds.             | `120` (2 minutes)              |
| `HOSTS_CACHE_DURATION_SECONDS`  | Cache duration for hosts in seconds.             | `86400` (24 hours)             |

To override any of these values, you can set environment variables in your shell before running the application, or you can use a `.env` file.

Example `.env` file:

```env
BASE_URL=https://new_base_url/api/v1/instances
REDIS_HOST=new_redis_host
REDIS_PORT=6380
REDIS_CACHE_DURATION_SECONDS=300
HOSTS_CACHE_DURATION_SECONDS=7200
```

---

## Usage

Access the proxy server at `http://localhost:3010/`. The main endpoint will greet you with a welcome message.

---

## API Endpoints

The application provides a set of RESTful API endpoints to interact with the Nitter RSS proxy service.

### General

#### GET `/`

- **Description**: Returns a welcome message.
- **Response Payload**: JSON object containing a welcome message.

### RSS Feed Proxy

#### GET `api/v1/rss/{username}`

- **Description**: Proxies to a healthy RSS host to retrieve the RSS feed for the given Twitter username.
  
- **Parameters**:
  - `username`: The Twitter username (required).
  - `force_update`: Optional query parameter to force an update from the actual RSS source, bypassing cache.
  
- **Response Payload**: RSS feed in XML format.

**HTTP Status Codes**:

- `200 OK`: The request was successful.
- `404 Not Found`: The RSS feed or username was not found.

---

## Dependencies

Install the project dependencies using the provided `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## 🌟 Credits

We owe a debt of gratitude to some remarkable projects and communities:

- **[Nitter](https://github.com/zedeus/nitter)**: Kudos to Nitter for pioneering a privacy-centric Twitter front-end. Your work has been an inspiration.
- **[nitter-status](https://github.com/0xpr03/nitter-status)**: Special acknowledgment to nitter-status for the option get all the nitter instances status.
- **[twiiit](https://github.com/chr15m/twiiit.com)**: Thanks to twiiit for their work on a similar project.

## 🤝 How to Contribute

We welcome contributions from the open-source community. Here's how you can help:

1. **Fork the Repository**: Fork the main repository and clone it to your local machine.
2. **Create a New Branch**: Create a new branch for your fixes or new features.
3. **Push Your Changes**: Commit your changes and push them to your forked repository.
4. **Submit a Pull Request**: Open a pull request to propose your changes to the main project.

For any questions, suggestions, or discussions, feel free to open an issue. We strive for a welcoming and open community.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
