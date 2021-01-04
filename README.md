# Data Engineering Challenge

Hello and thank you for applying for the Data Engineer position at Quandoo!

To help us better assess your technical skills, we have prepared a set of tasks for you.

In order to succeed, it is not 100% necessary to finish all the tasks. Quality is more important than quantity.

These tasks attempt to mimic the 3 most common types of problems that our data engineers encounter at Quandoo: 

* designing data pipelines
 
* writing SQL
 
* writing scalable, maintainable Python/Scala code 

If you're not sure whether you can make certain assumptions (for example, about the input data) you can either make up your own reasonable assumptions(in which case make sure to communicate them when submitting your work), or discuss it with us (aleksandr.kurilov@quandoo.com or create an Issue here).

The preferred way to submit your work is described at the end of this readme. If you would like to use a different method, write to us and let's discuss it.

Now, the tasks!


## Task 1 - Data pipeline architecture 
We want to help our salespeople find new clients who might be interested in our products. 
In order to do that, we want to crawl around 10 million web pages that contain info about these potential clients.
The data should be stored in(or readable as), the JSON format, and should satisfy a specific schema(let's say something like `{"name", "phone", "email"}`).
The end result should be some type of a DB table/Kafka topic/some other storage that contains this data.
We want to minimize data latency and avoid unnecessary financial costs as well.
In other words, the data should be updated as often as possible and as cheaply as possible.
How would you design such a system? 
You might consider, for example
* which programming language to use
* which distributed computing engine to use
* which cloud services to use
* which algorithms, broadly speaking, to use 

No need to go too deep: you don’t have to decide on specific libraries, language/engine/service-specific tools or super-precise configurations for the aforementioned products or cloud services.

Please, compose an architecture diagram or a description - in any format you want - as a solution for the task. 

## Task 2 - SQL 
We have a table that contains our “merchants”(restaurants).
For each merchant we might have more than one row, where each row represents the state of the merchant at the time indicated by the timestamp field.
Write an SQL query that returns the last state of each merchant. 
 
| Field Name | Data Type  |  Description |
|---|---|---|
| merchant_id  |  STRING |  Merchant Identifier |
| timestamp  |  INTEGER |  Merchant state timestamp|
| createdAt  |  INTEGER |  Merchant creation timestamp |
| cuisines_additional | STRING | Merchant’s additional cuisines |
| priceRange| INTEGER | Price range category | 
 
Write two(or more) SQL queries that both return the last state of each of the merchants and outline their advantages and disadvantages(for example, how many times is the source table scanned)?

You can find some sample data in sql_challenge_dataset.csv.

## Task 3 - Data Processing with Python/Scala

You can complete the challenge using either Python or Scala.

The goal here is to analyze our 2020 reservations. 

The first step is to create a program that would reliably work with the given inputs(reservation_dataset.csv and merchant_dataset.csv).

The second step is to consider scaling issues.

### Making it work with the given inputs

The input for this challenge are reservation_dataset.csv and merchant_dataset.csv(you can find them in this repo).

1. Exclude all the reservations with badly formatted email addresses. Note that the email addresses have been anonymized on purpose.
2. Print the average number of seated guests
3. Display the name of the merchant with the highest amount of seated guests from the merchant_csv dataset. Reservations with only 1 seated guest shouldn’t be considered for this analysis.
4. Display the name of the merchant with the highest amount of reservations for each quarter of the year (January, February, March;  April, May, June ...).

Please provide a dockerized program that can execute all the tasks sequentially.  

Bonus points if it comes with a script that allows us to use a different set of files as the input(with the same structure, of course).


### Scaling 

Does your solution scale for any/all of the subtasks(1-4)? 

In other words, would it still work if reservation_dataset.csv and merchant_dataset.csv were both 500G+ files? 

If not, try to come up with an upgraded version of the program that would handle bigger inputs.

If the solution that you have in mind is too complex or time-consuming to implement, describe what you would use and how it would fit together, or provide a diagram. 


## Submitting your solutions

* Fork it to a [!]private[!] gitlab repository (go to Settings -> General -> Visibility, project features, permissions -> Project visibility).
* Commit&Push your solutions(including all the diagrams, descriptions and code)
* Share the project with the gitlab user quandoo_recruitment_task (go to Settings -> Members -> Invite member, find the user in Select members to invite and set Choose a role permission to Developer)
* Send us an ssh clone link to the repository.

We are looking forward to discussing your solutions with you. Good luck!

# Solution:

## Task 1 - Data pipeline architecture 

Assumming that we have 10 millions of web pages to get information(crawling/scraping) using python (bs4,scrapy) or java(jsoup) applications, 
all these traffic realtime is a data wave, my approach is based on Kafka, because low latency, realtime feature, and multiple consumer/producer(containeraized) are main features and a good option for the problem.
Since Quandoo collect data throught websites in the whole worldwide, is required a high volume, fault tolerance, durability and zero downtime 
event stream platform, the main option Kafka is.
What about horizontal scaling, load balancing, self healing capabilities ? It's highly recommended Up your kafka clusters environment using Kubernetes,
It means a pod for each brokers, zookeeper, kafka connect, schema registry,etc. For use kubernetes + kafka cluster in a a cloud is recommended Confluent operator.
Not only Kubernetes works for kafka cluster, consumer and producer applications that could be python or kafka can be deployed in containers inside pods,
it adopt self healing features, if we ask about double process a event from a kafka topic, it does not happens since we use offset in consumer groups. 
This ensure not events missed per application, if have other application to consume the event from kafka topic not problem it uses another consumer group.
what about if my consumer App is down, is not a problem because consumer groups knows the lag(events not processed yet), when app is up will get pending events.

**I suggest this arquitecture using kubernetes, docker, kafka, python and prometheus for monitoring.**

![Image of arquitecture](/img/EventDriveArquitecture.png)

Programming languages:
- For scrapping
	-  python: bs4,scrapy . I suggest bs4 for the trending both works fine.(Franko recommend)
 	- java : jsoup. I recommend only if we have java dependencies, if not go with python
	- **I recommend python for a fast deliverables**
- For consumer/producer to Kafka
	- python: Faust,python kafka clients, python kafka client confluent. I recommend python becuase has integration with pandas,django,flask regarding which one
	- java : kafka streams . Has fully integration and ensure Exactly-once processing semantics. If Exactly-once is not required go for python. 
	- **I recommend Faust has more functions than other and has concepts from kafka streams and we can add ML models too.**
- which distributed computing engine to use
	- For Event stream platform: 
	- **I recommend kafka if we have a ops teams we can go with apache kafka opensource if not go with confluent + Kubernetes.**
- which monitoring tool to use
	- **kafka recommends monitor the cluster with prometheus, and we can integrate it with grafana**
- which cloud services to use
	- I prefer to use **GCP**. Since is the first option for analytics, per second billing, sustained use discounts makes it a good deal for cluster. 
				About consumer/producer apps we can use preemptible VMs in GKE too, if goes down self-healing will up with no events missed.
- which algorithms, broadly speaking, to use
	- We can design algotithms for contigence or disater recovery events in python/java/shell scripts in order to avoid data processed lost, restoring from some
	long term archive datastorage HDFS, S3,GCS, NoSql DB. If we need to improve or need new capabilities that bs4,scrapy,jsoup do not have, we can consider create our own algorithms

*I work with Kafka for event arquitectures, docker containers for microservices, and Elk for monitoring.

## Task 2 - SQL 

1) Check EXECUTION PLAN FOR execute a simple max-group by
``` bash
SELECT m.merchant_id , max(m.timestamp) as last_state  FROM merchants m group by m.merchant_id  ;
```
![Image of max](/img/cost_only_max.png)

Cost is 29.50

2) Check EXECUTION PLAN FOR execute a simple max-group + indexes + Analyze table + Optimize table (copy table);
``` bash
CREATE index idx_merchants_index on merchants_index(merchant_id(200));
CREATE index idx_timestamp on merchants_index(timestamp);
ANALYZE TABLE merchants_index;
OPTIMIZE TABLE merchants_index;
SELECT m.merchant_id , max(m.timestamp) as last_state  FROM merchants_index m group by m.merchant_id ;
```
![Image of max_plus](/img/cost_max_indx_anal_opt.png)

Cost is 29.50 . Because index, analyze and optimize are improves for query with filters.

3) Check EXECUTION PLAN FOR run a Partition by + Row Number+ Ordered + filter

``` bash
SELECT merchant_id,timestamp FROM(
SELECT
    ROW_NUMBER () OVER ( 
        PARTITION BY merchant_id
        ORDER BY timestamp desc
    ) order_timestamp ,merchant_id,timestamp
FROM
    merchants
    ) ordered_merchant 
    where order_timestamp=1;
```

![Image of partition_by](/img/partition_row_number.png)

Cost is 3.56 , **88% better**. Because we only ordered it, do not group by for a full scan.

## Task 3 - Data Processing with Python/Scala

### Making it work with the given inputs

I completed all task mentioned and I used docker with image, not pyspark because pyspark program run on top of a spark cluster, not containers.
**I used here Object oriented code, Unit testing, logging and of course dataframes**

Steps:

- Clone my repo(this one)
>git clone my_repo_franko_example

- Change directory to same than Dockerfile, and execute
>docker build -t quandoo_12-20 .

- Image built, now run container and please check output (include logs for move to Prometheus/Elasticsearch
>docker run -it --rm --name my-running-app2 quandoo_12-20

![Image of quandooApp](/img/Test.png)

**If you want to test with other input files(same name), only replace the files in this cloned repo, then apply docker build and docker run**

**Send parameters is supported, but better replace input files because the Dockerfile only runs a specific program and then ends.**

``` bash
class QuandooApp:
    
    def __init__(self, app_id,merchant_dataset='merchant_dataset.csv',reservation_dataset='reservation_dataset.csv'):

        self.app_id = app_id
        self.merchant_dataset = merchant_dataset
        self.reservation_dataset = reservation_dataset	
```

Also you can see the logs that can use to track apps from prometheus/elasticsearch.

![Image of logs](/img/logs.png)

Additionally I included test units.

![Image of unittest](/img/unittests.png)

### Scaling 

If the file increase suppose 500GB, we can consider move from python to pyspark program and run it using converted from csv to parquet format(81% ratio compression) inputs.

If we decide not use pyspark, let's check  the task for this 500GB file input, spliting the input file 500Gb.

1. 500GB file , we can split the file in chunk and run multiple applications, and union the ouputs.. is OK
2. 500GB file , if we split the average is an operation for the whole dataset..it will convert in a complex situation ..NOT OK.
3. 500GB file , same than task 2 is a max operation for the whole dataset..NOT OK
4. 500GB file , same than task 2 and 3, is a max operation for the whole dataset..NOT OK

I suggest for a bigger input files use pyspark cluster or cloud solution: Bigquery,google Dataflow,Google Dataproc.

Thanks - I hope to reach the goal :)
