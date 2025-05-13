import subprocess
import sys
import signal
import time
import os


def start_servers(num_instances, start_port=5001):
    processes = []
    for i in range(num_instances):
        port = start_port + i
        env = os.environ.copy()
        env["APP_PORT"] = str(port)
        try:
            process = subprocess.Popen(
                [sys.executable, "TestBackend/server.py", str(port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )
            processes.append(process)
            print(f"Started server on port {port} with PID {process.pid}")
            # Check if process started successfully
            time.sleep(1)  # Give it a moment to start
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                print(f"Port {port} failed to start. Stdout: {stdout}", file=sys.stderr)
                print(f"Port {port} stderr: {stderr}", file=sys.stderr)
                processes.remove(process)
        except FileNotFoundError:
            print(f"Error: 'server.py' not found in current directory!", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error starting server on port {port}: {e}", file=sys.stderr)
    return processes


def terminate_servers(processes):
    for process in processes:
        try:
            process.terminate()
            process.wait(timeout=5)
            print(f"Terminated server with PID {process.pid}")
        except subprocess.TimeoutExpired:
            process.kill()
            print(f"Forced termination of server with PID {process.pid}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python wrapper.py <number_of_instances>", file=sys.stderr)
        sys.exit(1)

    try:
        num_instances = int(sys.argv[1])
        if num_instances <= 0:
            raise ValueError("Number of instances must be positive")
    except ValueError:
        print("Error: <number_of_instances> must be a positive integer", file=sys.stderr)
        sys.exit(1)

    processes = start_servers(num_instances)


    def signal_handler(sig, frame):
        print("Terminating all servers...")
        terminate_servers(processes)
        sys.exit(0)


    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        while processes:
            for process in processes[:]:
                if process.poll() is not None:
                    stdout, stderr = process.communicate()
                    print(f"Server with PID {process.pid} exited. Stdout: {stdout}", file=sys.stderr)
                    print(f"Server with PID {process.pid} stderr: {stderr}", file=sys.stderr)
                    processes.remove(process)
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)