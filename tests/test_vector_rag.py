import unittest
from app.rag.vector_store import VectorIndex

class TestVectorRAG(unittest.TestCase):
    def setUp(self):
        self.index = VectorIndex(dimension=64)

    def test_insert_and_count(self):
        self.index.insert("doc_1", "chunk_1", "Arquitetura distribuída com tolerância a falhas.")
        self.index.insert("doc_2", "chunk_2", "Microsserviços escaláveis com Kubernetes e Docker.")
        self.assertEqual(self.index.count(), 2)

    def test_search_similarity_ordering(self):
        self.index.insert("doc_faiss", "c1", "Vector database com busca por similaridade e embeddings.")
        self.index.insert("doc_receita", "c2", "Receita de bolo de chocolate com morango.")

        hits = self.index.search("embeddings e base vetorial", top_k=2)
        self.assertGreater(len(hits), 0)
        self.assertEqual(hits[0]["doc_id"], "doc_faiss")
        self.assertGreaterEqual(hits[0]["similarity"], 0.0)

    def test_empty_search(self):
        hits = self.index.search("qualquer termo", top_k=3)
        self.assertEqual(len(hits), 0)
