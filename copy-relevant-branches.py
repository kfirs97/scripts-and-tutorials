import subprocess
from datetime import datetime
import os

def filter_date(date, min_date):
    date = datetime.strptime(date, '%Y-%m-%d')
    min_date = datetime.strptime(min_date, '%Y-%m-%d')
    return date >= min_date

def filter_branches(branches, min_date):
    return list(filter(lambda branch: filter_date(branch.split(' ')[1], min_date), branches))

def extract_branch_names(branches):
    return [branch.split(' ')[0].split('/')[1] for branch in branches]

def list_remote_branches_by_creation_date(repo_path):
    try:
        # Fetch the latest information from the remote 'origin'
        subprocess.check_call(['git', '-C', repo_path, 'fetch', 'origin'])

        # List remote branches and sort them by the earliest commit date
        result = subprocess.check_output(
            ['git', '-C', repo_path, 'for-each-ref', '--sort=committerdate', 'refs/remotes/origin/', '--format=%(refname:short) %(committerdate:iso8601)']
        ).decode('utf-8')

        branch_lines = result.strip().split('\n')
        for line in branch_lines:
            print(line)

        return branch_lines

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def copy_branches(old_repo_name, old_repo_url, new_repo_path, new_repo_url, branches):
    try:
        if not os.path.exists(new_repo_path):
            os.makedirs(new_repo_path)

        # Create a new empty Git repository - only if the repo is not initialized yet
        try:
            subprocess.check_call(['git', 'init', new_repo_path])
        except Exception as e:
            print(f'{e}')

        # Change the working directory to the new repository
        os.chdir(new_repo_path)

        # Add a remote for the old repository
        try:
            subprocess.check_call(['git', 'remote', 'add', old_repo_name, old_repo_url])
        except Exception as e:
            # if command fails it's probably because the remote origin already exists
            print(str(e))

        subprocess.check_call(['git', 'remote', 'add', 'origin', new_repo_url])

        # Fetch all branches from the old repository
        subprocess.check_call(['git', 'fetch', old_repo_name])

        for branch_name in branches:
            # Create and checkout the new branch
            subprocess.check_call(['git', 'checkout', '-b', branch_name, f'{old_repo_name}/{branch_name}'])

            # Push the branch to the new repository
            subprocess.check_call(['git', 'push', 'origin', branch_name])

            print(f"Branch '{branch_name}' copied and pushed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    old_repo_path = ""
    new_repo_path = ""
    new_repo_url = ""
    min_date = ""
    branches = list_remote_branches_by_creation_date(old_repo_path)
    filtered_branches = filter_branches(branches, min_date)
    branches_names = extract_branch_names(filtered_branches)
    
    # in case HEAD is part of the branches name
    try:
        branches_names.remove('HEAD')
    except:
        pass
    
    print(branches_names)
    copy_branches('Library.Components.ROS', 'git@github.com:cogniteam/Library.Components.ROS.git', new_repo_path, new_repo_url, branches_names)

if __name__ == "__main__":
    main()