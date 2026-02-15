import yaml
import sys
from Recommendation_System_Books.exception.exception_handler import AppException    

def read_yaml_file(file_path):
    """
    Read and parse a YAML file.
    
    Args:
        file_path (str): Path to the YAML file.
    
    Returns:
        dict: Parsed YAML content as a dictionary.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If the YAML parsing fails.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        return data
    except Exception as e:
        raise AppException(f"Error reading YAML file: {file_path} - {e}")