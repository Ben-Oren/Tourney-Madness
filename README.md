# Tourney-Madness
What predicts a college basketball team's record in the March Madness tournament?  

This project scrapes info from every game on sports-reference.com since 1990 to find out.  

The scraper grabs the game information for each team on its sports-reference.com page and stores it in json format.  Each row of data has:

team, season, date, game number (for that team within the season), type (regular season, conf tourney or march madness game), home/away, opponent, the conference of the opponent, whether the team won the game, the pts scored by the team and its opponent, # of overtimes, and the win, loss, and current w/l streak of the team after the game.

The data_cleaning file reads the raw json file generated by the scraper and transforms or calculates variables to either alter data in a more analysis-friendly format, or to create variables that weren't specified.  M

Most importantly, this is calculating a variable to use as a dependent in analysis: how many games the team in the current sesason actually won in the march madness tourney.  The data cleaning also includes finding the conference of the team, its pre-game win / loss records, and calculating things like point differential, average points, and streaks - calculated on the season and 5- and 10-game streaks - for both the team and its opponent in each game.  

The state of the project:  data cleaning is pretty much done, and analysis can start to begin.  This will include running an introductory correlations and regressions to see what the linear relationships among the variables are, and then a series of random forests to see if we can tease out more specific relationships among the data.  
