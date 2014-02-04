# Arte: World of Work
[![Build Status](https://travis-ci.org/jplusplus/arte-world-of-work.png?branch=master)](https://travis-ci.org/jplusplus/arte-world-of-work)

[![Coverage Status](https://coveralls.io/repos/jplusplus/arte-world-of-work/badge.png?branch=master)](https://coveralls.io/r/jplusplus/arte-world-of-work?branch=master) 

## Installation
**1. Prerequisites**
The following library & tools are required to run this project in local:
- python (2.6+)
- pip
- libmemcached
- libjpeg
- zlib

On ubuntu:
```
sudo apt-get install build-essential git-core python python-pip python-dev libmemcached-dev libjpeg62 libjpeg62-dev zlib1g-dev
``` 

**2. Download the project**

```bash
# pwd: ~
git clone git@github.com:jplusplus/arte-world-of-work.git 
cd arte-world-of-work
``` 

**3. Install** 
```bash
# pwd: ~/arte-wow
make install
```

## Troubleshooting 
- **I have a 'No module named defaults' error**
  
  Try to run: `pip install --upgrade -r requirements.txt`
