import openai
import os 
import json 
import threading

from flask_api import FlaskAPI
from flask import request 
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("openai_api") 
my_bearer_token = os.getenv("api_key")


app = FlaskAPI(__name__)


def auth():
    given_token = request.headers.get("Authorization")
    if given_token == None:
        return "Access denied. No token given"
    given_token = given_token.split()[1]
    if given_token != my_bearer_token:
        return "Access denied. Wrong bearer token given"
    
    return None


@app.route("/")
def main():
    return """
            If you want to rephrase text you can call <b>/Rephrase</b> api with json like this: </br></br>
            {'text':'text that you want to rephrase',</br>
             'number_of_variants': 2} </br></br>
             this will rephrase the text in 2 difference ways</br></br></br>
               
            If you want to generate some text about your company you can call the <b>/Generate</b> api with json like this</br>
            </br>{"description":"a description of your company", </br>
             "sections":{</br>
                "about": {"title": 2, "description": 1}, 
               ... }}</br></br>
            This will create an <i>about</i> page <i>title</i> and <i>description</i> about a company based on <i>description</i>
            """
        

    
    
@app.route("/Rephrase")
def Rephrase():
    
    auth_rez = auth()
    if  auth_rez != None:
        return  auth_rez
        

    text = request.data.get("text")
    try:
        number_of_variants = int(request.data.get("number_of_variants"))
    except ValueError as e:
        return "'number_of_variants' cannot be converted to number"
    
    if text == None or number_of_variants == None:
        return "Missing values"
    
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            n=number_of_variants,
            messages=[
                {"role":"user", "content":f"rephrase this '{text}'"}
            ]
        )
    except Exception as e:
        return f"And error has happened with open ai servers: </br> {str(e)}"   
    
    
    rephrased_text = []
    for choice in response["choices"]:
        
        c = choice["message"]["content"]
        c = c.strip("\'")
        c = c.strip("\"")
        rephrased_text.append(c)
    
    return  str(rephrased_text)
    
    
    
@app.route("/Generate")
def Generate():
    
    auth_rez = auth()
    if  auth_rez != None:
        return  auth_rez

    description = request.data.get("description") # description of the business 
    
    sections = request.data.get("sections")
    if type(sections) != dict:
        try:
            sections = json.loads(sections) # title:num_of_var, description:num_of_var
        except json.decoder.JSONDecodeError as e:
            return "invalid json provided"
        
    if description == None or sections == None:
        return "Missing value"
    
    for cat in sections.keys():
        for sub_cat in sections[cat].keys():
            if type(sections[cat][sub_cat]) != int:
                return "number of variants is not a number "
    
    output = {}
    
    thread_list = []
    for category in sections.keys():
        t = threading.Thread(target=make_call, args=(description, category, sections[category], output))
        t.start()
        thread_list.append(t)
    
    for t in thread_list:
        t.join()
        
    return json.dumps(output)
    
def make_call(description, category,  section, output):
    
    output[category] = {}
    
    for sub_category in section.keys():
        try:
            r = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                n=section[sub_category],
                messages=[
                {"role":"user",
                "content":f"""make a {sub_category} for {category} page for a business that is 
                described as {description}."""},
                
                {"role":"user",
                "content" : 
                """
                Use these rules for this task:
                1. do not create a name for the company unless you are given one. 
                2. do not say any thing about the location of the business unless it is in the description.
                3. say under 100 words for the response.                     
                4. be engaging and alluring
                """}
            ]
            )
        except Exception as e:
            return f'An error has occurred with open ai servers: </br> {str(e)}'

        variants = []
        for choice in r["choices"]:
            c = choice["message"]["content"]
            c = c.strip("\'")
            c = c.strip("\"")
            variants.append(c)
    
        output[category][sub_category] = variants        
    


if __name__ == "__main__":
    # app.run( debug=True)
    app.run(host="0.0.0.0", port=5000, debug=False)