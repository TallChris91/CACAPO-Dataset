import os
import pickle

labellist = ['ERA', 'RBI', 'atBatNumber', 'baseNumber', 'baseReachedNumber', 'baseStolen', 'basesRan', 'batterHitsTries', 'batterName', 'batterScoreNumber', 'battersFacedNumber', 'battingAverage', 'battingLineupNumber', 'catchType', 'catcherName', 'competitionName', 'earnedRunsNumber', 'errorNumber', 'fielderName', 'fielderPosition', 'finalScore', 'gameNumber', 'gameTally', 'hasLostTeam', 'hasScored', 'hasWonTeam', 'hitNumber', 'homeAway', 'homeRunNumber', 'injuryType', 'inningNumber', 'inningScore', 'inningsPitched', 'isOut', 'leftOnBase', 'locationPlayed', 'managerName', 'matchDate', 'matchStreakNumber', 'matchStreakType', 'numberOfStarts', 'onBaseNumber', 'outNumber', 'pitchCount', 'pitchNumber', 'pitchResult', 'pitchResultNumber', 'pitchType', 'pitcherName', 'pitcherRecord', 'pitcherSaveRecord', 'pitchesTotalThrown', 'presidentName', 'retireNumber', 'runAverage', 'runNumber', 'scoreNumber', 'scoreTally', 'standingsGames', 'startsNumber', 'stealNumber', 'strikeNumber', 'strikeOutNumber', 'strikeTrajectory', 'strikingType', 'teamName', 'teamRecord', 'teamStandings', 'throwDirection', 'umpireName', 'umpireType', 'unearnedRunsNumber', 'walkNumber', 'winLossRecord', 'winLossType', 'winningPercentage']
newlabellist = sorted(labellist)
labelliststring = ','.join(newlabellist)

#Create a Virtual Environment with prodigy and spacy (and the relevant models) beforehand
os.system(os.getcwd() + '/venv/Scripts/activate')
os.system('cd ' + os.getcwd())
os.system('python -m prodigy ner.correct EnglishSports en_core_web_md ' + os.getcwd() + '/Data/SportsJson.jsonl --label ' + labelliststring + ' --unsegmented')

#os.system('python -m prodigy db-out EnglishSports > ' + os.getcwd() + '/Data/EnglishSportsAll.jsonl')
