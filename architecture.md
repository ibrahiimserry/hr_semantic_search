# HR Semantic Search Engine - Architecture & Scaling

This document addresses the technical assessment requirements regarding data privacy and scaling the vector search service to 50,000+ resumes.

## 1. Data Privacy Architecture
When dealing with HR data (resumes, profiles), preserving Personally Identifiable Information (PII) is a top priority.
- **Data Anonymization / PII Redaction**: Before sending any resume text to the embedding model (`sentence-transformers`), we must redact sensitive information such as Name, Email, Phone Number, and Address. This can be achieved using Named Entity Recognition (NER) models (like spaCy or Presidio).
- **Separation of Concerns**: The Vector Database (FAISS) should only store the vector embeddings and an internal `candidate_id`. It should *not* store the raw text or PII.
- **Secure Metadata Storage**: The mapping between `candidate_id` and the actual candidate details (Name, contact info) should be stored in a secure, encrypted relational database (e.g., PostgreSQL) with Role-Based Access Control (RBAC). Only authorized HR personnel can resolve a `candidate_id` back to a person.
- **Encryption**: Data should be encrypted at rest (both the Vector DB index and the relational database) and in transit (using TLS/HTTPS for any API endpoints).

## 2. Scaling to 50k+ Resumes
The current implementation uses `IndexFlatL2` from FAISS, which performs an exact, exhaustive distance calculation (k-Nearest Neighbors). While perfectly fine for 100-1,000 resumes, it becomes a bottleneck as the dataset grows.

To scale efficiently to 50,000+ resumes and beyond:
- **Approximate Nearest Neighbor (ANN) Indexing**: We should transition from exact search (`IndexFlatL2`) to ANN indexing.
  - **IVF (Inverted File Index)**: E.g., `IndexIVFFlat`. This partitions the vector space into Voronoi cells. During search, it only compares the query against vectors in the nearest cells, drastically reducing search time.
  - **HNSW (Hierarchical Navigable Small World)**: Highly efficient graph-based indexing providing extremely fast search times and high recall, ideal for production workloads.
- **Batch Processing for Embeddings**: When ingesting 50k+ resumes, generating embeddings sequentially is slow. We should batch the text inputs and utilize a GPU (via PyTorch/CUDA) to compute embeddings in parallel.
- **Distributed Vector Database**: If the scale continues to grow (e.g., millions of resumes) or if we need high availability and horizontal scaling, we would migrate from a local FAISS instance to a distributed, cloud-native vector database such as Pinecone, Milvus, or Qdrant.
- **Caching**: Frequently searched Job Descriptions or generic roles (e.g., "Software Engineer") can have their result sets cached (using Redis) to avoid re-computing the embedding and vector search.
