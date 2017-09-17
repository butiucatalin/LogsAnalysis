# Logs Analysis

An internal reporting tool that will use information from a large database to answer several questions.

## Program's design

The program has a main menu which prompts the user to choose from several options in order to display the answers to each of the questions in the lab description. For each of these questions, the code connects to and queries an SQL database. When the application fetches data from multiple tables, it uses a single query with a join, rather than multiple queries. The output is displayed in clearly formatted plain text put together into a table for a better user experience.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for using, development and testing purposes.

## Prerequisites

In order to run this program , you will need to install [Vergant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) to your machine .

### Install VirtualBox

VirtualBox is the software that actually runs the virtual machine. [You can download it from virtualbox.org, here](https://www.virtualbox.org/wiki/Downloads). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

Ubuntu users: If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.

### Install Vagrant

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. [Download it from vagrantup.com](https://www.vagrantup.com/downloads.html). Install the version for your operating system.

Windows users: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

### Download the VM configuration

There are a couple of different ways you can download the VM configuration.

You can download and unzip this file: [FSND-Virtual-Machine.zip](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip) This will give you a directory called FSND-Virtual-Machine. It may be located inside your Downloads folder.

Alternately, you can use Github to fork and clone the repository https://github.com/udacity/fullstack-nanodegree-vm.

Either way, you will end up with a new directory containing the VM files. Change to this directory in your terminal with cd. Inside, you will find another directory called vagrant. Change directory to the vagrant directory.

## Running the program

Instructions on how to run the program . Please follow the next steps.

### Start the virtual machine

From your terminal, inside the vagrant subdirectory, run the command  **vagrant up**

```
vagrant up
```

Then type **vagrant ssh** to log in to your Linux VM

```
vagrant ssh
```

Inside the VM, change directory to **/vagrant**

```
cd /vagrant
```

### Setting up the database

*You need to perform only once the steps described in this section.*

Use the command **psql -d news** to connect to the database

```
psql -d news
```

If there's no such database , create it by typing :

```
psql
```

and then :

```
create database news
```

In both cases return to **/vagrant** directory by typing :

```
\q
```

Next, [download the data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called **newsdata.sql**. Put this file into the **vagrant** directory, which is shared with your virtual machine.

Afterwards, return to your terminal and type **psql -d news -f newsdata.sql**

```
psql -d news -f newsdata.sql
```

Now that you are connected to your database , you must create a view that will be used by the program in order to retrieve data from this database . You must type in the console the following command :

```
create view articles_views as select articles.id, count(*) as views from articles join log on log.path = concat('/article/',articles.slug) where log.status like '%200%' group by articles.id ;
```

## Run the code

*Warning !*
Before the first use , you have to copy the file named `LogsAnalysis.py` from this repository into the **vagrant** directory, which is shared with your virtual machine.

In your terminal , go to the **/vagrant** directory and type **python LogsAnalysis.py** into the console

```
python LogsAnalysis.py
```

In this moment you are inside the main menu and from now on you can follow the instructions provided by the program right into your console.

#### What are the most popular three articles of all time?

To answer this question type **1** in the main menu .

```
1
```

#### Who are the most popular article authors of all time?

To answer this question type **2** in the main menu .

```
2
```

#### On which days did more than 1% of requests lead to errors?

To answer this question type **3** in the main menu and then **1** in the following submenu.

```
3
```
and

```
1
```

## Views

The code relies on the view `articles_views` created in the database :

```
create view articles_views as select articles.id, count(*) as views from articles join log on log.path = concat('/article/',articles.slug) where log.status like '%200%' group by articles.id ;
```

This view creates a new entry associating every individual article to its number of views . An article view is found and counted only when its correct path is accessed ( "/article" + article slug [ unique as defined by the database's constrains ] ) and the server's response is OK to the request ( status is "200 OK" ) .

## Built With

* [Python 2.7.13](https://www.python.org/downloads/release/python-2713/) - The environment used

## Authors

* **Butiu Catalin** - *Initial work* - [Butiu Catalin](https://github.com/butiucatalin)

## Credits

* **Udacity** - fragments from IPND materials were included in this documentation. Don't forget to visit [udacity.com](https://www.udacity.com/) !

## License

Open source.

## Acknowledgments

* Udacity
* My inspiration
* etc
