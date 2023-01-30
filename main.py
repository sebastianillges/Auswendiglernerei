import os
import textwrap
import PySimpleGUI as sgui
import random
import csv
import numpy as np


def getNumberOfLines(source):
    with open(source) as f:
        count = sum(1 for _ in f)
    return count
def getLine(number, source):
    with open(source, "r", encoding='utf-8') as file:
        for line in file:
            if line.startswith(str(number) + "."):
                output = line[len(str(number)) + 2:len(line) - 1]
    return output
def getLines(source):
    number = 1
    lines = [""] * sum(1 for line in open(source))
    with open(source, "r", encoding='utf-8') as file:
        for line in file:
            if line.startswith(str(number) + "."):
                lines[number - 1] += line[len(str(number)) + 2:len(line) - 1]
                number += 1
    return lines

def insert_newlines(string, every=30):
    lines = []
    for i in range(0, len(string), every):
        lines.append(string[i:i + every])
    return '\n'.join(lines)

questionFile = "ITSECq.txt"                                                                                                  # File mit den Fragen
answerFile = "ITSECa.txt"                                                                                                    # File mit den Antworten
questions = getLines(questionFile)                                                                                      # Array mit den Fragen
print(str(len(questions)) + " questions")
answers = getLines(answerFile)                                                                                          # Array mit den Antworten
print(str(len(answers)) + " answers")

def loadScore():
    return np.genfromtxt(open("scores.csv"), delimiter=',', dtype=int, usecols=1)

def safeScore():
    resetScore()
    index = np.linspace(1, len(questions), num=len(questions))
    scoreFile = open("scores.csv", "w", encoding='UTF8', newline='')
    writer = csv.writer(scoreFile)
    for i in range(len(questions)):
        writer.writerow([int(index[i]), score[i]])
    scoreFile.close()

def updateScore(lineNum):
    return

def resetScore():
    index = np.linspace(1, len(questions), num=len(questions))
    os.remove("scores.csv")
    print("Score reset")
    scoreFile = open("scores.csv", "w", encoding='UTF8', newline='')
    writer = csv.writer(scoreFile)
    for i in range(len(questions)):
        writer.writerow([int(index[i]), int(0)])
    scoreFile.close()

def getNewRand():
    rand = random.randint(0, len(questions) - 1)
    avgScore = np.mean(score)
    while score[rand] >= avgScore and avgScore != 0:
        rand = random.randint(0, len(questions) - 1)
    return rand

score = loadScore()                                                                                                     # Lade den bisherigen Fragenscore in das Programm
scoreAvg = np.mean(score)                                                                                               # Durchschnitt aller Fragenscores

for i in range(1, getNumberOfLines(questionFile)):                                                                      # Textumbruch für zu lange Fragen und Antworten
    questions[i] = textwrap.fill(questions[i], 50)
    answers[i] = textwrap.fill(answers[i], 50)

randomNumber = random.randint(1, getNumberOfLines(questionFile) - 2)                                                    # Erstellen einer Zufallszahl

showing = 0

sgui.theme('Black')
contents = [
    [sgui.Text(questions[randomNumber] + '\n', font=('Helvetica', 18), key='q')],
    [sgui.Text('' + '\n', font=('Helvetica', 18), key='a')],
    [sgui.Button('Antwort anzeigen', font=('Helvetica', 18), key='show')],
    [sgui.Button('Gewusst', font=('Helvetica', 18), key='p'), sgui.Button('Nicht gewusst', font=('Helvetica', 18), key='kp')],
    [sgui.Text('\n')],
    [sgui.Text('\n')],
    [sgui.Text('\n')],
    [sgui.Text('\n')],
    [sgui.Button('Score zurücksetzen', font=('Helvetica', 18), key='reset')]
]

layout = [[sgui.VPush()],
          [sgui.Push(), sgui.Column(contents, element_justification='c'), sgui.Push()],
          [sgui.VPush()]]
window = sgui.Window('Fragen lern Tool', layout, size=(800, 800))

while True:
    event, values = window.read()
    if event == sgui.WIN_CLOSED:
        break
    if event == 'p' and showing:
        showing = 0
        score[randomNumber] += 1
        scoreAvg = np.mean(score)
        randomNumber = getNewRand()
        currentScore = score[randomNumber]
        if currentScore == scoreAvg:
            color = 'White'
        elif currentScore < scoreAvg:
            color = 'Red'
        else:
            color = 'Green'
        window['q'].update(questions[randomNumber] + '\n', text_color=color)
        window['a'].update('' + '\n')
    if event == 'kp' and showing:
        showing = 0
        randomNumber = getNewRand()
        currentScore = score[randomNumber]
        scoreAvg = np.mean(score)
        if currentScore == scoreAvg or currentScore == 0:
            color = 'White'
        elif scoreAvg > currentScore > 0:
            color = 'Red'
        else:
            color = 'Green'
        window['q'].update(questions[randomNumber] + '\n', text_color=color)
        window['a'].update('' + '\n')
    if event == 'show':
        showing = 1
        window['a'].update(answers[randomNumber] + '\n')
    if event == 'reset':
        resetScore()
        score = loadScore()
safeScore()
window.close()