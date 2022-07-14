import os
import shutil
from github import Github 


def update_scripts(access_token, username, ops_repo_name, path):


    # Erasing contents of folder

    folder = f'{path}/user_script_files'
    for filename in os.listdir(folder):
        if filename == ".gitignore" or filename == "__init__.py":
            continue
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


    # Writing file contents from GitHub

    if access_token == None:
        g = Github()
    else:
        g = Github(access_token)

    repo = g.get_repo(f"{username}/{ops_repo_name}")
    contents = repo.get_contents("")
    
    user_scripts_list = []
    
    while len(contents) > 0:
        file_content = contents.pop(0)
        user_scripts_list.append(os.path.splitext(file_content.name)[0])
        ops_file = open(f"{path}/user_script_files/{os.path.splitext(file_content.name)[0]}.py",'w')
        ops_file.write(file_content.decoded_content.decode('utf-8'))
        ops_file.close()
    
    return user_scripts_list



