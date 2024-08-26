# GitHub Repository Manager

This project automates the process of creating, initializing, and managing GitHub repositories using Terraform. The script provided allows you to create a new repository on GitHub, set up a local Git repository, and push the initial commit. Additionally, you have the option to destroy the Terraform-managed resources when no longer needed.

## Description

This tool simplifies the creation of GitHub repositories by automating repetitive tasks. It uses Terraform to interact with the GitHub API, enabling the creation of repositories based on customizable templates. Once a repository is created, the tool initializes a local Git repository, sets the main branch, and prepares it for development.

## Prerequisites

Before you can use this tool, ensure you have the following installed on your system:

* **Python 3.x**: Required to run the script.

* **Terraform**: Install Terraform to manage infrastructure as code.

  :eyes: [Install Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)

* **Git**: For initializing and managing the local repository.

  :eyes: [Reviewing your SSH keys](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/reviewing-your-ssh-keys)

* **GitHub Personal Access Token**: You need a GitHub token with the necessary permissions to create repositories.

  :eyes: [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

  

## Setup

### Creating a Virtual Environment

It's recommended to use a Python virtual environment to manage dependencies. Follow these steps to set up the environment:

#### **Navigate to the project directory:**

```shell
cd manage-repo
```

#### **Create a virtual environment:**

```shell
python3 -m venv venv
```

#### **Activate the virtual environment:**

```shell
source venv/bin/activate
```

#### **Install required Python packages:**

If `requirements.txt` does not exist, create it with the following content:

```shell
cat > requirements.txt <<EOF
jinja2
pyyaml
EOF
```



After activating the virtual environment, install the required packages using pip:

```shell
pip install -r requirements.txt
```

check

```shell
pip freezze
```



## Configuring the Project

### **Create or edit the configuration file:**

The `config.yaml` file at the root of the project should define the base directory where local repositories will be created and the repository name:

```yaml
cat > config.yaml <<EOF
local_repo_base_dir: "/path/to/local/repos"
repo_name: "your-repo-name"
EOF
```

* Replace "/path/to/local/repos" with the actual path where you want your repositories to be stored locally.
* ​    Replace "your-repo-name" with the desired repository name.

### Customize the repository name:

​    Alternatively, you can directly edit the repo_name value in the config.yaml file or pass it as a command-line argument when running the script.



## Usage

### **Clone the repository**:

```shell
git clone https://github.com/yourusername/manage-repo.git
cd manage-repo
```

### Activate the virtual environment:

Follow the steps mentioned above to activate the virtual environment.

### Configure your environment:

Set your GitHub token as an environment variable:

```shell
export TF_VAR_github_token=your_github_token
```



### Run the script:

**:warning: <u>Take time to fully understand what this script does before running it</u>**

```shell
python repo_manager.py
```

This will:

* Create a new GitHub repository based on the repo_name specified in `config.yaml`.
* Initialize a local Git repository.
* Create the main branch and push the initial commit.

### Destroy the Terraform resources (optional):

If you wish to remove the GitHub repository and associated resources managed by Terraform, run:

```shell
python repo_manager.py --destroy
```



## :facepunch: Contribution

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. **Fork the repository** to your own GitHub account.
2. **Clone your fork** locally:

```shell
git clone https://github.com/yourusername/github-repository-manager.git
cd manage-repo
```

**Create a new branch** for your feature or bug fix:

```shell
git checkout -b my-new-feature
```

**Make your changes** and commit them with a clear message:

```shell
git commit -m "Add new feature"
```

**Push your branch** to your fork:

1. ```shell
   git push origin my-new-feature
   ```

2. **Open a Pull Request** on the original repository and describe your changes.

By following these steps, you can help improve the project for everyone!

