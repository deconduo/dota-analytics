dota-analytics
==============

Data Analytics project

This project is divided into three parts.

Setup:

This contains a python script that downloads information about previous Dota 2 games using Valve's Web API. The game type, lobby type, and other parameters can be specified.

First the Match IDs and corresponding skill level is downloaded and saved to a file. Then the detailed information for each game is collected and stored in a csv file.

Finally the csv file is cleaned, and set up to be ready for analysis

Analytics:

The data is then modelled using the analytics tools. Various models can be used including neural nets, decision trees, and support vector machines.

After an apropriate model is chosen, the model is created and saved for later use.

Site:

Finally a flask site uses the model built in part 2. Using the input of a Steam ID, the site fetches the last 25 games played by that player and returns the skill level and some other details in graph format.
