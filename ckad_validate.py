import subprocess
import sys
import logging
import requests
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_kubectl_available():
    """Check if kubectl is available."""
    try:
        subprocess.run(["kubectl", "version", "--client"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def run_command(command):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {e.stderr}")
        sys.exit(1)

def validate_resource(resource_type, resource_name):
    """Validate if a specific Kubernetes resource exists."""
    logging.info(f"Validating {resource_type} {resource_name}...")
    run_command(f"kubectl get {resource_type} {resource_name}")

def validate_pod_connectivity(pod_name, target_pod_name, target_port):
    """Validate if one pod can connect to another on a specific port."""
    logging.info(f"Checking connectivity from {pod_name} to {target_pod_name} on port {target_port}...")

    # Define the command to check connectivity using netcat (nc)
    command = f"kubectl exec {pod_name} -- nc -zv {target_pod_name} {target_port}"

    try:
        output = run_command(command)
        if "succeeded" in output:
            logging.info(f"Connectivity from {pod_name} to {target_pod_name} on port {target_port} is successful.")
        else:
            logging.error(f"Connectivity test failed from {pod_name} to {target_pod_name} on port {target_port}.")
            logging.error(f"Command output: {output}")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to execute connectivity test: {e}")
        sys.exit(1)

def validate_url_accessibility(pod_name, url):
    """Validate if a URL is accessible from a specific pod."""
    logging.info(f"Checking URL accessibility from {pod_name} to {url}...")

    command = f"kubectl exec {pod_name} -- curl -s -o /dev/null -w '%{{http_code}}' {url}"

    try:
        http_status = run_command(command)
        if http_status == "200":
            logging.info(f"URL {url} is accessible from pod {pod_name}.")
        else:
            logging.error(f"URL {url} is not accessible from pod {pod_name}. HTTP status code: {http_status}")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to execute URL accessibility test: {e}")
        sys.exit(1)

def validate_external_url_accessibility(url):
    """Validate if a URL is accessible from outside the Kubernetes cluster."""
    logging.info(f"Checking external URL accessibility for {url}...")

    try:
        response = requests.get(url)
        if response.status_code == 200:
            logging.info(f"URL {url} is externally accessible.")
        else:
            logging.error(f"URL {url} is not externally accessible. HTTP status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        logging.error(f"Failed to execute external URL accessibility test: {e}")
        return False
    return True

def check_user_permission(verb, resource, namespace="default", username=None):
    """Check if a specified user has permissions to perform a given action on a resource."""
    user_info = f"user '{username}'" if username else "the current user"
    logging.info(f"Checking if {user_info} has permission to '{verb}' on '{resource}' in '{namespace}' namespace...")

    command = f"kubectl auth can-i {verb} {resource} --namespace {namespace}"
    if username:
        command += f" --as {username}"

    try:
        output = run_command(command)
        if output.strip() == "yes":
            logging.info(f"{user_info} has permission to '{verb}' on '{resource}' in '{namespace}' namespace.")
            return True
        else:
            logging.warning(f"{user_info} does not have permission to '{verb}' on '{resource}' in '{namespace}' namespace.")
            return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to execute permission check: {e}")
        sys.exit(1)

def check_controller_enabled(controller_name):
    """Check if a specific Kubernetes controller is enabled."""
    logging.info(f"Checking if the controller '{controller_name}' is enabled...")

    try:
        # This command might vary depending on your cluster setup and the controller
        output = run_command("kubectl get deployment -n kube-system")
        if controller_name in output:
            logging.info(f"Controller '{controller_name}' is enabled.")
            return True
        else:
            logging.warning(f"Controller '{controller_name}' is not enabled or not found.")
            return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to check controller status: {e}")
        sys.exit(1)

def check_api_version_available(api_version):
    """Check if a specific version of an API is available in the Kubernetes cluster."""
    logging.info(f"Checking if API version '{api_version}' is available...")

    try:
        output = run_command("kubectl api-versions")
        if api_version in output.splitlines():
            logging.info(f"API version '{api_version}' is available.")
            return True
        else:
            logging.warning(f"API version '{api_version}' is not available.")
            return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to check API version availability: {e}")
        sys.exit(1)

import subprocess
import yaml
import logging

def get_and_verify_pod_attributes(pod_name, namespace="default", attributes_to_verify=None):
    """Get a pod's YAML definition and verify specified attributes."""
    logging.info(f"Retrieving YAML for pod {pod_name} in namespace {namespace}...")

    command = f"kubectl get po {pod_name} -n {namespace} -o yaml"
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        pod_yaml = result.stdout

        pod_data = yaml.safe_load(pod_yaml)

        if attributes_to_verify:
            for attribute, expected_value in attributes_to_verify.items():
                actual_value = get_nested_attribute(pod_data, attribute.split('.'))
                if actual_value != expected_value:
                    logging.error(f"Attribute '{attribute}' has value '{actual_value}', expected '{expected_value}'")
                    return False
                else:
                    logging.info(f"Attribute '{attribute}' correctly has value '{expected_value}'")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to retrieve YAML: {e}")
        return False
    except Exception as e:
        logging.error(f"Error processing YAML: {e}")
        return False

def get_nested_attribute(data, attribute_path):
    """Recursively fetch a nested attribute."""
    for key in attribute_path:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    return data

def execute_validation(exercise_number):
    """Execute validation based on exercise number using a dynamic approach."""
    try:
        function_name = f"validate_exercise_{exercise_number}"
        validation_function = getattr(sys.modules[__name__], function_name)
        validation_function()
    except AttributeError:
        logging.error(f"No validation function found for exercise number {exercise_number}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred during validation: {e}")
        sys.exit(1)

def main():
    if not is_kubectl_available():
        logging.error("kubectl is not available. Please install it and ensure it's in your PATH.")
        sys.exit(1)

    try:
        exercise_number = int(input("Enter the exercise number to validate: "))
        execute_validation(exercise_number)
    except ValueError:
        logging.error("Please enter a valid number.")
        sys.exit(1)

if __name__ == "__main__":
    main()
