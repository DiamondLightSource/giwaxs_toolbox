Installation giwaxs_toolbox locally
=========================================


#. Check your version of python

    You will need python 3.11 or later. You can check your version of python by
    typing into a terminal:

    .. code-block:: bash 

        $ python3 --version


#. Create a virtual environment

    It is recommended that you install into a “virtual environment” so this
    installation will not interfere with any existing Python software:

    .. code-block:: bash 

        $ python3 -m venv /path/to/venv
        $ source /path/to/venv/bin/activate


#. Clone from GitHub

    Make sure you have git installed on your machine (https://github.com/git-guides/install-git)
    Move to the location you want to download the files to, and then clone the repository. 
    
    .. code-block:: bash 

        $ cd path/to/folder/
        $ git clone https://github.com/DiamondLightSource/giwaxs_toolbox.git 


#. Install from cloned repository
 

    .. code-block:: bash 

        $ pip install giwaxs_toolbox/
