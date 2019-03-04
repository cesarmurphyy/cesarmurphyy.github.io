# PACE 2019 S1 - EY Data and Analytics

## Overview

The goal of this project is to synchronise the movement of sticky notes on a physical project management board to a virtualised project management solution. We would like to be able to move a sticky note through a swim lane on the physical board and have the corresponding cards in a virtual tool update with minimal human intervention.

The nature of the project is heavily focused on Computer Vision. [OpenCV](https://opencv.org/) is a popular and open source tool for these types of tasks.

Since OpenCV is a low-level framework, considerations need to be made about portability. To address this, we will be using [Docker](https://www.docker.com/) as primary tool for both development and deployment of your solution. The Dockerfile supplied will pull from an existing docker image providing both python 3.7 and OpenCV.

If you don't have experience with Docker already take some time to go through the offical [get started](https://docs.docker.com/get-started/) documentation. Once you have Docker installed on your machine and feel confident with **at least part 1 and 2** of the tutorial you can continue with the steps below. _Taking the time to learn Docker will be an invaluable learning experience for your career as a software developer._

## Setup

1. **Clone the Template Repo**

Clone a local copy of the repo onto your machine and `cd` into the project directory.

    $ git clone https://github.com/ey-dna-pace/pace-2019-s1-group-2
    $ cd pace-2019-s1-group-2
    
When using git as a team we strongly encourage using the following methodology: [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/) _You should print the graphic on this page out and post it on your bedroom wall, analyse it once before you go to bed and again when you wake up in the morning. Everyday._

2. **Build the Docker image**

To use OpenCV as specified in the Dockerfile you are required to build an image. Docker will gather all the required dependencies to run OpenCV.

    $ docker build --tag=virtualprojectboard .
    
3. **Spin up a Docker Container**

During development you will want to update the source code of your Flask app without having to constantly rebuild your image. You can [mount a volume](https://docs.docker.com/storage/volumes/) for your working directory during development to keep your source up to date.

**Ensure the `<project_path>` segment of the following command is the correct syntax / path for your OS, on MacOs/Linux you can simply use `"($pwd)"`.**

    $ docker run -p 5000:5000 -m <project_path>:/app virtualprojectboard
    
4. **Check OpenCV is working**

If your installation has worked correctly you should see your Flask application is visitable at the following url http://127.0.0.1:5000. To ensure your Docker container is running as expected visit: http://127.0.0.1:5000/check_cv. This page will inform you if the application has access to OpenCV. If are you having any trouble, feel free to contact [Blake Lockley](mailto:blake.lockley@au.ey.com).


## Alternate Setup (No Docker/OpenCV)

If you are not working on functionality directly related to OpenCV or any other features of your app requiring dependencies included in your Dockerfile you can quickly spin up a virtual environment instead.

1. **Create a Virtual Environment** 

If you have not used virtualenv or similar tools before you can take a look here: [virtual environment](https://virtualenv.pypa.io/en/latest/). You should use a distribution of python 3 (preferably 3.7) already installed on your machine.

        $ virtualenv env --python=python3.7

2. **Activate your Virtual Environment**

Windows:
        
        $ env\Scripts\activate
        
MacOs/Linux:

        $ source env/bin/activate
        
Once your environment is activated you will notice the environments name `(env)` in the prompt.
        
3. **Install Requirements**

In the virtual environment, install dependencies from the requirements file.

        (env) $ pip install -r requirements.txt
        
4. **Run**

In the virtual environment, run the application as usual.

        (env) $ python app.py

_Impress Us_ 😉
