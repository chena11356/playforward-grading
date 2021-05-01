import sys
import json
import os

#### Variables to update before running
# PRINT_ACTIONS: if True, add list of actions to final data. If False, don't.
PRINT_ACTIONS = False

IDs = {
  200:	'Player enters Stack',
  203:	'Player completes Stack',
  204:	'Player exits Stack',
  205:	'Player finds object',
  207:	'Player panned Scene',
  208:	'Player reviewed Key Point in Change Decision Dialog',
  210:	'Player begins to scan Scene using Sense',
  211:	'Player ends scan',
  212:	'Player switches to a Sense',
  213:	'Player touches Object',
  216:	'Player triggers Stack Animatic',
  217:	'Player exits Stack Animatic',
  218:	'Player closes scene info panel',
  219:	'Player opens scene info panel',
  220:	'Player closes Change Decision panel',
  221:	'Player opens Change Decision panel',
  703:	'Player sees Epilogue panel',
  704:	'Player opens up Epilogue Item',
  705:	'Player closes Epilogue Item',
  706:	'Player pans epilogue',
  707:	'Player rates the Epilogue',
  708:	'Player hits done button',
  0:	'Player starts session',
  1:	'Player ends session',
  100:	'Player opens Challenge Stack popup',
  101:	'Player cancels entering Challenge Stack',
  102:	'Player confirms entering Challenge Stack',
  103:	'Player touches Epilogue button',
  104:	'Player cancels entering the Epilogue',
  105:	'Player confirms entering the Epilogue',
  600:	'Player selects age',
  601:	'Player selects gender',
  602:	'Player commits to age and gender',
  603:	'Player selects avatar',
  604:	'Player commits to avatar and name',
  605:	'Player exits avatar creator',
  300:	'Player enters the aspirational avatar',
  301:	'Player chooses an aspirational avatar level',
  302:	'Player selects aspirational avatar choice',
  303:	'Player starts typing in label entry',
  304:	'Player hits save button on aspirational avatar question popup',
  305:	'Player hits cancel button on aspirational avatar question popup',
  306:	'Player gains a star in a Asp. Avatar level',
  1000:	'Player hits replay on results panel',
  1001:	'Player hits done on results panel',
  1002:	'Player exits game through top bar back arrow',
  1003:	'Player enters Level Select menu',
  1004:	'Player selects minigame level',
  1005:	'Player earns additional skill point',
  400:	'Player closes intro panel to start game',
  401:	'Player hits continue arrow after the starter statement',
  402:	'Player selects "True"',
  403:	'Player selects "False"',
  404:	'Player selects "Opinion"',
  405:	'Player hits continue on their character\'s dialogue for how they identified starter\'s statement',
  406:	'Player hits continue on results for how they identified starter\'s statement',
  407:	'Player selects a fact card in the library view',
  408:	'Player selects "Use Fact" to use chosen fact card',
  409:	'Player hits continue on their character\'s dialogue reaction to their chosen fact card',
  410:	'Player hits continue on results for their chosen fact card',
  411:	'Player hits continue on the Round recap dialog that reiterates the facts',
  412:	'Player hits continue arrow at start of the It\'s On! section',
  413:	'Player hits continue arrow after opponent\'s It\'s On! statement',
  414:	'Player hits continue arrow after crowd response to opponent\'s It\'s On! statement',
  415:	'Player selects answer in It\'s On!',
  416:	'Player hits continue arrow their character says their chosen It\'s On answer',
  417:	'Player hits continue arrow after crowd response to their chosen It\'s On! statement',
  418:	'End of It\'s On',
  419:	'Player hits continue on results from It\'s On',
  420:	'End of level',
  500:	'Player closes intro panel to start game',
  501:	'Player hits continue arrow after first opponent statement',
  502:	'Player selects answer for what opponent means',
  503:	'Player hits continue on results for Think phase',
  504:	'Player starts an audio clip in Prepare phase',
  505:	'Player hits continue arrow on Prepare phase',
  506:	'Player hits continue on results for Prepare phase',
  507:	'Player chooses opponent\'s attack strategy',
  508:	'Player hits continue arrow after selecting opponent\'s attack',
  509:	'Player selects their own attack strategy',
  510:	'Player selects a sentence piece',
  511:	'Player hits Say It',
  512:	'Player hits continue arrow after their own attack',
  513:	'Opponent counters',
  514:	'Player hits continue arrow after opponent reaction',
  515:	'Game ends (one character hit 0)',
  516:	'Player hits continue arrow after game end',
  517:	'Player hits continue on results panel',
  800:	'Player closes intro panel to start game',
  801:	'Player closes goal panel',
  803:	'Player turns over a Stop And Think Card',
  804:	'Player selects Don\'t Do It',
  805:	'Player selects Do it',
  806:	'Player selects a Priority to Protect',
  807:	'Player hits Go for it!',
  808:	'Player hits Spin button',
  809:	'Player hits Stop Spin button',
  810:	'Player hits continue button after spin',
  811:	'Player hits okay after result panel',
  812:	'Player sees lose panel',
  813:	'Player hits okay after lose panel',
  814:	'Player selects an Opportunity Card type',
  815:	'Player cycles through Opportunity Cards using arrow buttons',
  816:	'Player picks card',
  817:	'Player closes panel that cycles through cards',
  818:	'Player sees win panel',
  900:	'Player closes intro panel to start game',
  901:	'Player selects an NPC',
  902:	'Player selects an NPC fact',
  903:	'Player hits Done button on NPC fact',
  904:	'Player starts drag on NPC',
  905:	'Player drops an NPC in a rank slot',
  906:	'Ready for Invite button appears',
  907:	'Player hits Ready for Invites Button',
  908:	'Invitation appears',
  909:	'Player chooses response to invitation',
  910:	'Player hits continue button after seeing invitation results panel',
  911:	'Player hits continue button on final results panel',
  912:	'Player closes 3 strikes panel.'
}

def finalResults(line):
  resultAsStr = ','.join(line[4:])
  resultAsJSON = json.loads(resultAsStr)
  gameTime = int(resultAsJSON["gameTime"])
  age = resultAsJSON["avatar"]["age"]

  gender = 'male'
  if (resultAsJSON["avatar"]["gender"] == 1):
    gender = 'female'

  skillPts = int(resultAsJSON["avatar"]["skillPoints"])
  miniGameStars = {'0': 0, '1': 0, '2': 0, '3': 0}
  for level in resultAsJSON["avatar"]["levelSaveData"]:
    miniGameStars[str(level["starRating"])] += 1
  return [gameTime, miniGameStars, age, gender, skillPts]

def S4_8Answers(ever, recent):
  weight = None
  ever = int(ever)
  recent = int(recent)
  if ever == 1:
      if recent != 8 and recent != 8888: 
        weight = max(0, 100 - 20*(recent-1))
  elif ever == 2:
        weight = 100
  return weight

def S4_3Answers(ever, recent):
  weight = None
  ever = int(ever)
  recent = int(recent)
  if ever == 1:
      if recent != 3 and recent != 8888: 
        weight = 100*(recent - 1)
  elif ever == 2:
        weight = 100
  return weight

def weighted_average(inputs):
  distribution = []
  weights = []
  for inp in inputs:
    distribution.append(inp[0])
    weights.append(inp[1])
  return round(sum([distribution[i]*weights[i] for i in range(len(distribution))])/sum(weights),2)


overallData = {}

fRead = open('all.txt', "r")

currIpadID = None
logData = None


# Read log data and populate overallData dictionary
for line in fRead:
  csv = line.split(",")
  if (len(csv) == 1 and csv[0] == '\n'):
    continue

  if (csv[0] != currIpadID and len(csv[0]) == 7):
    # New student found 
    if logData:
      overallData[logData['ipadID']] = logData
    currIpadID = csv[0]
    if PRINT_ACTIONS:
      logData = {
        'patientID': None, 
        'ipadID': currIpadID, 
        'age': None, 
        'gender': None, 
        'overallSkillPts': 0, 
        'gameTime': 0, 
        'miniGameStars': {'0': 0, '1': 0, '2': 0, '3': 0}, 
        'actions': []
      }
    else:
      logData = {
        'patientID': None, 
        'ipadID': currIpadID, 
        'age': None, 
        'gender': None, 
        'overallSkillPts': 0, 
        'gameTime': 0, 
        'miniGameStars': {'0': 0, '1': 0, '2': 0, '3': 0}
      }

  if (PRINT_ACTIONS):
    logData['actions'].append(IDs[int(csv[1])])

  if (IDs[int(csv[1])] == 'Player ends session'):
    # Get minigame and gametime data from JSON
    [gameTime, miniGamesStars, age, gender, overallSkillPts] = finalResults(csv)
    # Combine session results with previous ones, if they exist
    logData['gameTime'] = logData['gameTime'] + gameTime
    for rating in miniGamesStars:
      logData['miniGameStars'][str(rating)] += miniGamesStars[str(rating)]
    if (logData['age'] == None):
      logData['age'] = age
    if (logData['gender'] == None):
      logData['gender'] = gender
    logData['overallSkillPts'] = max(logData['overallSkillPts'], overallSkillPts)
  
fRead.close() 
overallData[logData['ipadID']] = logData

# Open subject data to associate ipadID with patientID and header_UID for later analysis
fRead = open('VGAME_SUBJLOC.csv', "r")
for line in fRead:
  csv = line.split(",")
  patientID = csv[0]
  ipadID = csv[9]
  if (len(ipadID) == 7 and ipadID in overallData):
    overallData[ipadID]['patientID'] = patientID

fRead.close()

# Populate experimentalData dictionary with data from S3, S4, and S8
experimentalData = {}

S3 = open('S3Scores.csv', "r")
for line in S3:
  [patientID, headerUID, Phase_Name, Q20, Q21, Q22, Q23] = line.split(",")
  if (Phase_Name == '3 Months'):
    questionWeights = []
    if (Q20 != '6'):
      questionWeights.append(100 - 25 * (int(Q20) - 1))
    if (Q21 != '6'):
      questionWeights.append(100 - 25 * (int(Q21) - 1))
    if (Q22 != '6'):
      questionWeights.append(100 - 25 * (int(Q22) - 1))
    if (Q23 != '6\n'):
      questionWeights.append(25 * (int(Q23) - 1))

    S3Weight = None
    if (len(questionWeights) > 0):
      S3Weight = sum(questionWeights) / len(questionWeights)

    experimentalData[patientID] = {'S3Weight': S3Weight, 'S4Weight': -1, 'S8Weight': -1}
S3.close()

S4 = open('S4Scores.csv', "r")
for line in S4:
  [patientID, Phase_Name, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20] = line.split(",")
  if (Phase_Name == '3 Months'):
    questionWeights = []
    questionWeights.append(S4_8Answers(Q1, Q3))
    questionWeights.append(S4_8Answers(Q4, Q6))
    Q7_Weight = None
    if int(Q7) != 5:
        Q7_Weight = 100 - 25 * (int(Q7)-1)
    questionWeights.append(Q7_Weight)
    questionWeights.append(S4_3Answers(Q8, Q9))
    questionWeights.append(S4_3Answers(Q10, Q11))
    questionWeights.append(S4_3Answers(Q12, Q13))
    questionWeights.append(S4_3Answers(Q14, Q15))
    questionWeights.append(S4_3Answers(Q16, Q17))
    questionWeights.append(S4_3Answers(Q18, Q19))
    questionWeights = [weight for weight in questionWeights if weight is not None]
    
    S4Weight = None
    if (len(questionWeights) > 0):
      S4Weight = sum(questionWeights) / len(questionWeights)

    if (patientID in experimentalData):
      experimentalData[patientID]['S4Weight'] = S4Weight
S4.close()

S8 = open('S8Scores.csv', "r")
for line in S8:
  [patientID, Phase_Name, _, S8Total] = line.split(",")
  if (S8Total == 'S8_Total\n'):
    continue
  if (Phase_Name == '3 Months'):
    S8Total = S8Total.split('\n')[0]
    S8Weight = 100 * (int(S8Total) / 22)
    if (patientID in experimentalData):
      experimentalData[patientID]['S8Weight'] = S8Weight
S8.close()

for key in experimentalData:
  if (experimentalData[key]['S8Weight'] != -1 and experimentalData[key]['S4Weight'] != -1):
    overallWeight = None
    weights = [[experimentalData[key]['S3Weight'], 4], [experimentalData[key]['S4Weight'], 17], [experimentalData[key]['S8Weight'], 22]]
    weightsWithoutNone = []
    weights = [weight for weight in weights if weight[0] is not None]
    if len(weights) > 0:
      overallWeight = weighted_average(weights)
    experimentalData[key]['gradePercent'] = overallWeight

fileWithGrades = open('dataGrades.txt', 'w+')
fileWithoutGrades = open('dataNoGrades.txt', 'w+')
for key in overallData:
  if overallData[key]['patientID'] != None:
    studentData = overallData[key]
    hasGrade = False
    if studentData['patientID'] in experimentalData and 'gradePercent' in experimentalData[studentData['patientID']]:
      studentData['gradePercent'] = experimentalData[studentData['patientID']]['gradePercent']
      grade = None
      if (studentData['gradePercent'] >= 90 and studentData['gradePercent'] <= 100):
        grade = 'A'
      elif (studentData['gradePercent'] >= 80 and studentData['gradePercent'] <= 89):
        grade = 'B'
      elif (studentData['gradePercent'] >= 70 and studentData['gradePercent'] <= 79):
        grade = 'C'
      elif (studentData['gradePercent'] >= 60 and studentData['gradePercent'] <= 69):
        grade = 'D'
      else:
        grade = 'E'
      studentData['grade'] = grade
      hasGrade = True
    jsonStudent = json.dumps(studentData)
    if (hasGrade):
      fileWithGrades.write(jsonStudent+'\n')
    else:
      fileWithoutGrades.write(jsonStudent+'\n')
  else:
    jsonStudent = json.dumps(overallData[key])
    fileWithoutGrades.write(jsonStudent+'\n')

fileWithGrades.close()
fileWithoutGrades.close()