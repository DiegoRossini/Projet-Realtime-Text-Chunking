#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importation des librairies nécessaires au pré-traitements des données

import pandas as pd
import nltk
import os
import glob
import time
import re
from nltk.tokenize import word_tokenize


# In[2]:


# Importation du csv "Formulation". Le meme traitement sera effectué sur les csv "Planification" et "Revision"

df = pd.read_table("./csv_formulation.csv", encoding="utf-8",on_bad_lines="skip")


# In[3]:


# On recupère la colonne "burst" qui contient ce qui a été écrit lors de l'expérience de recherche

burst = df["burst"]


# In[4]:


# Visualisation des premières 5 phrases de la colonne "burst"tokenize

burst[0:6]


# In[5]:


# On effece tous les valeurs nulles et qui ne seront pas traitées par la suite

burst_clean = [phrase.strip() for phrase in burst if type(phrase) != float]


# In[6]:


# Création des bigrammes des phrases contenus dans la colonnes "burst" nettoyée des valeurs nulles 

burst_clean = list(nltk.bigrams(burst_clean))


# Unification des bigrammes en une seule phrase sans spécification de l'emplacement de la pause entre les deux
# Ces sont les données qu'on passera au traitement du chunker SEM

burst_clean_no_pause = [(p1,p2) for p1,p2 in burst_clean]
burst_clean_no_pause = [" ".join(phrase) for phrase in burst_clean_no_pause]

 
# Unification des bigrammes en une seule phrase avec spécification de l'emplacement de la pause entre les deux
# Cette variable nous servira plus tard lorsqu'on va insérer les pauses à l'intérieur des données output de SEM

burst_clean_with_pause = [(p1,'@',p2) for p1,p2 in burst_clean]
burst_clean_with_pause = [" ".join(phrase) for phrase in burst_clean_with_pause]


# In[7]:


# Removing white spaces between the pause symbol. This will be usefull when we will look for the correct index of
# al pauses in our bigrams

# On efface l'espace entre le symbole représentant la pause ("@") et ses mots voisine. Cela
# a pour but de faciliter l'insértion de la pause dans la suite du script.

for i,phrase in enumerate(burst_clean_with_pause):
    for idx,char in enumerate(phrase):
        new_phrase = ''
        if char == '@':
            new_phrase = phrase[:idx-1]+'@'+phrase[idx+2:]
            burst_clean_with_pause[i] = new_phrase
            break


# In[8]:


# Visualisation exemple bigrammes avec symbole de pause...

burst_clean_with_pause[:3]


# In[9]:


# .. et sans symbole de pause

burst_clean_no_pause[0:3]


# In[10]:


# This function simply record the index position of all pauses

#def find_pause_idx_in_bigrams(burst_pauses):
 #   pause_idxs = []
  #  for bigram in burst_pauses:
   #     idx_pause = bigram.find('@')
    #    pause_idxs.append(idx_pause)
            
    #return pause_idxs


# In[11]:


#pauses_idx_list = find_pause_idx_in_bigrams(burst_clean_with_pause)


# In[12]:


#with open('../Traitement_textes_finaux/TEST_burst_no_pause_for_SEM_formulation.txt','w') as f:
 #   for bigram in burst_clean_no_pause:
  #      f.write("'")
   #     f.write(bigram)
    #    f.write("'")
  #      f.write('\n')
#f.close()


# In[13]:


# Importation de la librairie "Selenium" et des fonctions qui permettent de passer au chunker SEM en ligne chaque 
# bigramme.

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.firefox.options import Options


# In[14]:


# Cette fonction écrit ligne par ligne sur un document texte l'output du chunker SEM

def write_chunks_from_bigrams_burst(burst_clean_no_pause):
    
    # On fait en sorte qu'aucune fenetre de navigation n'apparaisse
    options = Options()
    options.headless = True
    
    # On fait une boucle sur chaque bigramme contenu dans "burst_clean_no_pause" et on prend en considération que les
    # bigrammes qui contiennent du texte
    for idx,bigram in enumerate(burst_clean_no_pause):
        bigram = str(bigram)
        if bigram == " ":
            with open("../Selenium_SEM_output//bigram_chunks_complete_formulation","a+", encoding="utf-8") as file:
                file.write("\n")
            file.close()
            continue
            
        else:
            # On ouvre le browser FireFox
            driver = webdriver.Firefox(options=options)
            
            # On navige vers le site de SEM
            url = "https://apps.lattice.cnrs.fr/sem/index"
            driver.get(url)
            driver.implicitly_wait(5)
            
            # On accepte les cookies et les fenetres de popup
            driver.switch_to.alert.dismiss()
            time.sleep(2)
            time.sleep(1)
            
            # On écrit le bigrammes sur la zone de texte et on lance la division en chunks
            driver.find_element(By.XPATH,"//textarea").send_keys(bigram)
            time.sleep(1)
            driver.find_element(By.ID,"inlineCheckbox2").click()
            time.sleep(1)
            driver.find_element(By.XPATH,"//button").click()
            time.sleep(1)
            driver.switch_to.alert.dismiss()
            time.sleep(1)
            driver.find_element(By.XPATH,"//label[contains(.,'Chunking')]").click()
            time.sleep(1)
            
            # On telecharge le fichier texte conténant le bigramme divisé en chunk
            driver.find_element(By.XPATH,"//a[contains(.,'⬇ text')]").click()

            
            with open("../Selenium_SEM_output//bigram_chunks_complete_formulation","a+", encoding="utf-8") as file:
                
                # On ouvre le fichier texte télécharge dupis le site de SEM contenant le bigramme, on écrit son contenu
                # sur un fichier appelé "bigram_chunks_complete_" et on éfface le fichier téléchargé auparavant
                file_path = glob.glob("/home/diego/Downloads/sem_*.text")
                file_path = str(file_path)[2:len(str(file_path))-2]
                with open(file_path,"r",encoding="utf-8") as f:
                    unique_line = ""
                    for line in f.readlines():
                        line = line.strip('\n')
                        unique_line = unique_line+" "+line
                file.write(unique_line)
                file.write("\n")
                os.remove(file_path)
            file.close()
            driver.close()


# In[15]:


# On lance notre focntion sur nos bigrammes

write_chunks_from_bigrams_burst(burst_clean_no_pause)


# In[16]:


# Creation d'une liste de 3 éléments avec structure "mot_avant - pause@ - mot_après" pour ajouter la position corrécte de
# la pause dans le document texte avec les bigrammes chunks

pauses_entre_mot = []
for bigram in burst_clean_with_pause:
    txt = bigram
    x = re.search(f"(([a-zA-Z]|à|â|ä|é|è|ê|ë|î|ï|ô|ö|ù|û|ü|ÿ|ç|À|Â|Ä|Ç|É|È|Ê|Ë|Î|Ï|Ô|Ö|Ù|Û|Ü|Ÿ)*|[^\s\w\d])@(([a-zA-Z]|à|â|ä|é|è|ê|ë|î|ï|ô|ö|ù|û|ü|ÿ|ç|À|Â|Ä|Ç|É|È|Ê|Ë|Î|Ï|Ô|Ö|Ù|Û|Ü|Ÿ)*|[^\s\w\d])", txt)
    x = x[0]
    x = word_tokenize(x)
    if len(x) == 1:
        x.insert(0,"^")
        x.append("$")
    elif len(x) == 2:
        if x[1] == "@":
            x.append("$")
        elif x[0] == "@":
            x.insert(0,"^")
    pauses_entre_mot.append(x)


# In[ ]:


# Insertion du symbole de pause "@" entre le bigrammes divisés en chunks. Les données bruité sont traitées avec un
# enchainement de "try" "except"

with open("../Selenium_SEM_output/bigram_chunks_complete_formulation","r",encoding="utf-8") as f:
    with open("../Selenium_SEM_output/bigram_chunks_complete_formulation_with_pauses","a+",encoding="utf-8") as final_file:
        for idx,line in enumerate(f.readlines()):
            mot_1 = pauses_entre_mot[idx][0]
            mot_2 = pauses_entre_mot[idx][2]  
            try:
                match_1 = re.search(mot_1,line)
                match_2 = re.search(mot_2,line)
                set_pause = line[match_1.span()[1]:match_2.span()[0]]
                between_chunks = re.search("\)\s\(",set_pause)
            except:
                try:
                    match_1 = re.search("\\"+mot_1,line)
                    match_2 = re.search(mot_2,line)
                    set_pause = line[match_1.span()[1]:match_2.span()[0]]
                    between_chunks = re.search("\)\s\(",set_pause)
                except:
                    match_1 = re.search('\"',line)
                    match_2 = re.search(mot_2,line)
                    set_pause = line[match_1.span()[1]:match_2.span()[0]]
                    between_chunks = re.search("\)\s\(",set_pause)
        
        
            if between_chunks is None:
                try:
                    match_1 = re.search(mot_1,line)
                    match_2 = re.search(mot_2,line)
                    set_pause = line[match_1.span()[1]:match_2.span()[0]+match_1.span()[0]]
                    between_chunks = re.search("\)\s\(",set_pause)
                except:
                    try:
                        match_1 = re.search("\\"+mot_1,line)
                        match_2 = re.search(mot_2,line)
                        set_pause = line[match_1.span()[1]:match_2.span()[0]+match_1.span()[0]]
                        between_chunks = re.search("\)\s\(",set_pause)
                    except:
                        match_1 = re.search('\"',line)
                        match_2 = re.search(mot_2,line)
                        set_pause = line[match_1.span()[1]:match_2.span()[0]+match_1.span()[0]]
                        between_chunks = re.search("\)\s\(",set_pause)
                if between_chunks is None:
                    final_file.write(line[:match_1.span()[1]])
                    final_file.write('@')
                    final_file.write(line[match_1.span()[1]:])
                elif between_chunks[0] == ') (':
                    final_file.write(line[:match_1.span()[1]+1])
                    final_file.write(')@(')
                    final_file.write(line[match_2.span()[0]-3:])
            elif between_chunks[0] == ') (':
                final_file.write(line[:match_1.span()[1]+1])
                final_file.write(')@(')
                final_file.write(line[match_2.span()[0]-3:])


# In[ ]:


# La chunk "Adp" a été coupé en "dP" lors du traitement précédent. On rectifie ce petit erreur.

with open("../Selenium_SEM_output/bigram_chunks_complete_formulation_with_pauses","r",encoding="utf-8") as f:
    with open("../Selenium_SEM_output/bigram_chunks_complete_formulation_with_pauses_2","a+",encoding="utf-8") as final_file:
        i = 0
        for idx,line in enumerate(f.readlines()):
            if line == "\n":
                continue
            else:
                if '@(dP' in line:
                    idx_pause = line.find('@')
                    line = line[:idx_pause]+'@(AdP'+line[idx_pause+4:]
                    final_file.write(line)
                else:
                    final_file.write(line)

