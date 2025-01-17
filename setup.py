from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path:str)-> List[str]:

    HYPEN_DOT = '-e .'

    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]

        if HYPEN_DOT in requirements:
            requirements.remove(HYPEN_DOT)
    return requirements


setup(
    name="studentMarksPredictor",                 # Package name
    version="0.0.1",                  # Version
    author="Sumit Kumar",               # Author name
    description="Student price predictor project",
    packages=find_packages(),         # Automatically finds all Python packages
    install_requires= get_requirements('requirements.txt')
)
