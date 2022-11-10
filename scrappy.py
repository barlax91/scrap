import time
import bs4
import pandas
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import sqlite3 as sq
from urllib import request

db_stack = sq.connect("db_stack.db")


list_questions = []
list_votes = []
list_answers = []
list_views = []

for i in range (5):
    time.sleep(1)
    url = "https://stackoverflow.com/questions?tab=newest&page="+str(i)
    request_text = request.urlopen(url).read()
    page = bs4.BeautifulSoup(request_text,'html.parser')
    questions = page.select(".s-post-summary")

    for question in questions:
        q = question.select_one('.s-link').get_text()
        stats = question.select('.s-post-summary--stats')
        list_questions.append(q)
        for sta in stats:
            votes = sta.select('[title~=Score]')
            answers = sta.select('[title~=answer],[title~=answers]')
            views = sta.select('[title~=views]')
            for vote in votes:
                votes_number = vote.select_one('.s-post-summary--stats-item-number').get_text()
                votes_text= vote.select_one('.s-post-summary--stats-item-unit').get_text()
                list_votes.append(int(votes_number))
            for answer in answers:
                answers_number = answer.select_one('.s-post-summary--stats-item-number').get_text()
                answers_text = answer.select_one('.s-post-summary--stats-item-unit').get_text()
                list_answers.append(int(answers_number))
            for view in views:
                views_number = view.select_one('.s-post-summary--stats-item-number').get_text()
                views_text = view.select_one('.s-post-summary--stats-item-unit').get_text()
                list_views.append(int(views_number))
df = pandas.DataFrame.from_dict({"Questions" : list_questions, "Votes" : list_votes, "Answers" : list_answers, "Vues" : list_views})
#print (df)

df.to_sql(name='Stackoverflow',if_exists='replace',con=db_stack)
cursor = db_stack.cursor()
cursor.execute("SELECT * from Stackoverflow")
rows= cursor.fetchall()
for row in rows:
    print(row)
db_stack.close()

plt.figure(figsize=(15,6))
g1 = sb.barplot(x="Questions", y="Vues", data=df,palette="Blues_d")
g1.set(xticklabels=[])
plt.xlabel("Questions", fontsize=16, color="black")
plt.ylabel("Nombre de vues", fontsize=16, color="black")
plt.title("Nombre de vues par questions", fontsize=18, color="black")
g1.set(xlabel=None)
g1.tick_params(bottom=False)

plt.show()

plt.figure(figsize=(15,6))
g2 = sb.barplot(x="Questions", y="Votes", data=df,palette="Blues_d")
g2.set(xticklabels=[])
plt.xlabel("Questions", fontsize=16, color="black")
plt.ylabel("Nombre de Votes", fontsize=16, color="black")
plt.title("Nombre de Votes par questions", fontsize=18, color="black")
g2.set(xlabel=None)
g2.tick_params(bottom=False)

plt.show()

plt.figure(figsize=(15,6))
g3 = sb.barplot(x="Questions", y="Answers", data=df,palette="Blues_d")
g3.set(xticklabels=[])
plt.xlabel("Questions", fontsize=16, color="black")
plt.ylabel("Nombre de Réponses", fontsize=16, color="black")
plt.title("Nombre de Réponses par questions", fontsize=18, color="black")
g3.set(xlabel=None)
g3.tick_params(bottom=False)

plt.show()