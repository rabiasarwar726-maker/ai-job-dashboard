from fastapi import FastAPI, UploadFile, File
from sentence_transformers import SentenceTransformer, util
import spacy

app = FastAPI()

model = SentenceTransformer('all-MiniLM-L6-v2')
nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    doc = nlp(text)
    return list(set([token.text.lower() for token in doc if token.pos_=="NOUN"]))

@app.get("/")
def home():
    return {"message":"AI Job Dashboard Running"}

@app.post("/match")
async def match(resume:str, job:str):
    emb1 = model.encode(resume, convert_to_tensor=True)
    emb2 = model.encode(job, convert_to_tensor=True)
    score = util.cos_sim(emb1, emb2).item()
    return {"match_score": round(score*100,2)}

@app.post("/skills")
async def skills(resume:str, job:str):
    r_skills = extract_skills(resume)
    j_skills = extract_skills(job)
    missing = list(set(j_skills)-set(r_skills))
    return {"missing_skills": missing}

@app.post("/ats")
async def ats(resume:str):
    score = 0
    if len(resume)>500: score+=25
    if "experience" in resume.lower(): score+=25
    if "skills" in resume.lower(): score+=25
    if "education" in resume.lower(): score+=25
    return {"ATS_score":score}
