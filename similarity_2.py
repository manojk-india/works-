import os
import numpy as np
from pptx import Presentation
from sentence_transformers import SentenceTransformer, util

def extract_text_from_ppt(ppt_path):
    """Extract text from a PowerPoint presentation."""
    prs = Presentation(ppt_path)
    text_content = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text_content.append(shape.text)
    return " ".join(text_content)  

# Load sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")


ppt_folder = "ppts"
ppt_files = [os.path.join(ppt_folder, f) for f in os.listdir(ppt_folder) if f.endswith(".pptx")][:10]

# Extract text from PPTs
all_docs = [extract_text_from_ppt(ppt) for ppt in ppt_files]

# Encode all documents into embeddings
embeddings = model.encode(all_docs, convert_to_tensor=True) 

# Extract text and embedding for query PPT
query_ppt_text = extract_text_from_ppt("ppts/Future_of_AI_2.pptx")
query_embedding = model.encode(query_ppt_text, convert_to_tensor=True)

# Compute similarity scores
similarity_scores = util.pytorch_cos_sim(query_embedding, embeddings)[0].cpu().numpy()  # Convert to numpy array

# Get top-k similar PPTs
top_k = 4
top_indices = np.argsort(similarity_scores)[-top_k:][::-1]  # Get top 3 in descending order
print(similarity_scores)



print("Top 4 similar PPTs:")
for idx in top_indices:
    print(f"{ppt_files[idx]} - Similarity Score: {similarity_scores[idx]:.4f}")
