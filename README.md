# Twitch WAP Test

This project automates a search on Twitch's mobile web version using Selenium and pytest. The automation script opens the mobile site, performs a search, handles pop-ups, scrolls through the search results, selects a streamer, and takes a screenshot.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Setting Up the Python Environment](#setting-up-the-python-environment)
- [Running Tests](#running-tests)
- [GIFT Test running locally](#GIFT-Test-running-locally) 


## Features

- Automated browser testing using Selenium.
- Dockerized setup for easy environment management.
- Mobile emulation support for testing mobile web applications.
- Capability to record video of the tests for later review.
- Detailed HTML reports of test results.


## Prerequisites

- **Python 3.x**: Ensure Python is installed on your machine. You can download it from [Python.org](https://www.python.org/downloads/).
- **Docker**: Install Docker Desktop compatible with your version of Chrome. You can download it from [Docker Desktop](https://www.docker.com/products/docker-desktop/). Make sure it’s accessible in your system's PATH.


## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Crack525/dockerized-selenium.git
   cd dockerized-selenium

2. **Build the Docker image:**
    ```bash
    docker build -t twitch-selenium-tests .


## Setting Up the Python Environment

If you want to run the tests outside of Docker (optional), you can set up a Python virtual environment:

1. **Create a virtual environment:**
    ```bash
    python -m venv venv

2. **Activate the virtual environment:**

- **On Windows:**
    ```bash
    venv\Scripts\activate

- **On Mac/Linux:**
    ```bash
    source venv/bin/activate

3. - **Install the required Python dependencies::**
    ```bash
    pip install -r requirements.txt

## Running Tests

To run the tests in Docker, execute the following command, the command below will run the tests in a container and generate reports in the specified directories.:

    ```bash
    docker run -it --shm-size=4g --rm \
        -v $(pwd)/screenshots:/app/screenshots \
        -v $(pwd)/reports:/app/reports \
        twitch-selenium-tests


## GIFT Test running locally

![Animation](https://github.com/Crack525/dockerized-selenium/blob/main/screen_recording.gif)
