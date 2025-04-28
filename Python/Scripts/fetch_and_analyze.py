import requests
import os
import pandas as pd

def fetch_file_from_github(repo_owner, repo_name, file_path, token, output_file):
    """
    Fetch a file from a GitHub repository using the GitHub API.

    :param repo_owner: Owner of the repository
    :param repo_name: Name of the repository
    :param file_path: Path to the file in the repository
    :param token: GitHub personal access token
    :param output_file: Local file path to save the fetched file
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers = {"Authorization": f"token {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        content = response.json().get("content")
        if content:
            with open(output_file, "wb") as f:
                f.write(requests.utils.unquote_to_bytes(content))
            print(f"File saved to {output_file}")
        else:
            print("No content found in the file.")
    else:
        print(f"Failed to fetch file: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Replace these variables with your repository details and file path
    REPO_OWNER = "your-username"
    REPO_NAME = "your-repository"
    FILE_PATH = "path/to/your/file.csv"
    TOKEN = "your-personal-access-token"
    OUTPUT_FILE = "local_file.csv"

    # Fetch the file from GitHub
    fetch_file_from_github(REPO_OWNER, REPO_NAME, FILE_PATH, TOKEN, OUTPUT_FILE)

    # Perform analysis on the fetched file
    if os.path.exists(OUTPUT_FILE):
        df = pd.read_csv(OUTPUT_FILE)
        print("File content:")
        print(df.head())