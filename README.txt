This is a command-line utility for use by sellers and managers of the company CoffeeForMe
Arguments of the utility are entered through the command line, also it is possible through the interactive mode

You can start script with entering name and position:
    '-n' or '--name' - Is used to set the name of the user.
    '-p' or '--position' - Is used to set the position of the user.
Or you can start script and enter them, when script ask you about it.

Script is capable of:
1. Saving the bill into a txt file. Each time new. 
(It contains information: seller name, date, time, total price, items with their prices).
2. Saving the details of sale into a DataBase, through the sqlite module. Data saved automatically for each sale. 
Sales details are available only for position "manager".
4. Saving the logs.
5. Showing everything what happens in logs via file handler.
6. Showing the name of file that experienced import failure, and the name of module that wasn't imported.
7. Catching all exceptions, that are most likely to happen.

