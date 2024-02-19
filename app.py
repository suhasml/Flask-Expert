# from flask import Flask, render_template, request, redirect, url_for, flash
# import requests
# import pickle  
# import os
# from langchain_community.llms import OpenAI
# from langchain.chains import RetrievalQAWithSourcesChain
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.document_loaders import UnstructuredURLLoader
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
# #from env import OPENAI_API_KEY  


# app = Flask(__name__)
# app.secret_key = 'supersecretkey'

# with open('flask_docs_db2.pkl', 'rb') as f:
#     vector_store = pickle.load(f)

# llm = OpenAI(temperature=0.9, max_tokens=100, openai_api_key=os.OPENAI_API_KEY, model="gpt-3.5-turbo-instruct")

# # Route for the homepage
# @app.route('/')
# def home():
#     return render_template('home.html')

# # Route for the login page
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # Handle login form submission
#         email = request.form['email']
#         password = request.form['password']

#         #send it to the api to check if the user exists and the password is correct then redirect to the home page
#         url = 'https://usersdb-1-z1806283.deta.app/login'
#        #data should be in json format
#         data = {'email': email, 'password': password}
#         response = requests.post(url, json=data)
#         if response.status_code == 200:
#             return redirect(url_for('ask'))
#         else:
#             #a pop up message should appear saying that the email or password is incorrect
#             flash('Email or password is incorrect', 'error')
#     return render_template('login.html')

# # Route for the signup page
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         # Handle signup form submission
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']
       
#         #send it to the api to check if the user exists and the password is correct then redirect to the home page
#         url = 'https://usersdb-1-z1806283.deta.app/signup'
#          #data should be in json format
#         data = {'name': name, 'email': email, 'password': password}
#         response = requests.post(url, json=data)
#         if response.status_code == 201:
#             return redirect(url_for('ask'))
#         else:
#             flash('Email already exists', 'error')
#     return render_template('signup.html')

# @app.route('/ask', methods=['GET', 'POST'])
# def ask():
#     if request.method == 'POST':
#         # Handle form submission
#         question = request.form['question']
#         # Save the question to your database or perform any other necessary actions
#         chain = RetrievalQAWithSourcesChain.from_llm(
#             llm = llm,
#             retriever= vector_store.as_retriever(),
#         )

#         result = chain(
#             {"question": question},
#             return_only_outputs=True
#         )
#         answer = result['answer'] + '\nSources: ' + ''.join(result['sources'])
#         return render_template('main.html', question=question, answer=answer)

#     return render_template('main.html')


# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import pickle  
import os
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.document_loaders import UnstructuredURLLoader
from langchain_community.document_loaders import UnstructuredURLLoader
# from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS

from env import OPENAI_API_KEY

app = Flask(__name__)
app.secret_key = 'supersecretkey'

with open('flask_docs_db2.pkl', 'rb') as f:
    vector_store = pickle.load(f)

llm = OpenAI(temperature=0.9, max_tokens=100, openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo-instruct")

# Route for the homepage
@app.route('/')
def home():
    return render_template('home.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form submission
        email = request.form['email']
        password = request.form['password']

        #send it to the api to check if the user exists and the password is correct then redirect to the home page
        url = 'https://usersdb-1-z1806283.deta.app/login'
       #data should be in json format
        data = {'email': email, 'password': password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return redirect(url_for('ask'))
        else:
            #a pop up message should appear saying that the email or password is incorrect
            flash('Email or password is incorrect', 'error')
    return render_template('login.html')

# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle signup form submission
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
       
        #send it to the api to check if the user exists and the password is correct then redirect to the home page
        url = 'https://usersdb-1-z1806283.deta.app/signup'
         #data should be in json format
        data = {'name': name, 'email': email, 'password': password}
        response = requests.post(url, json=data)
        if response.status_code == 201:
            return redirect(url_for('ask'))
        else:
            flash('Email already exists', 'error')
    return render_template('signup.html')

@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        # Handle form submission
        question = request.form['question']
        # Save the question to your database or perform any other necessary actions
        chain = RetrievalQAWithSourcesChain.from_llm(
            llm = llm,
            retriever= vector_store.as_retriever(),
        )

        result = chain(
            {"question": question},
            return_only_outputs=True
        )
        answer = result['answer'] + '\nSources: ' + ''.join(result['sources'])
        return render_template('main.html', question=question, answer=answer)

    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)
