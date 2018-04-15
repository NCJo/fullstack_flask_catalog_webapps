# Catalog Web App Project

This fullstack web application was developed in flask, SQLalchemy, HTML5, CSS, Bootstrap.
It also contains several JSON endpoints.

### Tech

Catalog App relies on several packages to be able to successfully run :

* Python2
* Flask
* Virtual Box - VM environment
* Vagrant - Configuration program

### Installation

1.) Install VirtualBox from this [website](https://www.virtualbox.org/wiki/Downloads)
2.) Install Vagrant from this [website](https://www.vagrantup.com/downloads.html)
3.) Vagrant takes a configuration file called *Vagrantfile* that tells it how to start your Linux VM. Download the Vagrantfile [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f73b_vagrantfile/vagrantfile)

### How to run
1.) Download the code or clone a repository from GitHub (To clone a repo, type the code below in the terminal)
```sh
$ git clone https://github.com/NCJo/fullstack_catalog_webapps.git
```
2.) Navigate to the repository folder
3.) Start virtual machine by run the following command in the directory
```sh
$ vagrant up
```
follow by
```sh
$ vagrant ssh
```
4.) Navigate to the Catalog App folder
5.) Set up database by running this command
```sh
$ python models.py
```
6.) Populate database with fake data
```sh
$ python lotsfproducts.py
```
7.) Run Web server by
```sh
$ python application.py
```
8.) The server is running locally using http://localhost:8000

### JSON Endpoints
* /items.json
   - show all items in the database in JSON
* /category.json
   - show all categories in teh database in JSON
* /<category name>/items.json
   - show all items in certain category in JSON
