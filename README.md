# Graph Datastructure Solution for Movielens dataset

And 'the story' goes like this...

### 1. Understanding the dataset  

- 1.1 The ER Diagram 
    - Snowflake data model 
    - rating and tags : are fact table  

![ML ERD](https://github.com/vivek-bombatkar/graph-data-structure-for-recommendation-dataset/blob/master/ML_ERD.JPG)  

- 1.2 Graph representation
    - Undirected graph  
    - Nodes: represent movies  
    - Edges: combinations of Tags and relavence. More the relaves more the waight to the Edge  

![ML_GRAPH](https://github.com/vivek-bombatkar/Graph-Datastructure-Solution-for-Movielens-dataset/blob/master/ML_GRAPH_4.JPG)  
 
### 2. Ingestion pipeline

- 2.1 Overall architecture
    - Primary data source could be SFTP location, WEB API etc. 
    - HIVE as a RAW data storage, to store data in partitioned by ingestion timestamp .    
    - HBASE to store final graph data structure           

![ML_INGESTION](https://github.com/vivek-bombatkar/graph-data-structure-for-recommendation-dataset/blob/master/ML_INGESTION_3.JPG)  

- 2.2 Adjacency List: to store data to graph structure 

![ML_HBASE_STRUCTUR](https://github.com/vivek-bombatkar/graph-data-structure-for-recommendation-dataset/blob/master/ML_HBASE_STRUCTUR_1.JPG)  

        
- 2.3 Technical implementation with Airflow
        
    - [dag_ml_graph_ingestion_pipeline.py](https://github.com/vivek-bombatkar/graph-data-structure-for-recommendation-dataset/blob/master/dag_ml_graph_ingestion_pipeline_.py)

    ![ML_AIRFLOW_PIPELINE](https://github.com/vivek-bombatkar/graph-data-structure-for-recommendation-dataset/blob/master/ML_AIRFLOW_PIPELINE.JPG)

        
### 3. Show me The code  

- 3.1 Repository structure
```

├── pics/
├── Dockerfile  
├── README.md
├── requirements.txt    # list all dependencies for package.
├── setup.py            # build script for setuptools. 
├── Makefile            # organize code compilation.
├── src/
|       __init__.py
|       main.py
|       module_1.py
|       └──shared/
|           __init__.py
|           logging.yaml
|           common.py
├── dag/
|       dag_ml_graph_ingestion_pipeline_.py     # Airflow dag file
└── tests/
|    └── testdata/
|       test_main.py
└── notebook/                                   # data exploration, quick prototype, etc.
|       pyspark_ingestion_pipeline.ipynb

```  

- 3.2 Code snipt from 'notebook' implementation [pyspark_ingestion_pipeline.ipynb](https://github.com/vivek-bombatkar/graph-data-structure-for-recommendation-dataset/blob/master/pyspark_ingestion_pipeline.ipynb)  

    - ###3.2.1 Data Exploration with Pandas
    ```python

        In [1]:
    import pandas as pd
    File uploaded to /FileStore/tables/links.csv
    File uploaded to /FileStore/tables/movies.csv
    File uploaded to /FileStore/tables/tags.csv
    File uploaded to /FileStore/tables/genome_tags-e89dc.csv
    File uploaded to /FileStore/tables/ratings.csv
    File uploaded to /FileStore/tables/genome_scores-02096.csv

    In [3]:
    # %fs head /FileStore/tables/links.csv

    pdf_links = pd.read_csv("/dbfs/FileStore/tables/links.csv")
    pdf_movies = pd.read_csv("/dbfs/FileStore/tables/movies.csv")
    pdf_tags = pd.read_csv("/dbfs/FileStore/tables/tags.csv")
    pdf_genome_tags = pd.read_csv("/dbfs/FileStore/tables/genome_tags-e89dc.csv")
    pdf_ratings = pd.read_csv("/dbfs/FileStore/tables/ratings.csv")
    pdf_genome_scores = pd.read_csv("/dbfs/FileStore/tables/genome_scores-02096.csv")

    # pdf_links

    ```

    - PySpark dataframe from csv data and load data to HDFS / HIVE 
    ```python

    In [14]:
    sdf_links = spark.read.csv('/FileStore/tables/links.csv',inferSchema = "true",header= True)
    sdf_movies = spark.read.csv("/FileStore/tables/movies.csv",inferSchema = "true",header= True)
    sdf_tags = spark.read.csv("/FileStore/tables/tags.csv",inferSchema = "true",header= True)
    sdf_genome_tags = spark.read.csv("/FileStore/tables/genome_tags-e89dc.csv",inferSchema = "true",header= True)
    sdf_ratings = spark.read.csv("/FileStore/tables/ratings.csv",inferSchema = "true",header= True)
    sdf_genome_scores = spark.read.csv("/FileStore/tables/genome_scores-02096.csv",inferSchema = "true",header= True)

     sdf_genome_scores .printSchema()

    In [15]:
    from pyspark.sql.functions import lit
    import time
    ts = time.gmtime()
    partition_ts = time.strftime("%Y%m%d_%H%M%S", ts)

    # 1. genome_scores
    # partition by timestamp and movieID
    # add a timestamp as partition column
    sdf_genome_scores = sdf_genome_scores.withColumn('partition_ts',lit(partition_ts))
    sdf_genome_scores.write.partitionBy('partition_ts','movieId').mode("append").saveAsTable("genome_scores")

    # 2. genome_tags
    # partition by timestamp only 
    # repartiton(1000).
    sdf_genome_tags = sdf_genome_tags.withColumn('partition_ts',lit(partition_ts))
    sdf_genome_tags.write.partitionBy('partition_ts').mode("append").saveAsTable("genome_tags")

    # 3. tags
    # partition by timestamp only and movieID
    sdf_tags = sdf_tags.withColumn('partition_ts',lit(partition_ts))
    sdf_tags.write.partitionBy('partition_ts','movieId').mode("append").saveAsTable("tags")

    In [17]:
    %fs ls /user/hive/warehouse/genome_scores/partition_ts=20181022_182142/movieId=2/
    path	name	size
    dbfs:/user/hive/warehouse/genome_scores/partition_ts=20181022_182142/movieId=2/_SUCCESS	_SUCCESS	0
    dbfs:/user/hive/warehouse/genome_scores/partition_ts=20181022_182142/movieId=2/_committed_3187766080380504256	_committed_3187766080380504256	121
    dbfs:/user/hive/warehouse/genome_scores/partition_ts=20181022_182142/movieId=2/_started_3187766080380504256	_started_3187766080380504256	0
    dbfs:/user/hive/warehouse/genome_scores/partition_ts=20181022_182142/movieId=2/part-00000-tid-3187766080380504256-33905e8c-c865-4bcc-b994-25b322c89c46-33.c000.snappy.parquet	part-00000-tid-3187766080380504256-33905e8c-c865-4bcc-b994-25b322c89c46-33.c000.snappy.parquet	


    ```

    - lookup and agg the ratings + tags + genome_tags + genome_score tables to HBASE  
    - API for grapg traverse & data retrival 
        - Get the most relavent Tag for movie  
        - Find column family for that TagId (Key)  
        - Suggest Movies from given column list   
    - unit test    
2. Tech stack : pyspark + HBASE + Dockerfile + sparkml(later) 
4. recomendation api


## Resources used 
- Graph database 
    - https://lbartkowski.wordpress.com/2015/04/21/why-i-left-apache-spark-graphx-and-returned-to-hbase-for-my-graph-database/  
    - HBASE https://mapr.com/blog/guidelines-hbase-schema-design/  
    - HBASE https://de.slideshare.net/DanLynn1/storing-and-manipulating-graphs-in-hbase  
    - video https://www.youtube.com/watch?v=KQMCOgVdsiw  
    - https://medium.com/basecs/from-theory-to-practice-representing-graphs-cfd782c5be38  
- graph structure for recomendation dataset  
    - python https://www.kaggle.com/rounakbanik/movie-recommender-systems  
    - *python graphlab movielense https://www.analyticsvidhya.com/blog/2016/06/quick-guide-build-recommendation-engine-python/  
    - movielense https://dzone.com/articles/building-graph-based-movie  
    - *code notebook https://github.com/jadianes/spark-movie-lens  
    - graphx scala https://github.com/sundeepblue/yelper_recommendation_system  
    - *pyspark http://www.3leafnodes.com/apache-spark-introduction-recommender-system   
    - python https://www.geeksforgeeks.org/graph-and-its-representations/  
    - https://docs.microsoft.com/en-us/azure/hdinsight/hdinsight-using-spark-query-hbase  
- spark graphX  
    - https://spark.apache.org/docs/latest/graphx-programming-guide.html  
- unit test  
- visualization 
    - https://go.gliffy.com/go/html5/12822750  
