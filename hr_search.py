import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import random

# ---------------------------------------------------------
# 1. Mock Data Generation
# ---------------------------------------------------------
def generate_mock_resumes(num_resumes=50):
    first_names = ["Ahmed", "Sarah", "Mohamed", "Fatima", "Omar", "Aisha", "Ali", "Nour", "Youssef", "Laila"]
    last_names = ["Abdallah", "Hassan", "Ali", "Ibrahim", "Mahmoud", "Said", "Tariq", "Mansour", "Fawzi", "Kamal"]
    
    roles = ["Python Developer", "Data Scientist", "Frontend Engineer", "DevOps Engineer", "AI Engineer", "Product Manager"]
    
    skills_pool = {
        "Python Developer": ["Python", "Django", "Flask", "SQL", "Git", "REST APIs"],
        "Data Scientist": ["Python", "Machine Learning", "Pandas", "NumPy", "SQL", "Scikit-Learn"],
        "Frontend Engineer": ["JavaScript", "React", "HTML", "CSS", "TypeScript", "Redux"],
        "DevOps Engineer": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux", "Terraform"],
        "AI Engineer": ["Python", "PyTorch", "TensorFlow", "NLP", "Computer Vision", "FAISS", "Transformers", "Semantic Search"],
        "Product Manager": ["Agile", "Scrum", "Jira", "Product Roadmap", "Communication", "Leadership"]
    }

    resumes = []
    for i in range(num_resumes):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        role = random.choice(roles)
        # Select 3 to 5 skills from the role's skill pool
        candidate_skills = random.sample(skills_pool[role], random.randint(3, len(skills_pool[role])))
        experience_years = random.randint(1, 10)
        
        # Create a text summary that will be used for embedding
        summary = f"Experienced {role} with {experience_years} years of experience. Skilled in {', '.join(candidate_skills)}."
        
        resumes.append({
            "id": i,
            "name": name,
            "role": role,
            "skills": candidate_skills,
            "experience_years": experience_years,
            "summary": summary
        })
    
    # Ensure at least one really good AI Engineer for our test
    resumes[0] = {
        "id": 0,
        "name": "Ibrahim Expert",
        "role": "AI Engineer",
        "skills": ["Python", "PyTorch", "NLP", "FAISS", "Transformers", "Vector Databases", "Semantic Search"],
        "experience_years": 5,
        "summary": "Experienced AI Engineer with 5 years of experience. Skilled in Python, PyTorch, NLP, FAISS, Transformers, Vector Databases, Semantic Search."
    }
    
    return resumes

# ---------------------------------------------------------
# 2. Embedding Generation & FAISS Indexing
# ---------------------------------------------------------
class HRVectorSearch:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        print(f"Loading embedding model '{model_name}'...")
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.resumes_db = {}
        self.dimension = None

    def ingest_resumes(self, resumes):
        print(f"Ingesting {len(resumes)} resumes...")
        self.resumes_db = {r['id']: r for r in resumes}
        
        # Extract the text to be embedded
        texts = [r['summary'] for r in resumes]
        
        # Generate embeddings
        print("Generating vector embeddings...")
        embeddings = self.model.encode(texts, show_progress_bar=False)
        
        # Convert to float32 numpy array for FAISS
        embeddings = np.array(embeddings).astype('float32')
        self.dimension = embeddings.shape[1]
        
        # Initialize FAISS Index (IndexFlatL2 for exact L2 distance search)
        print(f"Initializing FAISS index with dimension {self.dimension}...")
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # Add vectors to FAISS
        self.index.add(embeddings)
        print(f"Successfully added {self.index.ntotal} vectors to FAISS.")

    # ---------------------------------------------------------
    # 3. Semantic Query & Reasoning
    # ---------------------------------------------------------
    def generate_reasoning(self, job_desc, candidate):
        """
        Simple programmatic reasoning generation using keyword overlap.
        """
        job_desc_lower = job_desc.lower()
        matched_skills = [skill for skill in candidate['skills'] if skill.lower() in job_desc_lower]
        
        if matched_skills:
            reasoning = f"Candidate matches key required skills: {', '.join(matched_skills)}. "
            reasoning += f"They have {candidate['experience_years']} years of experience as a {candidate['role']}."
        else:
            reasoning = f"Candidate is a {candidate['role']} with {candidate['experience_years']} years of experience, showing strong semantic relevance to the job description."
            
        return reasoning

    def search(self, job_description, top_k=3):
        print(f"\nSearching for Job Description: '{job_description}'")
        
        # Encode the Job Description
        query_embedding = self.model.encode([job_description])
        query_embedding = np.array(query_embedding).astype('float32')
        
        # Search FAISS
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for i in range(top_k):
            idx = int(indices[0][i])
            dist = float(distances[0][i])
            candidate = self.resumes_db[idx]
            
            # Calculate a mock match score based on L2 distance
            # L2 distance is smaller for closer matches. Let's convert it to a % score.
            match_score_pct = max(0, 100 - (dist * 15))
            
            reasoning = self.generate_reasoning(job_description, candidate)
            
            results.append({
                "candidate_id": candidate['id'],
                "name": candidate['name'],
                "role": candidate['role'],
                "match_score": f"{match_score_pct:.1f}%",
                "reasoning": reasoning
            })
            
        return results

# ---------------------------------------------------------
# 4. Main Execution
# ---------------------------------------------------------
if __name__ == "__main__":
    # 1. Generate Mock Data
    resumes = generate_mock_resumes(50)

    # Save mock resumes for inspection
    with open("mock_resumes.json", "w", encoding="utf-8") as f:
        json.dump(resumes, f, indent=4)
    print("Saved generated mock resumes to 'mock_resumes.json'")

    # 2. Setup Search Engine (loaded once, searched many times)
    search_engine = HRVectorSearch()
    search_engine.ingest_resumes(resumes)

    # 3. Interactive Search Loop
    print("\n" + "="*60)
    print("  HR Semantic Search Engine - Ready!")
    print("  Available roles: Python Developer, Data Scientist,")
    print("                   Frontend Engineer, DevOps Engineer,")
    print("                   AI Engineer, Product Manager")
    print("  Type 'exit' to quit.")
    print("="*60)

    while True:
        print()
        job_description = input("Enter Job Description to search: ").strip()

        if job_description.lower() == "exit":
            print("Exiting. Goodbye!")
            break

        if not job_description:
            print("Please enter a valid job description.")
            continue

        # 4. Perform Search
        top_candidates = search_engine.search(job_description, top_k=3)

        # 5. Output Results as JSON
        output_json = json.dumps(
            {"job_description": job_description, "top_candidates": top_candidates},
            indent=4
        )
        print("\n--- Final JSON Output ---")
        print(output_json)
        print("-" * 60)
        print("Search again or type 'exit' to quit.")
