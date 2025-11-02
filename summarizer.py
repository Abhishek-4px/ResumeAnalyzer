import os
from groq import Groq

def get_groq_api_key():
    try:
        import streamlit as st
        return st.secrets["GROQ_API_KEY"]
    except:
        pass
    
    api_key = os.getenv("GROQ_API_KEY")   # added just for local sessions
    if not api_key:
        raise ValueError("GROQ_API_KEY not found.") 
    return api_key

def initialize_groq_client():
    api_key = get_groq_api_key()
    return Groq(api_key=api_key)

# The prompt I created is from prompt genie
def create_summarization_prompt(resume_text):
    prompt = f"""You are an expert at explaining technical projects to non-technical people, such as HR managers or business executives.

Analyze this resume and provide a comprehensive summary of ALL technical projects found.

For EACH project, structure your response as follows:

**Project Name**: [Extract the exact project name]

**What It Does (Simple Explanation)**: 
Explain in 2-3 sentences using everyday language and analogies. Avoid technical jargon. Make it understandable to someone with no technical background.

**Technical Complexity Level**: 
Rate as one of: Basic | Intermediate | Advanced | Expert

**Real-World Impact**: 
Describe who benefits from this project and how it helps solve real problems.

**Skills Demonstrated**: 
List 3-5 key skills this project showcases (e.g., problem-solving, system design, algorithm implementation)

**Impressiveness Rating**: 
Score from 1-10 with clear justification:
- 1-3: Basic/learning project
- 4-6: Solid intermediate work
- 7-8: Advanced, professional-grade
- 9-10: Exceptional, research/expert level

**Time Investment Saved**: 
Estimate: "This summary saves you [X] minutes/hours of technical research"

---

Example for reference:
If someone "Implemented Attention is All You Need from scratch":

**Project Name**: Transformer Neural Network (Attention Mechanism Implementation)

**What It Does**: Built the core technology that powers ChatGPT, Google Translate, and modern AI chatbots completely from scratch. This is like building a car engine from individual parts instead of buying a ready-made engine – it requires understanding every component deeply.

**Technical Complexity Level**: Expert

**Real-World Impact**: This technology revolutionized how computers understand and generate human language. It's used in translation apps, virtual assistants, content creation tools, and AI chatbots that millions use daily.

**Skills Demonstrated**: Deep learning expertise, mathematical modeling, algorithm implementation, research paper comprehension, software engineering

**Impressiveness Rating**: 9/10 - This demonstrates exceptional theoretical knowledge and practical coding ability. Most engineers use pre-built versions; building from scratch shows mastery of cutting-edge AI.

**Time Investment Saved**: This summary saves you 1-2 hours of researching what "transformers" and "attention mechanisms" are in AI.

---

Now analyze this resume:

{resume_text}

IMPORTANT: If no clear technical projects are found, state that explicitly and provide general observations about the candidate's technical background."""

    return prompt

def summarize_resume_projects(resume_text, model="llama-3.3-70b-versatile"):
    try:
        client = initialize_groq_client()
        prompt = create_summarization_prompt(resume_text)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert technical translator who explains complex projects to non-technical audiences."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=model,
            temperature=0.7, # most research papers suggest randomness between 0.5-0.7
            max_tokens=4096,
            top_p=1,         # nucleus sampling , I have alr used temp so no need
            stream=False  # false as it is hectic live typing of chunks
        )
        
        return chat_completion.choices[0].message.content  # extracting the 1st response
    
    except Exception as e:
        raise Exception(f"Error generating summary with Groq: {str(e)}")

def get_available_models():
    return [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "mixtral-8x7b-32768",
        "gemma2-9b-it"
    ]
