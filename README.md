# Arte: World of Work

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
git clone git@github.com:jplusplus/arte-wow.git 
cd arte-wow
``` 

**3. Install** 
```bash
# pwd: ~/arte-wow
make install
```

## Troubleshooting 
- [I have a 'No module named defaults' error](#wiki-troubleshooting_1)

#### <a name='troubleshooting_1' href="README#wiki-troubleshooting_1">1.</a> I have a 'No module named defaults' error 
Try to run:
```sh
pip install --upgrade -r requirements.txt
```
