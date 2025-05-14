# Load Balancer
## Introduction

This project implements a load balancer in Python using Uvicorn, a high-performance ASGI server. The load balancer distributes incoming HTTP requests across multiple backend servers to improve the responsiveness, reliability, and scalability of applications. It has been tested to demonstrate significant performance improvements over a single server setup.

## Installation and Setup

To set up the project, follow these steps:

1. **Clone the repository** from [GitHub](https://github.com/MohabASHRAF-byte/load-balancer) and navigate to the root directory.

2. **Install dependencies**. If a `requirements.txt` file is present, run:

   ```bash
   pip install -r requirements.txt
   ```


3. **Run the backend servers**. Start multiple backend servers on different ports using:

   ```bash
   python TestBackend/server.py <port-number>
   ```

   For example, to start three servers:

   ```bash
   python TestBackend/server.py 5001
   python TestBackend/server.py 5002
   python TestBackend/server.py 5003
   ```

4. **Run the load balancer**. Start the load balancer by executing:

   ```bash
   python main.py
   ```

   This launches the load balancer on port 5000, ready to distribute incoming requests.

## Features

The load balancer includes the following features:

- **Load Balancing Algorithms**: The project supports multiple algorithms to distribute requests across backend servers :
  - round-robin
  - least-connections
  - random-choice
- **Server Management**: Currently, backend servers must be started manually. API-based server management is a planned feature but not yet implemented.
- **High-Performance Server**: Utilizes Uvicorn for efficient handling of asynchronous HTTP requests.

## Usage

To use the load balancer:

1. **Start backend servers** on different ports, for example:

   ```bash
   python TestBackend/server.py 5001
   python TestBackend/server.py 5002
   python TestBackend/server.py 5003
   ```

   These servers will handle the requests distributed by the load balancer. The server URLs are:
   - http://127.0.0.1:5001/
   - http://127.0.0.1:5002/
   - http://127.0.0.1:5003/

2. **Start the load balancer**:

   ```bash
   python main.py
   ```

3. **Send requests** to the load balancer at http://127.0.0.1:5000/. The load balancer will distribute these requests across the running backend servers.

## Performance Comparison

The project was tested using Apache Bench (ab) with the command:

```bash
ab -n 5000 -c 100 http://127.0.0.1:500x/
```

Tests compared a single server (port 5003) against the load balancer (port 5000), each handling 5000 requests with 100 concurrent connections. Below are the results.

### Single Server (port 5003)

| Metric                     | Value          |
|----------------------------|----------------|
| Time taken for tests (s)   | 63.172         |
| Requests per second        | 79.15          |
| Time per request (ms)      | 1263.441       |
| Transfer rate (Kbytes/sec) | 12.29          |

### Load Balancer (port 5000)

| Metric                     | Value          |
|----------------------------|----------------|
| Time taken for tests (s)   | 28.105         |
| Requests per second        | 177.91         |
| Time per request (ms)      | 562.095        |
| Transfer rate (Kbytes/sec) | 37.01          |

### Performance Improvements

The load balancer demonstrates significant improvements over a single server:

| Metric                     | Single Server | Load Balancer | Change (%)            |
|----------------------------|---------------|---------------|-----------------------|
| Time taken for tests (s)   | 63.172        | 28.105        | -55.51% (decrease)    |
| Requests per second        | 79.15         | 177.91        | +124.79% (increase)   |
| Time per request (ms)      | 1263.441      | 562.095       | -55.51% (decrease)    |
| Transfer rate (Kbytes/sec) | 12.29         | 37.01         | +201.38% (increase)   |

- **Requests per second**: Increased by approximately 124.79%, meaning the load balancer handles over twice as many requests per second.
- **Time per request**: Decreased by approximately 55.51%, indicating faster response times.
- **Transfer rate**: Increased by approximately 201.38%, showing a substantial boost in data transfer efficiency.

## Conclusion

This load balancer project effectively distributes HTTP requests across multiple backend servers, significantly enhancing application performance. Compared to a single server, the load balancer reduces response times, increases request throughput, and improves data transfer rates, as evidenced by Apache Bench testing. Built with Python and Uvicorn, it provides a practical solution for improving application scalability and reliability. Future enhancements may include API-based server management for more dynamic control.
