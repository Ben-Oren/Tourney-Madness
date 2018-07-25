import pandas as pd
import numpy as np
import json

#get data
with open('test.json') as data_file:
	data = json.load(data_file)
	
df = pd.DataFrame(data)

#remove N/A rows that were buffers in original data
#what do those rows look like?
#	'game number' serves as index per team per season, look at game number variable
#		df['game number'].unique()
#		all integers except for 'G'
#	look at values for columns in rows that have 'G'
#		for column in df.columns:
#			len(df.ix[df['game number'] == 'G', column].unique())
#		all have 1 value except for team 
# 	so, restrict data frame to rows that don't have 'G' as game number

df = df.ix[df['game number'] != 'G', :]

#change home / away values to "home", "away" and "N" (neutral site)
df.ix[df['home_away'] == '@', 'home_away'] = 'away'
df.ix[df['home_away'] == 'N/A', 'home_away'] = 'home'

#create conf column
#BUT need to demarcate seasons by date before doing; currently grouped just by year, doesn't capture November to March grouping
#SO change seasons to capture November to March grouping

df.ix[:, 'Month'] = df.date.map(lambda x: x[5:8])
df.season = df.season.astype(int)
df.season = df.season - df.Month.map({	'Jan': 1,
                                        'Feb': 1,
 										'Mar': 1, 
										'Apr': 1,
										'Nov': 0,
										'Dec': 0})

#That's done, so now create conference column with fast pandaized method
grouped = df.groupby(['team', 'season'])['conf_opp'].value_counts()

conference = pd.DataFrame(grouped)
conference.columns = ['value count']
		
conference = conference.reset_index()
conference['count max'] = conference.groupby(['team', 'season'])['value count'].transform(max)
conference['marker'] = np.sign(conference['value count'] - conference['count max'])

conference = conference.ix[conference['marker'] == 0, :]

conference = conference.ix[:,['team', 'season', 'conf_opp']]

conference.columns = ['team', 'season', 'conf']

#check to see if this "get max opp conf and set conf to that value" method results in dupes:
#conference.loc[:, 'duplicated'] = conference.duplicated(subset = ['team', 'season'], keep = False)

#if so and they're just a few dumb teams:
#conference = conference.loc[conference['duplicated'] == False, :]
#conference = conference.drop('duplicated', 1)

conf_df = pd.merge(df, conference, how = 'inner', on = ['team', 'season'])

#add 'conf_game' marker column

conf_df.loc[:, 'conf_game'] = conf_df.apply(lambda x: 1 if x['conf_opp'] == x['conf'] else 0, axis = 0)

#create streak columns
#change game number to int

conf_df.loc[:, 'game number'] = conf_df['game number'].astype(int)

#initialize streaks with first game
conf_df.loc[conf_df['game number'] == 0, 'losing_streak_pre_game'] = 0
conf_df.loc[conf_df['game number'] == 0, 'winning_streak_pre_game'] = 0

#create a bunch of frames by team and season, sort by game number
#Needs "won_game" column
conf_df.loc[:, 'won_game'] = conf_df.w_l.map({'W':1, 'L':0})

#split up into frames by team and season
frame_list = []
for team in conf_df.team.unique():
	for season in conf_df.loc[conf_df['team'] == team, 'season'].unique():
		frame = conf_df.loc[(conf_df['team'] == team) & (conf_df['season'] == season), :]
		frame = frame.sort_values(['game number'], ascending == True)
		frame_list.append(frame)

#'winning streak generation' function (note: this is the winning streak before the game is played, so the value for the first game is 0, value for the second game is the result of the first game, etc) 
def win_streak_column(row, frame):
	if frame.loc[row, 'game number'] < 2:
		return 0
	if frame.loc[row-1, 'won_game'] == 0:
		return 0
	
	team_var = frame.loc[row, 'team']
	season_var = frame.loc[row, 'season']
	
	first_game_index = frame.index[(frame.team == team_var) & (frame.season == season_var) & (frame['game number'] == 1)].tolist()[0]
	
	start_idx = frame['won_game'].loc[first_game_index:row-1][frame['won_game'] == 0].last_valid_index()
	
	if type(start_idx) == None.__class__:
		start_idx = first_game_index - 1
	
	return i - 1 - start_idx
	
def losing_streak_column(frame, row):
	if frame.loc[row, 'game number'] < 2:
		return 0
	if frame.loc[row - 1, 'won_game'] == 1:
		return 0
		
	team_var = frame.loc[row, 'team']
	season_var = frame.loc[row, 'season']
	
	first_game_index = frame.index[(frame.team == team_var) & (frame.season == season_var) & (frame['game number'] == 1)].tolist()[0]
	
	start_idx = frame['won game'].loc[first_game_index:row-1][frame['won_game'] == 1.last_valid_index()
	
	if type(start_idx) == None.__class__:
		start_idx = first_game_index - 1
		
	return row - 1 - start_idx	
	
#create column in each frame
hold_list = []
for frame in frame_list:
	frame.loc[:, 'winning_streak_pre_game'] = frame.index.to_series().map(lambda i: win_streak_column(i, frame))
	hold_list.append(frame)

frame_list = hold_list

ff = pd.concat(frame_list)

#alt code to get win / losing streaks on big frame row by row
# for row in ddtest.index:
#      ...:     game = ddtest.loc[row, 'game number']
#      ...:     if game >1:
#      ...:         prev_game = ddtest[ddtest['game number'] == game - 1].index.tolist()[0]
#      ...:         prev_win_streak = ddtest.loc[prev_game, 'winning_streak_pre_game']
#      ...:         prev_lose_streak = ddtest.loc[prev_game, 'losing_streak_pre_game']   
#      ...:         if ddtest.loc[prev_game, 'w_l'] == 'W':
#      ...:             ddtest.loc[row, 'winning_streak_pre_game'] = prev_win_streak + 1
#      ...:             ddtest.loc[row, 'losing_streak_pre_game'] = 0
#      ...:         if ddtest.loc[prev_game, 'w_l'] == 'L':
#      ...:             ddtest.loc[row, 'losing_streak_pre_game'] = prev_lose_streak + 1
#      ...:             ddtest.loc[row, 'winning_streak_pre_game'] = 0



#rejigger some variables

#convert ot to numeric

ff.loc[:, 'ot'] = ff.ot.map({'N/A': 0, 'OT':1, '2OT': 2, '3OT': 3, '4OT':4, '5OT':5, '6OT':6})

#convert pts and opp_pts to int
#create pts_diff variable
#if haven't gone back to grab 2017 season data, the above pts code needs to have ff.loc[ff.pts != 'N/A', 'pts'] etc. throughout
ff['pts'] = ff['pts'].astype(int)
ff['opp_pts'] = ff['opp_pts'].astype(int)
ff['pts_diff'] = f['pts'] - f['opp_pts']

#w/l variables
#wins pre_game

def w_pregame(frame, row):
	if frame.loc[row, 'game number'] == 1:
		return 0
		
	team_var = frame.loc[row, 'team']
	season_var = frame.loc[row, 'season']
	
	first_game_index = frame.index[(frame.team == team_var) & (frame.season == season_var) & (frame['game number'] == 1)].tolist()[0]
	
	return frame.loc[first_game_index:row-1, 'won_game'].sum()
		
#won previous game
def won_prev_game_col(frame, row):
	if frame.loc[row, 'game number'] == 1:
		return np.nan
	return frame.loc[row-1, 'won_game']

#w/l avg pregame, entire season
def w_avg_pregame_season(frame, row):
	if frame.loc[row, 'game number'] == 1:
		return 0
	
	prev_game_number = frame.loc[row-1, 'game number']
	
	return (frame.loc[row, 'w_pregame']) / prev_game_number
		
#w/l avg pregame, over last 5 games
def w_avg_pregame_5gms(frame, row):
	return pd.rolling_mean(frame.won_prev_game, 5, min_periods = 1)
	
#pts previous game
def pts_prev_game_col(frame, row):
	if frame.loc[row, 'game number'] == 1:
		return np.nan
	return framee.loc[row-1, 'pts']
	
#avg pts, season
def avg_pts_pregame_sn(frame, row):
	if frame.loc[row, 'game number'] == 1:
		return np.nan
		
	team_var = frame.loc[row, 'team']
	season_var = frame.loc[row, 'season']
	
	first_game_index = frame.index[(frame.team == team) & (frame.season == season_var) & (frame['game number'] == 1)].tolist()[0]
	
	return frame.loc[first_game_index:row-1, 'pts'].sum() / frame.loc[row-1, 'game number']
	
#avg pts previous 5 games
def avg_pts_pregame_5gms(frame, row):
	return pd.rolling_mean(frame.pts_pregame, 5, min_periods = 1)
	
	
#Including opponents stats from recent games
#Cleaning up team names so can cross-reference team names and dates
def rename_team(frame, team_var):
	t = team_var
	f = frame
	f = f.loc[f['team'] == t, :]
	
	opponent_date = f.loc[0, ['opponent', 'date']].tolist()
	
	new_name = f.loc[(f.team == opponent_date[0]) & (f.date == opponent_date[1]), 'opponent'].tolist()
	
	if len(new_name) == 1:
		return new_name[0]
		
	else:
		
		opponent = f.loc[f['team'].isin(f.loc[f['team'] == t, 'opponent'].unique().tolist()), 'team'].value_counts().index.tolist()[0]
		
		date = f.loc[(f['team'] == t) & (f.opponent == f.loc[f['team'].isin(f.loc[f['team'] == t, 'opponent'].unique().tolist()), 'team'].value_counts().index.tolist()[0]), 'date'].tolist()[0]
		
		try:
			new_name = f.loc[(f.team == opponent) & (f.date == date), 'opponent'].tolist()[0]
			return new_name
			
		except IndexError:
			return team
			
#to implement the above:
#team_to_replace = dd.loc[~dd.team.isin(dd.opponent.unique().tolist()), 'team'].unique().tolist()
#rename_team_dict = {}
#for team in team_to_replace:
#	rename_team_dict[team] = rename_team(dd, team)
#	dd.team = dd.team.replace(rename_team_dict)
	
#compare In [1304] and In [1386] for the right opp_pts_prevgame function
# In [1304]
temp = dd.groupby(['team', 'season'])
def opp_pts_prevgame(row):
	a = dd.loc[temp.groups[(dd.opponent[row], dd.season[row])]]
	frame = a[a.shift(-1)['date'] == dd.date[row]]
	
	if len(frame) == 0:
		return np.nan
	else:
		return frame['pts'].tolist()[0]
		
#In [1386]
temp = dd.groupby(['team', 'season'])
def opp_pts_prevgame(row):
	try:
		a = dd.loc[temp.groups[(dd.opponent[row], dd.season[row])]]
		frame = a[a.shift(-1)['date'] == dd.date[row]]
	
		if len(frame) == 0:
			return np.nan
		else:
			return frame['pts'].tolist()[0]
	
	except KeyError:
		return np.nan

#get dummy variables for home_away, conf, conf_opp, type, Month
f_concat = pd.get_dummies(ff, columns = ['home_away', 'conf', 'conf_opp', 'type', 'Month'])

#create a merge frame by dropping non_key and non_merge columns
f_concat = f_concat.drop(['opponent', 'conf_game', 'winning_streak_pre_game_fast', 'pts', 'opp_pts', 'ot', 'wins', 'losses', 'won_game', 'pts_diff'], axis = 1)

#merge that mo so that main frame has dummy variables and original columns too
ff = pd.merge(ff, f_concat, how = 'inner', on = ['team', 'season', 'game_number', 'date'])





test = test[['team', 'season', 'season_fix', 'season_test', 'game number', 'date', 'Month', 'opponent', 'conf_game', 'home_away', 'home', 'wins_post_game', 'winning_streak', 'losses_post_game', 'losing_streak', 'w_l', 'game_won', 'pts', 'opp_pts', 'pts_diff', 'ot', 'type', 



		
