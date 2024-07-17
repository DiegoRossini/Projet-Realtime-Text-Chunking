# Prendre en compte startPos et endPos quand reproduction
# tjrs des problemes, planification crash

# ---SETUP---

from os import system

system("title En attente d'input...")
filesToOpen=input("[97mEntrez le chemin des fichiers .csv à utiliser séparés d'un espace ([96mne pas mettre l'extension, ne pas mettre 'csv_' devant[97m) :\n\n→ [90m").split(" ")
system("title Travail en cours...")
for fileToOpen in filesToOpen:
    try:
        fileInput=open(f"csv_{fileToOpen}.csv","r",encoding="utf-8").readlines()
    except:
        print(f"\n[91mERREUR : Le fichier {fileToOpen} n'a pas pu être ouvert.")
        continue
    for i,j in enumerate(fileInput):
        fileInput[i]=j.replace("\n","").split("\t")
    charBurstIndex=fileInput[0].index("charBurst")
    startPosIndex=fileInput.pop(0).index("startPos")

# ---TREATMENT---

    h=[]

    outputLines=[]
    outputLine=[]
    outputIndex=0
    for i,j in enumerate(fileInput):
        if j[charBurstIndex][0]=="\"" and j[charBurstIndex][len(j[charBurstIndex])-1]=="\"":
            fileInput[i][charBurstIndex]=j[charBurstIndex][1:len(j[charBurstIndex])-1].replace("\"\"","\"")
        h.append(fileInput[i][charBurstIndex])
    for i in fileInput:
        toAddIndex=0
        for j in i[charBurstIndex]:
            if j!="⌫":
                outputLine.insert(int(i[startPosIndex])+toAddIndex,j)
                toAddIndex+=1
            else:
                outputLine.pop(int(i[startPosIndex])-1+toAddIndex)
                toAddIndex-=1
            input("[97m"+"".join(outputLine))#DEBUG Juste pour voir la ligne qu'on a jusqu'ici
        outputLines.append(outputLine)
        outputLine=outputLines[outputIndex][:]
        outputIndex+=1
    
    fileOutput=open(f"output_{fileToOpen}.csv","w",encoding="utf-8")
    fileOutput.write("charBurst\twholeTextTyped\n")
    for i,j in zip(fileInput,outputLines):
        fileOutput.write(f"{i[charBurstIndex]}\t{''.join(j).replace('␣',' ')}\n")
    fileOutput.close()

system("title Travail terminé !")
input("\n[92mTravail terminé !")
