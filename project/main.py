from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, Cookie
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

# Google API
import os
import google.generativeai as genai


app = FastAPI()
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],allow_methods=["*"],allow_headers=["*"],
                   )

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"),name="static")


@app.get('/signup',response_class=HTMLResponse)
def signup_page(request:Request):
    return templates.TemplateResponse("signup.html",{"request":request})

# Create an account 
@app.post('/signup')
def signup(username:str=Form(...), age:int=Form(...), gender:str=Form(...),password:str=Form(...), height:float=Form(...), weight:float=Form(...)):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        password TEXT NOT NULL,
        height REAL NOT NULL,
        weight  REAL NOT NULL                                       
               )
    ''')
    cursor.execute('''
        INSERT INTO Users (username, age, gender,password,height, weight) VALUES (?,?,?,?,?,?)

''',(username, age, gender,password,height, weight))
    conn.commit()
    cursor.execute("""SELECT id FROM users WHERE username=?""",(username,))
    user_id=cursor.fetchone()
    conn.close()
    if user_id!=None:
        return RedirectResponse(url="/login", status_code=303)
    else:
        return {"message":"An error occurred, try again"}

# Log in 

@app.get('/login',response_class=HTMLResponse)
def login_page(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})


@app.post('/login')
def login(username:str=Form(...), password:str=Form(...)):
    conn = sqlite3.connect('users.db')
    conn.row_factory=sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM users WHERE username=?""",(username,))
    user_data=cursor.fetchone()
    conn.close()
    if user_data==None:
        return {"result":"User not found"}
    elif user_data['password']==password:
        response =RedirectResponse(url="/", status_code=303)
        response.set_cookie("username",user_data['username'])
        response.set_cookie("height",user_data['height'])
        response.set_cookie("weight",user_data['weight'])
        return response
    else:
        return {"result":"Incorrect password"} 
 
# Home page 

# notes
def bmi_calc(weight,height):
    return float("{:.2f}".format(weight/(height**2)))


def bmi_note(bmi):
    if bmi < 18.5:
        return "Underweight: You are below the normal weight range. Consider consulting a healthcare provider to ensure you're maintaining a healthy diet."
    elif 18.5 <= bmi < 24.9:
        return "Normal weight: Your weight is within the healthy range. Keep up the good work with a balanced diet and regular physical activity."
    elif 25 <= bmi < 29.9:
        return "Overweight: You are above the normal weight range. Consider adopting a healthier lifestyle with a balanced diet and regular exercise."
    elif 30 <= bmi < 34.9:
        return "Obesity (Class 1): You are in the obesity range. It is advisable to consult a healthcare provider for guidance on weight management."
    elif 35 <= bmi < 39.9:
        return "Obesity (Class 2): Your BMI indicates higher obesity. Seeking medical advice for a personalized health plan is recommended."
    else:
        return "Obesity (Class 3): You are in the severe obesity range. It's important to consult with a healthcare provider for appropriate interventions."



@app.post('/')
def home_page(request:Request,message:str=Form(...), api_key="TOKEN"):
    genai.configure(api_key=api_key)
    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-8b",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
    history=[]
    )
    height=float(request.cookies.get("height"))
    weight=float(request.cookies.get("weight"))
    bmi=bmi_calc(weight,height)
    username=request.cookies.get("username")
    message = "Iam "+username+message
    if "bmi" in message or "BMI" in message or "Bmi" in message:
        message = "my bmi is "+str(bmi)+message
    try:
        response = chat_session.send_message(message)
        response_dict=response.to_dict()
        generated_text = response_dict['candidates'][0]['content']['parts'][0]['text']
        res=""
        for i in generated_text:
            if i!="\n":
                res+=i
            else:
                i+="<br>"
    except Exception as e:
        res="Sorry, it seems that your message is long or there was a connection error."
    finally:
        return {"response":res}

    

@app.get('/',response_class=HTMLResponse)
def home_page(request:Request):
    username=request.cookies.get("username")
    if username:  
        height=float(request.cookies.get("height"))
        weight=float(request.cookies.get("weight"))
        bmi=bmi_calc(weight,height)
        note=bmi_note(float(bmi))
        return templates.TemplateResponse("home.html",{"request":request,"username":username,"height":height,"weight":weight,"bmi":bmi, "note":note})
    #Login is required
    else:
        return RedirectResponse(url="/login", status_code=303)

