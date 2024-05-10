import os
import pytest
import yaml
from subprocess import run

def test_modify_and_use_config():
    # Step 1: Modify the YAML file
    config_path = '../configs/template_config.yaml'
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Updating the configuration as per the requirements
    config['dataset_name'] = 'wikitext'
    config['dataset_subset'] = 'wikitext-2-v1'
    config['use_slurm'] = False
    config['raw_dataset_path'] = '/tmp/data/datasets/wikitext-2-v1'

    new_config_path = '../configs/user_configs/template_config.yaml'
    with open(new_config_path, 'w') as file:
        yaml.safe_dump(config, file)

    # Step 2: Modify the download_data.sh script
    script_path = '../scripts/download_data.sh'  # Correct this path as needed
    with open(script_path, 'r') as file:
        script_content = file.read()

    modified_script_content = script_content.replace('<YOUR_CONFIG_HERE>.yaml', 'template_config.yaml')

    new_script_path = '../scripts/user_scripts/download_data.sh'
    with open(new_script_path, 'w') as file:
        file.write(modified_script_content)

    # Make sure the script is executable
    os.chmod(new_script_path, 0o755)

    # Step 3: Execute the script and verify
    result = run(["./download_data.sh"], cwd="../scripts/user_scripts", check=False)
    assert result.returncode == 0, "Script did not complete successfully"

    # Verify directory and its contents
    assert os.path.exists('/tmp/data/datasets/wikitext-2-v1'), "Dataset directory does not exist"
    assert os.listdir('/tmp/data/datasets/wikitext-2-v1'), "Dataset directory is empty"
