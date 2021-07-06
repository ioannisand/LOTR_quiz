from quote import RandomQuote, characters_list
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import random
import os
from dotenv import load_dotenv
import gunicorn


# just so i can use the .env file to hide secret key
load_dotenv()

# initializing app and applying flask bootstrap
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("secret_key")
Bootstrap(app)

#LOTR CHAR LIST
characters_list = characters_list


score = 0

'''function to initialize a form (did it this way because setattr() didn't work with FlaskForm instances and if i put other attributes
(other than Form Fields) in the constructor, then the field attributes couldnt call them (putting the field attributes in the constructor didnt work either)
i guess it has to do with how WTForms are built?'''
def generate_new_form():
    class QuotesForm(FlaskForm):
        quote = RandomQuote()
        text = quote.quote_text
        right_answer = quote.character_name
        all_answers = [random.choice(characters_list) for i in range(3)]
        all_answers.append(right_answer)
        random.shuffle(all_answers)
        radio = RadioField(label=text, choices=all_answers, validators=[DataRequired()])
        submit = SubmitField("Submit")
    new_form = QuotesForm()

    return new_form

# initializing 3 variables to hold each new QuestionForm object, its quote and the right answer respectively
a=None
b=None
c=None

# add one to the score
def score_plus_one():
    global score
    score +=1




# homepage
@app.route('/')
def homepage():
    global score
    score = 0
    return render_template("index.html", number=score ,initialform=generate_new_form())



#
@app.route('/question/<int:num>', methods=["GET", "POST"])
def show_question(num):
    global a
    global b
    global c

    if score == 0 and request.method == "GET":

        a = generate_new_form()
        b = a.text
        c = a.right_answer

    if request.method == "POST":

        if request.form["radio"] == c:
            score_plus_one()
            a = generate_new_form()
            b = a.text
            c = a.right_answer
            return redirect(url_for("show_question", num=score))
        else:
            return redirect(url_for("end", score=score))


    return render_template("question.html", number=score, forma=a, question=b, answer=c)

@app.route('/end/<int:score>')
def end(score):
    return render_template("end.html", score=score)




if __name__ == '__main__':
    app.run()