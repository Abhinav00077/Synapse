import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
from config import EMBEDDING_MODEL, K_CLUSTERS, DATA_DIR

class HeadlineClusterer:
    def __init__(self, model_name=EMBEDDING_MODEL, n_clusters=K_CLUSTERS):
        self.model_name = model_name
        self.n_clusters = n_clusters
        self.embedding_model = SentenceTransformer(model_name)
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.embeddings = None
        self.cluster_labels = None
        
    def create_embeddings(self, headlines):
        """
        Create embeddings for headlines using MiniLM
        """
        print(f"Creating embeddings for {len(headlines)} headlines...")
        self.embeddings = self.embedding_model.encode(headlines, show_progress_bar=True)
        print(f"Embeddings shape: {self.embeddings.shape}")
        return self.embeddings
    
    def cluster_headlines(self, headlines):
        """
        Cluster headlines using KMeans
        """
        if self.embeddings is None:
            self.create_embeddings(headlines)
        
        print(f"Clustering {len(headlines)} headlines into {self.n_clusters} clusters...")
        self.cluster_labels = self.kmeans.fit_predict(self.embeddings)
        
        # Create cluster results
        cluster_results = []
        for i, (headline, label) in enumerate(zip(headlines, self.cluster_labels)):
            cluster_results.append({
                'headline': headline,
                'cluster_id': int(label),
                'embedding_index': i
            })
        
        return cluster_results
    
    def get_cluster_summaries(self, cluster_results):
        """
        Get representative headlines for each cluster
        """
        cluster_summaries = {}
        
        for cluster_id in range(self.n_clusters):
            cluster_headlines = [item['headline'] for item in cluster_results if item['cluster_id'] == cluster_id]
            
            if cluster_headlines:
                # Find the most representative headline (closest to cluster centroid)
                cluster_indices = [item['embedding_index'] for item in cluster_results if item['cluster_id'] == cluster_id]
                cluster_embeddings = self.embeddings[cluster_indices]
                centroid = self.kmeans.cluster_centers_[cluster_id]
                
                # Calculate distances to centroid
                distances = np.linalg.norm(cluster_embeddings - centroid, axis=1)
                representative_idx = cluster_indices[np.argmin(distances)]
                
                cluster_summaries[cluster_id] = {
                    'representative_headline': cluster_results[representative_idx]['headline'],
                    'headlines': cluster_headlines,
                    'size': len(cluster_headlines)
                }
        
        return cluster_summaries
    
    def analyze_clusters(self, cluster_results):
        """
        Analyze cluster characteristics
        """
        cluster_analysis = {}
        
        for cluster_id in range(self.n_clusters):
            cluster_headlines = [item['headline'] for item in cluster_results if item['cluster_id'] == cluster_id]
            
            if cluster_headlines:
                # Calculate average length
                avg_length = np.mean([len(headline) for headline in cluster_headlines])
                
                # Find common words
                all_words = ' '.join(cluster_headlines).lower().split()
                word_freq = pd.Series(all_words).value_counts().head(5)
                
                cluster_analysis[cluster_id] = {
                    'size': len(cluster_headlines),
                    'avg_length': avg_length,
                    'common_words': word_freq.to_dict()
                }
        
        return cluster_analysis
    
    def save_model(self, filepath=None):
        """
        Save the trained model
        """
        if filepath is None:
            filepath = os.path.join(DATA_DIR, 'clustering_model.pkl')
        
        model_data = {
            'kmeans': self.kmeans,
            'embeddings': self.embeddings,
            'cluster_labels': self.cluster_labels,
            'model_name': self.model_name,
            'n_clusters': self.n_clusters
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath=None):
        """
        Load a trained model
        """
        if filepath is None:
            filepath = os.path.join(DATA_DIR, 'clustering_model.pkl')
        
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.kmeans = model_data['kmeans']
            self.embeddings = model_data['embeddings']
            self.cluster_labels = model_data['cluster_labels']
            self.model_name = model_data['model_name']
            self.n_clusters = model_data['n_clusters']
            
            print(f"Model loaded from {filepath}")
            return True
        except FileNotFoundError:
            print(f"Model file not found: {filepath}")
            return False

if __name__ == "__main__":
    # Test the clusterer
    test_headlines = [
        "Apple stock rises on strong iPhone sales",
        "Tesla reports record quarterly earnings",
        "Microsoft announces new AI features",
        "Google parent Alphabet beats revenue expectations",
        "Amazon expands cloud services",
        "Facebook parent Meta faces regulatory scrutiny",
        "Netflix subscriber growth slows",
        "Disney streaming service gains momentum",
        "Intel chip shortage affects production",
        "AMD gains market share in processors"
    ]
    
    clusterer = HeadlineClusterer()
    cluster_results = clusterer.cluster_headlines(test_headlines)
    cluster_summaries = clusterer.get_cluster_summaries(cluster_results)
    
    print("\nCluster Summaries:")
    for cluster_id, summary in cluster_summaries.items():
        print(f"Cluster {cluster_id}: {summary['representative_headline']} (Size: {summary['size']})") 