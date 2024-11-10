# to transfer the  data from mysql(rds) to hdfs
sqoop import --connect jdbc:mysql://madb.c30kweeoo13i.eu-west-3.rds.amazonaws.com/im_db  
--table movies --username admin --password 'password'

# to  transfer the data from mysql(rds) to hive
hive --service metastore
sqoop import --connect jdbc:mysql://madb.c30kweeoo13i.eu-west-3.rds.amazonaws.com/im_db --table movies --username admin --password 'password' --hive-import 
