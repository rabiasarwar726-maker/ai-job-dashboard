from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

app = FastAPI(title="AI Job Dashboard")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["allow_origins=["https://genuine-macaron-0024a6.netlify.app"]
"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"message": "AI Job Dashboard running 🚀"}

# ---------------- HELPER ----------------
def detect_description_column(df):
    for col in df.columns:
        if "desc" in col.lower() or "description" in col.lower():
            return col
    return None

# ---------------- UPLOAD ----------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        df = pd.read_csv(io.StringIO(contents.decode()))
    except Exception as e:
        return {"error": f"CSV read failed: {str(e)}"}

    return {
        "filename": file.filename,
        "rows": len(df),
        "columns": list(df.columns),
        "preview": df.head().to_dict(orient="records")
    }

# ---------------- ANALYZE ----------------
@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        df = pd.read_csv(io.StringIO(contents.decode()))
    except Exception as e:
        return {"error": f"CSV read failed: {str(e)}"}

    desc_col = detect_description_column(df)
    if not desc_col:
        return {"error": "CSV must contain description column"}

    # Top skills
    vectorizer = CountVectorizer(stop_words="english")
    X = vectorizer.fit_transform(df[desc_col].astype(str))

    skills = pd.DataFrame({
        "skill": vectorizer.get_feature_names_out(),
        "count": X.toarray().sum(axis=0)
    })

    top_skills = skills.sort_values("count", ascending=False).head(20).to_dict(orient="records")

    # Job categories
    categories = []
    for text in df[desc_col]:
        text = str(text).lower()
        if any(word in text for word in ["ai", "machine learning", "data"]):
            categories.append("AI / Data Science")
        elif any(word in text for word in ["frontend", "backend", "web"]):
            categories.append("Web Development")
        elif any(word in text for word in ["cloud", "devops", "docker"]):
            categories.append("DevOps / Cloud")
        else:
            categories.append("Other")

    df["category"] = categories

    return {
        "top_skills": top_skills,
        "job_category_counts": df["category"].value_counts().to_dict(),
        "preview": df.head().to_dict(orient="records")
    }

# ---------------- RECOMMEND ----------------
@app.post("/recommend")
async def recommend_jobs(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        df = pd.read_csv(io.StringIO(contents.decode()))
    except Exception as e:
        return {"error": f"CSV read failed: {str(e)}"}

    desc_col = detect_description_column(df)
    if not desc_col:
        return {"error": "CSV must contain description column"}

    # Role mapping
    role_keywords = {
        "Data Scientist": ["data", "machine learning", "analytics"],
        "AI Engineer": ["ai", "deep learning", "pytorch", "tensorflow"],
        "Web Developer": ["html", "css", "javascript", "react", "frontend", "backend"],
        "DevOps Engineer": ["docker", "kubernetes", "cloud", "aws"],
        "Software Engineer": ["java", "python", "c++", "software"]
    }

    recommendations = []
    for text in df[desc_col]:
        text = str(text).lower()
        matched = [role for role, keywords in role_keywords.items() if any(k in text for k in keywords)]
        recommendations.append(matched if matched else ["Other"])

    df["recommended_roles"] = recommendations

    all_roles = [r for sub in recommendations for r in sub]
    role_counts = dict(Counter(all_roles))

    return {
        "role_counts": role_counts,
        "preview": df.head().to_dict(orient="records")
    }

# ---------------- MATCH RESUME ----------------
@app.post("/match")
async def match_resume(resume: UploadFile = File(...), jobs: UploadFile = File(...)):
    # read resume
    resume_text = (await resume.read()).decode(errors="ignore")

    # read jobs CSV
    contents = await jobs.read()
    try:
        df = pd.read_csv(io.StringIO(contents.decode()))
    except Exception as e:
        return {"error": f"Jobs CSV read failed: {str(e)}"}

    desc_col = detect_description_column(df)
    if not desc_col:
        return {"error": "Jobs CSV must contain description column"}

    # Vectorize
    texts = [resume_text] + df[desc_col].astype(str).tolist()
    vectorizer = CountVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(texts)

    # Cosine similarity
    similarity = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    df["match_score"] = similarity

    top_jobs = df.sort_values("match_score", ascending=False).head(5)

    return {
        "top_matches": top_jobs.to_dict(orient="records")
    }




