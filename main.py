from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from flask import Flask, redirect, session, render_template, url_for
from authlib.integrations.flask_client import OAuth

# model setup

load_dotenv()
api_key: str  = os.getenv('key')
model: str     = "deepseek-r1-distill-llama-70b"
deepseek      = ChatGroq(api_key=api_key, model_name=model)

# Getting only result from the model

parser         = StrOutputParser()
deepseek_chain = deepseek | parser
# result: str = deepseek_chain.invoke('what is a bot')
# print(result)


# Loading and Splitting data in chunks
loader = TextLoader('data.txt', encoding='utf-8')
data   = loader.load()
# print(data)


# Define the function of the chatbot
template = """
You are AI-powered chatbot designed to provide 
information and assistance for people
based on the context provided to you only.    
Don't in any way make things up.   
Context:{context}
Question:{question}
"""

question: str = 'What is pdf parsing'
template = template.format(context=data, question=question)
# print(template)

answer = deepseek_chain.invoke(template)
print(answer)


# Auth0 setup
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET')

app.config['AUTH0_CLIENT_ID']     = os.getenv('AUTH0_CLIENT_ID')
app.config['AUTH0_CLIENT_SECRET'] = os.getenv('AUTH0_CLIENT_SECRET')
app.config['AUTH0_DOMAIN']        = os.getenv('AUTH0_DOMAIN')
app.config['AUTH0_CALLBACK_URL']  = os.getenv('AUTH0_CALLBACK_URL')
app.config['AUTH0_AUDIENCE']      = f"https://{app.config['AUTH0_DOMAIN']}/userinfo"

oauth = OAuth(app)
oauth.register(
    'auth0',
    client_id=app.config['AUTH0_CLIENT_ID'],
    client_secret=app.config['AUTH0_CLIENT_SECRET'],
    server_metadata_url=f"https://{app.config['AUTH0_DOMAIN']}/.well-known/openid-configuration",
    client_kwargs={'scope': 'openid profile email'}
)

# Auth0 routes
@app.route('/')
def home():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/login')
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=app.config['AUTH0_CALLBACK_URL'],
        scope='openid profile email',
        prompt='login'
    )

@app.route('/callback')
def callback():
    token = oauth.auth0.authorize_access_token()
    session['user'] = token.get('userinfo') or token
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
