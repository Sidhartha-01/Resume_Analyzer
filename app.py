import fitz  # PyMuPDF
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def analyze_resume_with_gemini(pdf_path, api_key):
    """Extract and analyze resume details using Gemini API."""
   
    resume_text = extract_text_from_pdf(pdf_path)
    

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
    
    
    prompt = ("Extract the following details from the resume: name: “...”, email: ,core_skills: [ ]soft_skills: [ ],resume_rating: , improvement_areas:, upskill_suggestions:   .No field should be empty. if any of the fields data is not available then analyse and fill the proper. resume_rating:  improvement_areas: upskill_suggestions:. these field s should be filled compulsory"+ resume_text)
    
    response = model.generate_content(prompt)
    
    # print(response.text)
    return response.text

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    pdf_path = "uploaded_resume.pdf"
    file.save(pdf_path)
    
    api_key = "AIzaSyALs5U3G39wEo-SyCuLFv-fEEWQmNkf6Pg"  # Replace with your Gemini API key
    extracted_info = analyze_resume_with_gemini(pdf_path, api_key)
    return jsonify({"resume_details": extracted_info})

if __name__ == "__main__":
    app.run(debug=True)
