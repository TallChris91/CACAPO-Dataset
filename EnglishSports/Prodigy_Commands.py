import os
import pickle

labellist = ['ERA', 'RBI', 'atBatNumber', 'baseNumber', 'baseReachedNumber', 'baseStolen', 'basesRan', 'batterHitsTries', 'batterName', 'batterScoreNumber', 'battersFacedNumber', 'battingAverage', 'battingLineupNumber', 'catchType', 'catcherName', 'competitionName', 'earnedRunsNumber', 'errorNumber', 'fielderName', 'fielderPosition', 'finalScore', 'gameNumber', 'gameTally', 'hasLostTeam', 'hasScored', 'hasWonTeam', 'hitNumber', 'homeAway', 'homeRunNumber', 'injuryType', 'inningNumber', 'inningScore', 'inningsPitched', 'isOut', 'leftOnBase', 'locationPlayed', 'managerName', 'matchDate', 'matchStreakNumber', 'matchStreakType', 'numberOfStarts', 'onBaseNumber', 'outNumber', 'pitchCount', 'pitchNumber', 'pitchResult', 'pitchResultNumber', 'pitchType', 'pitcherName', 'pitcherRecord', 'pitcherSaveRecord', 'pitchesTotalThrown', 'presidentName', 'retireNumber', 'runAverage', 'runNumber', 'scoreNumber', 'scoreTally', 'standingsGames', 'startsNumber', 'stealNumber', 'strikeNumber', 'strikeOutNumber', 'strikeTrajectory', 'strikingType', 'teamName', 'teamRecord', 'teamStandings', 'throwDirection', 'umpireName', 'umpireType', 'unearnedRunsNumber', 'walkNumber', 'winLossRecord', 'winLossType', 'winningPercentage']
newlabellist = sorted(labellist)
#print(newlabellist)
#exit(0)
labelliststring = ','.join(newlabellist)

os.system('C:/Users/chris/venv/Scripts/activate')
os.system('cd C:/Users/chris/Desktop')
os.system('python -m prodigy ner.correct EnglishSportsTrain en_core_web_md C:/Users/chris/Desktop/Train/FullTrain.jsonl --label ' + labelliststring + ' --unsegmented')

#os.system('python -m prodigy db-out EnglishSportsTrain > C:/Users/chris/Desktop/EnglishSportsTrain.jsonl')
