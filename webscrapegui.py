import tkinter as tkr
from PIL import Image, ImageTk

import requests
from bs4 import BeautifulSoup
import pprint
import tkinter.font as font
import os
import random
import re
import sys

from datetime import date
today = date.today()
# dd/mm/YY
d1 = today.strftime("%Y-%m-%d")
#print("d1 =", d1)
resp= requests.get("https://www.goal.com/en-us/results/"+d1)
raw_text= BeautifulSoup(resp.content, 'html.parser')
status=raw_text.select('.match-row__data')
comp_name= raw_text.select('.competition-matches')
link_name= raw_text.select('.match-row__link')
#pprint.pprint(comp_name)
#pprint.pprint(link_name)


def teams(data):
    #print(data)
    lst=[ "AFC", "Arsenal", "Aston Villa", "Brighton & Hove Albion", "Burnley","Chelsea" ,"Crystal Palace" ,"Everton" ,"Leicester City" , "Manchester City",
          "Liverpool" ,"Manchester United" , "Newcastle United" , "Norwich City" , "Sheffield United" ,"TottenhamHotspur"  , "Southampton", "Watford" ,"WestHam","Wolverhampton Wanderers"]
    for i in range(len(lst)):
        x=data.find(lst[i])>0
        #print(x)
        if x==True:
            return "Premiere League"
    lst2=["Alavés", "Athletic Bilbao","Atlético Madrid","Barcelona","Celta Vigo","Eibar","Espanyol","Getafe","Granada","Leganés","Levante","Mallorca","Osasuna","Real Betis","Real Madrid", 	
"Real Sociedad","Sevilla","Valencia","Valladolid","Villarreal"]
    for i in range(len(lst2)):
        x=data.find(lst2[i])>0
        #print(x)
        if x==True:
            return "La Liga Santandir"

    
    return "Other League"

def goal(status,link_name):
    num=0
    lst=[]
    lst2=[]
    for i,j in enumerate (status):
        title= status[i].getText()
        
        link= link_name[(i+3) +num ].get('href', None)
        num=num+3
        #print(title)
        new_title = str(title).replace(" ","")
        #print(new_title)
        competition_name=teams(new_title)
        complete_link= "https://www.goal.com" + link
        #print(complete_link)
        #print("\n")
        lst.append({'Match-Info':title, 'Link': complete_link, "Competition Name": competition_name  })
    return lst
        
        
#pprint.pprint(goal(status,link_name))

def goalwebscraper(comp,status):
    lst=[]
    for i,j in enumerate (comp):
        name= comp[i].select('.competition-title')     #get competition name inside the achor tags
        new_name= str(name[i].getText())      # get competition name from achor tags
        #print(name)
        #print(new_name)
        num=0
        lst2=[]
        for i,j in enumerate (status):
            title= status[i].getText()
            
            link= link_name[(i+3) +num ].get('href', None)
            num=num+3
            new_title = str(title).replace(" ","")
            #print(title)
            
            #print(new_title)
            competition_name=teams(new_title)
            complete_link= "https://www.goal.com" + link
            #print(complete_link)
            #print("\n")
            lst.append({'Match-Info':title, 'Link': complete_link, "Competition Name": competition_name  })
    
        #print(lst)
        return lst
#pprint.pprint(goalwebscraper(comp_name,status))



    
    

def test(entry):
    #print("data from entry: ",entry)
    resp2= requests.get("https://www.goal.com/en-us/results/"+entry)
    raw_text2= BeautifulSoup(resp2.content, 'html.parser')
    status2=raw_text2.select('.match-row__data')
    comp_name2= raw_text2.select('.competition-matches')
    link_name2= raw_text2.select('.match-row__link')
    T_area.config(state="normal")
    T_area.delete(1.0,tkr.END)
    T_area.insert(tkr.END,goal(status2,link_name2))
    T_area.config(state="disabled")





bas= tkr.Tk()
canvas=tkr.Canvas(bas, height=700, width=1200)
canvas.pack()

background_image=tkr.PhotoImage(file="clubcfc.png")
bglabel= tkr.Label(bas,image=background_image)
bglabel.place(relwidth=1, relheight=1)

frame=tkr.Frame(bas,bg="#80c1ff", bd=5)
frame.place(relwidth=0.75,relheight=0.15, relx=0.5, rely=0.1, anchor='n')

entry= tkr.Entry(frame, bg='green', font=40, fg="white")
entry.place(relwidth=0.65,relheight=1)

button= tkr.Button(frame, fg="white", bg="purple",text= "Search Match Date", command= lambda: test(entry.get()))
myFont2 = font.Font(family='Helvetica', size=20, weight='bold')
button['font'] = myFont2
button.place(relwidth=0.3,relheight=1, relx=0.7)




frame2=tkr.Frame(bas,bg="#80c1ff", bd=10)
frame2.place(relwidth=0.75,relheight=0.6, relx=0.5, rely=0.3, anchor='n')

label=tkr.Label(frame2, text="Match Information & Score", bg="grey" )
myFont = font.Font(family='Helvetica', size=40, weight='bold')
label['font'] = myFont
label.place(relwidth=1,relheight=0.15)
#S = tkr.Scrollbar(frame2)
T_area=tkr.Text(frame2)
T_area.place(relwidth=1,relheight=0.8, relx=0.5,  rely=0.2, anchor='n')
#S.pack(side=tkr.RIGHT, fill=tkr.Y)
#S.config(command=T_area.yview)
#T_area.config(yscrollcommand=S.set)
T_area=tkr.Text(frame2)
T_area.place(relwidth=1,relheight=0.8, relx=0.5,  rely=0.2, anchor='n')




bas.mainloop()
