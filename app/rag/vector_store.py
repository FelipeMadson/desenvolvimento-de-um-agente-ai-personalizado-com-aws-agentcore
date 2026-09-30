import math
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class DocumentChunk:
    doc_id: str
    chunk_id: str
    text: str
    vector: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)

class VectorIndex:
    def __init__(self, dimension: int = 64):
        self.dimension = dimension
        self.chunks: List[DocumentChunk] = []

    def _normalize(self, vec: List[float]) -> List[float]:
        norm = math.sqrt(sum(x * x for x in vec))
        if norm == 0.0:
            return [0.0] * len(vec)
        return [x / norm for x in vec]

    def _hash_embed(self, text: str) -> List[float]:
        """Gera embedding semântico determinístico de alta dispersão baseado em n-gramas e hashing."""
        vec = [0.0] * self.dimension
        words = text.lower().split()
        for idx, word in enumerate(words):
            h = int(hashlib_idx := sum(ord(c) * (31 ** i) for i, c in enumerate(word[:8])))
            pos = h % self.dimension
            sign = 1.0 if (h % 2 == 0) else -1.0
            vec[pos] += sign * (1.0 / (idx + 1))
        return self._normalize(vec)

    def insert(self, doc_id: str, chunk_id: str, text: str, metadata: Optional[Dict[str, Any]] = None) -> DocumentChunk:
        vector = self._hash_embed(text)
        chunk = DocumentChunk(doc_id=doc_id, chunk_id=chunk_id, text=text, vector=vector, metadata=metadata or {})
        self.chunks.append(chunk)
        return chunk

    def search(self, query: str, top_k: int = 3, min_similarity: float = 0.0) -> List[Dict[str, Any]]:
        query_vec = self._hash_embed(query)
        results = []

        for chunk in self.chunks:
            # Cosine similarity entre dois vetores normalizados é o produto escalar (dot product)
            similarity = sum(q * c for q, c in zip(query_vec, chunk.vector))
            if similarity >= min_similarity:
                results.append({
                    "doc_id": chunk.doc_id,
                    "chunk_id": chunk.chunk_id,
                    "text": chunk.text,
                    "similarity": round(float(similarity), 4),
                    "metadata": chunk.metadata
                })

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    def count(self) -> int:
        return len(self.chunks)

    def clear(self) -> None:
        self.chunks.clear()
