# <font style="font-size:1.2em;">superturkersServer Documentation</font>
by Susumu Saito *(last updated: 2018-03-16)*

---

# <font color="red">[IMPORTANT]</font> Rule for Server Development

#### 1. Always modify the test server.

Keep the deployment server clean and glitch-free. The main purpose of having a test server is to avoid making server-client communication protocols inconsistent during server development, which would prevent client code developers from testing due to server errors. The deployment server should be always updated ONLY by ```git pull```ing the code that is pushed from the test server (and django migration --- to be described later).

#### 2. Only one person can edit at the same time.

Communicate with people to always make sure nobody else's there. Since we have only one test server and it's therefore a shared space, it is very likely that you unconsciously screw up or overwrite others' code they're still working on (this is a tragedy!) So do not forget to make sure you're the only one, otherwise just wait until he/she's done.

#### 3. Remember to push code when finished, and let people know.

Do NOT leave with your work-in-progress code left. For the above reason, the test server remains "locked" forever until you finish editing the code; nobody has a clue about to what extent you've already done and you haven't. Imagine that someone had to take over your incompleted code in some case of emergency --- unexpected glitch or overwriting is very likely. So just keep in mind the following procedure:

1. Push your server code, **as well as its corresponding fix on the client code**
2. Pull your server code on the deployment server
3. Let people know that you pushed the code (and tell them to pull your updated client code)

---

# Notations

### Keywords in this documentation

* *Deployment server* ... a production server environment, with which real crowdworkers' client code interact. Always needed to be bug-free, and cannot be modified directly.
* *Test server* ... a debug server environment, which is a duplicate of the deployment server. The server code in this environment can be modified for testing, but only by one person at a time.

### CUI commands

When ```%``` is at the head of a command line, it is executed on your laptop localhost environment (e.g., MacBook's Terminal). When ```$``` is at the top, it is executed on the remote webfaction server (i.e., command line after logging in to the server with ```ssh```, yet still on the same terminal app).

	% some commands on your laptop localhost environment
	$ some commands on the remote webfaction server

### Names

<table>
  <tr>
    <th></th><th>Deployment</th><th>Test</th>
  </tr>
  <tr>
    <th bgcolor="#ddd">Subdomain<br>&lt;subdomain></th>
    <td style="text-align:center;" bgcolor="white">extension.superturker.com</td>
    <td style="text-align:center;" bgcolor="white">test.superturker.com</td>
  </tr>
  <tr>
    <th bgcolor="#fbe">WebFaction Application<br>&lt;wf_app></th>
    <td rowspan="4" style="text-align:center;">superturk</td>
    <td rowspan="4" style="text-align:center;">superturk_test</td>
  </tr>
  <tr>
    <th bgcolor="#fbe">WebFaction Website<br>&lt;wf_website></th>
  </tr>
  <tr>
    <th bgcolor="#bef">MySQL DB<br>&lt;mysql_db></th>
  </tr>
  <tr>
    <th bgcolor="#bef">MySQL Log in User (=passwd)<br>&lt;mysql_user></th>
  </tr>
  <tr>
    <th bgcolor="#feb">Django Project<br>&lt;django_project></th>
        <td colspan="2" style="text-align:center;" bgcolor="white">superturker</td>
  </tr>
  <tr>
    <th bgcolor="#feb">Django Application<br>&lt;django_app></th>
    <td colspan="2" style="text-align:center;" bgcolor="white">scraper</td>
  </tr>
</table>

---

# Basic Operations

## 1. Logging in to WebFaction server

Connecting to BigLab's shared remote server hosted by WebFaction via CUI.<br>
To sign in, we use "jbigham" as a username (ask Jeff for a password).

#### On local environment (your laptop localhost):
	$ ssh jbigham@codingthecrowd.com
	jbigham@codingthecrowd.com's password: ***************

### *(Optional: Creating ssh login shortcut)*

You can shorten the log-in command by setting an ssh profile.

#### On local environment:

	$ printf "Host biglab\nUser jbigham\nHostName codingthecrowd.com" >> ~/.ssh/config
	# From next time, just login by typing below:
	$ ssh biglab 
	
## 2. Getting to working location

### Navigating to a WebFaction application directory

*In general, you can access to all the WebFaction application directories by executing:

	$ cd ~/webapps/<application_name>
	
Since you're supposed to always modify the test environment (see the "Rule for Server Deployment" at the top), just do:

	$ cd ~/webapps/superturk_test
	
### Application directory structure (only essential directories)

Here's a list of essential directories/files for server development.

	superturk (or superturk_test)
	 + apache2/
	 |  + bin/           --> exec files for apache2 commands
	 |  |  + restart
	 |  |  + start
	 |  |  + stop           --> execute by "./<command> (e.g., "./restart")
	 |  |  + ...
	 |  + ...
	 + superturker/   --> django project directory
	 |  + django.log     --> server program log outputs
	 |  + manage.py      --> exec file for django commands
	 |  + superturker/   --> project configurations
	 |  |  + ...
	 |  + scraper/       --> django app directory
	 |  |  + models.py      --> defining DB tables and DB accessing functions
	 |  |  + views.py       --> functions for response to client requests
	 |  |  + urls.py        --> links between view.py functions and URL for RESTful API
	 |  |  + ...
	 + ...

## 3. Editing and testing on test server

### Basic things to edit

There are not so many things you might want to do on the server code.
Some operations are described in "Advanced Operations" below:

1. To modify table structure, change models.py and migrate DB. See "Adding/Changing/Deleting columns to DB".
2. To see test output logs (like you normally do by "print()"), see "Viewing django server logs".
3. To set/change operation triggered by URL request, modify view.py and url.py and restart apache2 server.
4. To add new python packages, see "Installing python package (pip)".

### Pushing code to GitHub

Don't forget to push your code to GitHub when you finish editing/testing the program,  so that the deployment server is simply updated by pulling the code you pushed from the test environment.

	

## 4. Updating deployment server

<u><font color="red">**[Caution]**</font> Make sure the code is glitch-free beforehand.</u>

Simply execute the command below (executing all the essential commands --- ```git pull```, DB migration, and restarting apache2 --- in a batch).

	$ cd ~/webapp/superturk/    # navigate to the deployment server
	$ ./auto_update
	
---

# Advanced Operations

## Accessing MySQL DB via client

If you are using Mac, the best way is to install [Sequel Pro](https://www.sequelpro.com/).
If you are a Windows user, there are multiple solutions but one of the well-known client apps is [MySQL Workbench](https://www.mysql.com/products/workbench/).

To access the database, you'll first log into the webfaction server via SSH and then log into the MySQL database locally --- don't worry, most MySQL client apps do them all in the background.

For example, using Sequel Pro, all you need to do is to input the following parameters and click "Connect" button:

<table>
  <tr><th></th><th>Parameter name</th><th>Value</th></tr>
  <tr><th rowspan=4>SSH<br>(same as "Basic<br>Operations" (1.))</th><td>Host</td><td>codingthecrowd.com</td></tr>
  <tr><td>User</td><td>jbigham</td></tr>
  <tr><td>Password</td><td>**ask Jeff**</td></tr>
  <tr><td>Port</td><td>22 (default)</td></tr>
  <tr><th rowspan=4>MySQL</th><td>Host</td><td>127.0.0.1</td></tr>
  <tr><td>User</td><td>guest (view-only)</td></tr>
  <tr><td>Password</td><td>guest</td></tr>
  <tr><td>Port</td><td>29755</td></tr>
</table>

It just looks like the following:

<img src="https://dl2.pushbulletusercontent.com/xSEK4pvp9GieT2REKNVzXKyxaoI1Q8Ee/Screenshot_2018-03-20%2017.02.49.png" style="width:400px;" />



## Adding/Changing/Deleting columns to DB

### At a glance:
1. Modify model.py
2. Run django migration commands

<u><font color="red">**[Caution]**</font> Do NOT directly run SQL commands to make changes.</u>

### 1. Modify model.py

In Django, all information for DB table structure is written in model.py. We want to always keep consistency between what's written in the file and what's actually in MySQL DB.

Each table in DB is defined with a python class, and each column of the table is a class variable. For example, if you create "Worker" python class with "age", "gender", and "country" variables, a table called "*&lt;django\_app>_worker*" with columns named "age", "gender", and "country" will be created in the DB.

For more detailed information for modifying model.py, [see Django documentation](https://docs.djangoproject.com/en/2.0/topics/db/models/#fields).

### 2. Migrate DB tables

	$ python3.6 manage.py makemigrations scraper   # creating migration file
	$ python3.6 manage.py migrate                  # migrate

#### [Common issue on migration]

You will get the following error when you **add** a column without a default value, while one or more records are already stored in the table.

```
$ python3.6 manage.py makemigrations scraper
You are trying to add a non-nullable field 'answers' to posthitsurveyanswer without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit, and let me add a default in models.py
Select an option: 1
Please enter the default value now, as valid Python
The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
Type 'exit' to exit this prompt
>>> ""
```

## Refreshing server (Restarting Apache2 server daemon)

You are often required restarting apache when you pull a new code from github / migrate django database. Try to execute ```./restart``` if your server code is not refreshed.

	$ cd ~/webapps/superturk/apache2/bin
	$ ./start      # start server
	$ ./stop       # stop server
	$ ./restart    # restart server

## Viewing django server logs

It is usually not desirable to do any debugging directly on WebFaction server (do it on test server), but if you want to do brief check of the program, do ```logger.info(somestring)``` instead of something like ```print(somestring)```.

The log output is printed in an error log. To see the log, just open with any editor like vim, as follows:

	$ vim ~/logs/user/error_superturk.log

Or you might want it to be automatically refreshed as you run the program --- then do in a splitted tmux window or something:

	$ less +F ~/logs/user/error_superturk.log

## Installing python package (pip)

On WebFaction server, you are not granted ```sudo``` privilege --- do as follows instead:

	$ cd ~/lib/python3.6
	$ pip3.6 install <package_name>

## Renewing certificate

Let'sEncrypt SSL certificate expires in 3 months --- if it's expired, you'll get <span style="color:red">NET::ERR\_CERT\_DATE\_INVALID</span> error upon server communication. This needs to be done for both the deployment server and the test server.


#### On webfaction server:

	$ cd ~/src
	$ acme.sh --renew -d extension.superturker.com

#### On local environment:

1. log in to webfaction control panel on your web browser, navigate to "DOMAIN / WEBSITES" on the top tab and "SSL certificates" on the second tab.
2. click "superturk" profile.
3. copy certificate strings to your laptop (because it's kinda annoying to copy strings directly from the server)

		$ mkdir ~/acme_superturker && cd ~/acme_superturker
		$ scp -r jbigham@codingthecrowd.com:/home/jbigham/.acme.sh/<subdomain> .
		jbigham@codingthecrowd.com's password: ***************
 	
4. copy & paste certificate strings in text boxes on the console
 * “Certificate” -> \<subdomain\>.cer
 * “Private key” -> \<subdomain\>.key
 * “Intermediates/bundle” -> fullchain.cer

## References

* [SuperTurkersServer Github repository](https://github.com/CMUBigLab/superturkersServer)
* [WebFaction-letsencrypt](https://community.webfaction.com/questions/19988/using-letsencrypt)
* [Installing socat on webfaction server](https://community.webfaction.com/questions/21246/trying-to-use-lets-encrypt-using-acmesh-need-socat-tools)
* [Importing & Exporting MySQL DB on WebFaction](https://docs.webfaction.com/user-guide/databases.html#import-and-export-database-records)
* [git diff to ignore ^M](https://stackoverflow.com/questions/1889559/git-diff-to-ignore-m)
