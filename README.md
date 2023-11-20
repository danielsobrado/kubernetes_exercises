# Kubernetes Validation Tool

This tool provides a set of functions to validate various aspects of a Kubernetes cluster, including pod connectivity, URL accessibility from within and outside the cluster, and user permissions.

## Features

- **Pod Connectivity Check**: Validates if one pod can connect to another within the cluster.
- **Internal URL Accessibility Check**: Validates if a URL is accessible from a specific pod within the cluster.
- **External URL Accessibility Check**: Validates if a URL is accessible from outside the Kubernetes cluster.
- **User Permission Check**: Checks if a user has specific permissions in the Kubernetes cluster.
- **Controller Status Check**: Determines if a specific Kubernetes controller is enabled.
- **API Version Availability Check**: Checks if a specific version of an API is available in the Kubernetes cluster.

## Requirements

- Python 3.x
- `kubectl` installed and configured to communicate with your Kubernetes cluster.
- Python `requests` library for HTTP requests (for external URL checks).

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install the required Python packages:
   
   ```bash
   pip install requests
   ```

3. Clone the repository or download the script files to your local machine.

## Usage

To validate a specific Kubernetes exercise, run the script with the exercise name as an argument. The script will perform all necessary checks and provide you with the results.

Example command:

```bash
python ckad_validate.py exercise_name
```

## Contributing

Contributions to this tool are welcome. Please ensure that any pull requests or issues adhere to the existing coding style and functionality.

