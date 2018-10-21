# graph-data-structure-for-movielens-dataset

## tasks

- Graph database 
    - https://lbartkowski.wordpress.com/2015/04/21/why-i-left-apache-spark-graphx-and-returned-to-hbase-for-my-graph-database/  
- graph structure for recomendation dataset  
    - python https://www.kaggle.com/rounakbanik/movie-recommender-systems  
    - *python graphlab movielense https://www.analyticsvidhya.com/blog/2016/06/quick-guide-build-recommendation-engine-python/  
    - movielense https://dzone.com/articles/building-graph-based-movie  
    - *code notebook https://github.com/jadianes/spark-movie-lens  
    - graphx scala https://github.com/sundeepblue/yelper_recommendation_system  
    - *pyspark http://www.3leafnodes.com/apache-spark-introduction-recommender-system   
- spark graphX  
    - https://spark.apache.org/docs/latest/graphx-programming-guide.html  
- unit test  
- API  
- data model GIFI diagram  
    
- git repo structure and readme documentation  
    
- ingestion pipeline
- docker contenarize solution

## paln
1. Understanding the dataset  
    - The ER Diagram 
        - rating table: fact less fact table  
        - 
    ![ML ERD](https://github.com/vivek-bombatkar/graph-data-structure-for-recommendation-dataset/blob/master/ML_ERD.JPG)  
    
    - Graph representation
        - Nodes: represent movies  
        - Edges: combinations of Tags and relavence. More the relaves more the waight to the Edge  
    ![ML_GRAPH](https://github.com/vivek-bombatkar/graph-data-structure-for-recommendation-dataset/blob/master/ML_GRAPH.JPG)  
 
2. Ingestion pipeline
    - Overall architecture
        - Primary data source coule be SFTP location, WEB API etc. 
        - HIVE as a RAW data store  
        - HBASE to store final graph data structure   
    ![ML_INGESTION](https://github.com/vivek-bombatkar/graph-data-structure-for-recommendation-dataset/blob/master/ML_INGESTION.JPG)  
        
2. fisrt implementation with 'notebook'
    - ingestion to HBASE  
    - Airflow to build pipeline - Docker locally 
    - API for data retrival  
    - unit test    
2. Tech stack : pyspark + HBASE + Dockerfile + sparkml(later) 
3. visualization , story telling
    - https://go.gliffy.com/go/html5/12822750  
4. recomendation api
5. xxx
