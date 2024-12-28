"""
This setup.py file contains all the metadata information 
related to the Network Security project for phishing data
"""

from setuptools import find_packages,setup

def get_requirements()-> list[str]:
    """
    This functions gets the list of requirements
    """
    req_lst:list[str] = []

    try:
        with open('requirements.txt','r') as file:
            #read the file lines
            lines = file.readlines()

            for line in lines:
                requirement = line.strip()
                if requirement and requirement!='-e .':
                    req_lst.append(requirement)
        
    except FileNotFoundError:
        print('requirement file does not exist')

    return req_lst

setup(
    name='Network security',
    version='0.0.1',
    author = 'Forgetful-coder',
    author_email='aayushaggarwal243@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()

)


        
