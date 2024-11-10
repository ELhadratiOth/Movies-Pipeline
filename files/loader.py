import json
import boto3
import csv
import mysql.connector

s3_client = boto3.client('s3')

db_config = {
    'host': 'madb.c30kweeoo13i.eu-west-3.rds.amazonaws.com', # it;s a private  link don;t worry hhhh 
    'user': 'admin', 
    'password': 'password', 
    'database': 'im_db'  ,
    'port' : '3306'
}

def lambda_handler(event, context):
    bucket_name = 'bucketimdb'
    file_key = 'movies_data.csv'
    
    local_file = '/tmp/movies_data.csv'
    s3_client.download_file(bucket_name, file_key, local_file)

    connection = mysql.connector.connect(** db_config)

    
    try:
        with connection.cursor() as cursor:
            create_db_query = f"CREATE DATABASE IF NOT EXISTS {db_config['database']}"
            cursor.execute(create_db_query)
            
            create_table_query = """
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                year INT,
                duration INT,
                limite VARCHAR(50),
                rating FLOAT,
                rating_votes INT
            )
            """
            cursor.execute(create_table_query)
            
            with open(local_file, mode='r', encoding='ISO-8859-1') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    insert_query = """
                    INSERT INTO movies (name, year, duration, limite, rating, rating_votes)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (
                        row['name'],
                        row['year'],
                        row['duration'],
                        row['limite'],
                        row['rating'],
                        row['rating_votes']
                    ))
            
            connection.commit()
    
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise e
    
    finally:
        connection.close()
    
    return {
        'statusCode': 200,
        'body': 'finishhh'
    }
