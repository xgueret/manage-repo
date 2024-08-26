import os
import subprocess
import shutil
import yaml
import re
from jinja2 import Environment, FileSystemLoader

# Load configuration from config.yaml
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

# Extract variables from configuration
LOCAL_REPO_BASE_DIR = config["LOCAL_REPO_BASE_DIR"]
REPO_NAME = config["REPO_NAME"]
REPO_DESCRIPTION = config["REPO_DESCRIPTION"]

# Paths
repo_path = os.path.join(LOCAL_REPO_BASE_DIR, REPO_NAME)
terraform_path = os.path.join(repo_path, "terraform")

def is_initialized(terraform_path):
    """Checks if Terraform has already been initialized by looking for the .terraform directory."""
    return os.path.exists(os.path.join(terraform_path, ".terraform"))

def create_local_repo_directory(repo_path):
    """Creates the local repository directory structure."""
    if not os.path.exists(terraform_path):
        os.makedirs(terraform_path)
        print(f"Created directory {terraform_path}")

    # Initialize Jinja2 environment
    env = Environment(loader=FileSystemLoader('models/terraform'))

    # Copy the main.tf file from models to the terraform directory
    shutil.copy('models/terraform/main.tf.j2', os.path.join(terraform_path, 'main.tf'))

    # Render the variables.tf template
    variables_template = env.get_template('variables.tf.j2')
    variables_tf_content = variables_template.render(repo_name=REPO_NAME, repo_description=REPO_DESCRIPTION)
    
    # Write the rendered content to the terraform directory
    with open(os.path.join(terraform_path, "variables.tf"), "w") as variables_tf_file:
        variables_tf_file.write(variables_tf_content)

    print(f"Copied Terraform main.tf and rendered variables.tf to {terraform_path}")

def initialize_git_repo(repo_path, repo_url):
    """Initializes a Git repository in the given path and adds the remote origin."""
    os.chdir(repo_path)
    
    if not os.path.exists(os.path.join(repo_path, ".git")):
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "branch", "-M", "main"], check=True)
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
        print(f"Initialized Git repository and added remote origin {repo_url}")
    else:
        print("Git repository already initialized.")

def run_terraform_commands(terraform_path):
    """Runs the necessary Terraform commands to create the GitHub repository."""
    # Navigate to the Terraform directory
    os.chdir(terraform_path)
    print(f"Changed directory to {terraform_path}")

    # Re-initialize Terraform if necessary
    if not is_initialized(terraform_path) or not os.path.exists(os.path.join(terraform_path, "terraform.tfstate")):
        print("Running terraform init...")
        subprocess.run(["terraform", "init"], check=True)
    else:
        print("Terraform is already initialized, skipping terraform init.")
    
    # Run terraform plan and handle possible errors
    try:
        print("Running terraform plan...")
        plan_proc = subprocess.run(["terraform", "plan"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        substring = "no changes are needed."
        if substring in plan_proc.stdout:
            print("No changes detected. Your infrastructure matches the configuration.")
            return subprocess.check_output(["terraform", "output", "repository_url"], text=True).strip()
        elif plan_proc.returncode == 2:
            print("Changes detected. Proceeding with terraform apply.")
        else:
            print("Terraform plan returned an error. Details:")
            print(plan_proc.stdout)
            print(plan_proc.stderr)
            plan_proc.check_returncode()  # Raises an error if return code is 1

        # Run Terraform apply without confirmation
        print("Running terraform apply...")
        apply_proc = subprocess.run(["terraform", "apply", "-auto-approve"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Extract the repository URL from the output
        repo_url = None
        for line in apply_proc.stdout.splitlines():
            if "repository_url =" in line:
                repo_url = line.split(" = ")[1].strip()
                break

        return repo_url
    
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during terraform execution: {e}")
        print(f"Output: {e.output}")
        print(f"Stderr: {e.stderr}")
        return None

def main(destroy=False):
    """Main function to create or destroy a GitHub repository."""
    create_local_repo_directory(repo_path)
    
    if destroy:
        print("Running terraform destroy...")
        os.chdir(terraform_path)
        subprocess.run(["terraform", "destroy", "-auto-approve"], check=True)
        print("Repository destroyed.")
        return
    
    repo_url = run_terraform_commands(terraform_path)
    
    if repo_url:
        print(f"Repository URL: {repo_url}")
        initialize_git_repo(repo_path, repo_url)
    else:
        print("No changes were made to the repository or an error occurred.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Manage GitHub repositories with Terraform.")
    parser.add_argument("--destroy", action="store_true", help="Destroy the GitHub repository.")
    args = parser.parse_args()

    main(destroy=args.destroy)
