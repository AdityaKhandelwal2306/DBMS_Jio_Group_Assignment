import faiss
import numpy as np

class FaissIndex:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)
        self.embeddings = []
    
    def create(self, embedding):
        self.index.add(np.array([embedding]))
        self.embeddings.append(embedding)
        return len(self.embeddings) - 1
    
    def read(self, idx):
        if idx < 0 or idx >= len(self.embeddings):
            return None
        return self.embeddings[idx]
    
    def update(self, idx, embedding):
        if idx < 0 or idx >= len(self.embeddings):
            return False
        self.embeddings[idx] = embedding
        self.rebuild_index()
        return True
    
    def delete(self, idx):
        if idx < 0 or idx >= len(self.embeddings):
            return False
        del self.embeddings[idx]
        self.rebuild_index()
        return True
    
    def rebuild_index(self):
        self.index = faiss.IndexFlatL2(len(self.embeddings[0]))
        self.index.add(np.array(self.embeddings))
