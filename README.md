# graph-data-structure-for-movielens-dataset

## tasks

- Graph database 
    - https://lbartkowski.wordpress.com/2015/04/21/why-i-left-apache-spark-graphx-and-returned-to-hbase-for-my-graph-database/  
    - HBASE https://mapr.com/blog/guidelines-hbase-schema-design/  
    - HBASE https://de.slideshare.net/DanLynn1/storing-and-manipulating-graphs-in-hbase  
    - https://medium.com/basecs/from-theory-to-practice-representing-graphs-cfd782c5be38  
- graph structure for recomendation dataset  
    - python https://www.kaggle.com/rounakbanik/movie-recommender-systems  
    - *python graphlab movielense https://www.analyticsvidhya.com/blog/2016/06/quick-guide-build-recommendation-engine-python/  
    - movielense https://dzone.com/articles/building-graph-based-movie  
    - *code notebook https://github.com/jadianes/spark-movie-lens  
    - graphx scala https://github.com/sundeepblue/yelper_recommendation_system  
    - *pyspark http://www.3leafnodes.com/apache-spark-introduction-recommender-system   
    = python https://www.geeksforgeeks.org/graph-and-its-representations/  
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
        - Snowflake data model 
        - rating and tags : are fact table  
        
    ![ML ERD](https://github.com/vivek-bombatkar/graph-data-structure-for-recommendation-dataset/blob/master/ML_ERD.JPG)  
    
    - Graph representation
        - Nodes: represent movies  
        - Edges: combinations of Tags and relavence. More the relaves more the waight to the Edge  
        
    ![ML_GRAPH](https://github.com/vivek-bombatkar/graph-data-structure-for-recommendation-dataset/blob/master/ML_GRAPH_1.JPG)  
 
2. Ingestion pipeline
    - Overall architecture
        - Primary data source could be SFTP location, WEB API etc. 
        - HIVE as a RAW data store to store all the data in partitioned way.    
        - HBASE to store final graph data structure   
        
    ![ML_INGESTION](https://github.com/vivek-bombatkar/graph-data-structure-for-recommendation-dataset/blob/master/ML_INGESTION.JPG)  
        
    - Technical implementation with Airflow
        - [dag_ml_graph_ingestion_pipeline.py](https://github.com/vivek-bombatkar/graph-data-structure-for-recommendation-dataset/blob/master/dag_ml_graph_ingestion_pipeline_.py)
    
        ![ML_AIRFLOW_PIPELINE](https://github.com/vivek-bombatkar/graph-data-structure-for-recommendation-dataset/blob/master/ML_AIRFLOW_PIPELINE.JPG)
        
        
2. fisrt implementation with 'notebook'

    - pyspark DF store to HIVE
    - lookup and agg the ratings + tags + genome_tags + genome_score tables to HBASE  
    - Airflow to build pipeline - Docker locally 
    - API for grapg traverse & data retrival 
        - Adjacency List  
    - unit test    
2. Tech stack : pyspark + HBASE + Dockerfile + sparkml(later) 
3. visualization , story telling
    - https://go.gliffy.com/go/html5/12822750  
4. recomendation api
5. xxx
