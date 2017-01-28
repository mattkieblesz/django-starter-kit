import json
import os
import shutil
from jinja2 import Environment, FileSystemLoader

default_project_name = 'ProjectName'
default_config_filename = 'config.json'

with open(default_config_filename) as file:
    project_vars = json.load(file)

project_name = project_vars['project_name']
current_project_dir = os.path.dirname(os.path.realpath(__file__))
dst_project_dir = os.path.join(current_project_dir, '..', project_name)

assert os.path.exists(dst_project_dir) is False, 'Project already exists'

shutil.copytree(default_project_name, dst_project_dir)

env = Environment(
    loader=FileSystemLoader(dst_project_dir),
    variable_start_string='<%',
    variable_end_string='%>'
)

# reverse tree so we can rename current root while walking
tree = list(os.walk(dst_project_dir))
tree.reverse()

for root, _, files in tree:

    for file in files:
        filepath = os.path.join(root, file)
        template_path = os.path.relpath(filepath, dst_project_dir)
        template = env.get_template(template_path)
        result = template.render(**project_vars)

        with open(filepath, "w") as f:
            f.write(result)

        dst_file = file.replace(default_project_name, project_name)
        dst_filepath = os.path.join(root, dst_file)
        os.rename(filepath, dst_filepath)

    # now we can rename current root directory
    current_path, current_dir_name = os.path.split(root)
    dst_dir_name = current_dir_name.replace(default_project_name, project_name)
    dst_dirpath = os.path.join(current_path, dst_dir_name)
    os.rename(root, dst_dirpath)
