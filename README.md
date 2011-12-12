---
**Ocean Observatories Initiative Cyberinfrastructure** 
**Integrated Observatory Network (ION)** 

pydap-handler-ion - Pydap handler for serving data from OOI-CI ION

(C) UC Regents, 2010-2011

---

# Description
*some really excellent description*

**References**  
*references to any architecture, design, or external pages*

#Prerequisites

This assumes basic development environment setup (git, directory structure). Please follow the
"New Developers Tutorial" for basic steps.

Pyon: The main dependency of this repository is the pyon Capability Container. Follow the listed
steps to install the minimal needed dependencies to run pyon on a Mac. For more details and Linux
install instructions, check out the pyon README: https://github.com/ooici/pyon/blob/master/README



Install the following if not yet present:

- git 1.7.7: Download the Mac or Linux installer and run it

- OS Packages and package management:
For Mac, use homebrew
    > /usr/bin/ruby -e "$(curl -fsSL https://raw.github.com/gist/323731)"
- python 2.7
*see below for installation*

* couchdb 1.1.0 (optional if memory mockdb is used)
*see below for installation*

- rabbitmq 2.6.1 or later (recommended, but can use rabbitmq on amoeba)
    *Download generic Linux version and unpack into a suitable directory.
    **Note:** May need erl (Erlang) and some dependencies installed before*

- **Install** libevent, libyaml, zeromq, couchdb, python, and rabbitmq with Homebrew
    > brew install libevent libyaml zeromq couchdb python rabbitmq

    You can even reinstall git using brew to clean up your /usr/local directory
    Be sure to read the pyon README for platform specific guidance to installing
    dependent libraries and packages.
    Linux: Note that many installs have much older versions installed by default.
    You will need to upgrade couchdb to at least 1.1.0.

Python packages and environment management:

- pip
    > easy_install pip

- virtualenv and virtualenvwrapper modules for your python 2.7 installation
    > easy_install --upgrade virtualenv
    > easy_install --upgrade virtualenvwrapper
    Note: This may require Mac's XCode (use XCode 3.3 free version)

- Setup a virtualenv to run COI-services (use any name you like):
    > mkvirtualenv --no-site-packages --python=python2.7 coi
    Note: Do not use the pyon virtualenv if you are a pyon developer

###Compiled Library Dependencies
- hdf5 library 

     > brew install hdf5

- netcdf

    > brew install netcdf

###Other OOI-CI Project Dependencies

This project requires that both the pyon and eoi-services projects are installed in the same directory as the pydap-handlers-ion project (typically the "Dev/code" directory if the OOI-CI development directory structure is used).  These projects can be obtained using the following commands:

    git clone git@github.com:ooici-eoi/eoi-services.git
    git clone git@github.com:ooici/pyon.git

#Source

Obtain the eoi-agents project by running:  

    git clone git@github.com:ooici-eoi/pydap-handler-ion.git
    cd pydap-handler-ion

#Buildout

Build the project using buildout

    python bootstrap.py
    bin/buildout

#Running the test server

You can test the ION handler for pydap by starting the test server

    bin/run-server.sh

Then browse to *http://127.0.0.1:8001* to see and interact with the test datasets

