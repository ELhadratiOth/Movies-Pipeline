import json
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920x1080") 
chrome_options.add_argument("--disable-gpu") 
chrome_options.add_argument("--user-agent=Mozilla/5.0") 

db_config = {
    "host": "hostingdb.c30kweeoo13i.eu-west-3.rds.amazonaws.com",
    "user": "admin",
    "password": "password",
    "database": "imdb_database"
}

def create_database_and_table():
    connection = mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"]
    )
    cursor = connection.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config["database"]}")
    
    connection.database = db_config["database"]

    create_table_query = """
    CREATE TABLE IF NOT EXISTS imdb_movies (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255),
        year VARCHAR(10),
        duration INT,
        limite VARCHAR(50),
        rating VARCHAR(10),
        rating_votes INT
    )
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()

def insert_data(data):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO imdb_movies (name, year, duration, limite, rating, rating_votes)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    for item in data:
        cursor.execute(insert_query, (
            item["name"],
            item["year"],
            item["duration"],
            item["limite"],
            item["rating"],
            item["rating_votes"]
        ))

    connection.commit()
    cursor.close()
    connection.close()

def lambda_handler(event, context):
    create_database_and_table()

    driver = webdriver.Chrome(options=chrome_options)
    imdb = 'https://www.imdb.com/chart/top/?sort=release_date%2Cdesc'
    driver.get(imdb)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ipc-metadata-list-summary-item__c")))

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    items = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item__c")

    listOfElement = []

    def parse_duration(film_duration):
        try:
            return int(film_duration.split("h")[0]) * 60 + int(film_duration.split()[1][:-1])
        except:
            try:
                return int(film_duration.split("h")[0]) * 60
            except:
                return int(film_duration[:-1])

    def parse_rating_votes(rating_text):
        rating_votes = rating_text[2:-2]
        if rating_text[-2] != 'K':
            rating_votes = int(float(rating_votes) * 1000)
        return rating_votes

    for i in range(len(items)):
        film = items[i].text.split('\n')
        
        name = film[0].split(".")[1].strip()
        year = film[1]
        duration = parse_duration(film[2])

        if len(film) == 7:
            limite = film[3]
            rating = film[4]
            rating_votes = parse_rating_votes(film[5])
        else:
            limite = "Not Rated"
            rating = film[3]
            rating_votes = parse_rating_votes(film[4])

        dataOfElem = {
            "name": name,
            "year": year,
            "duration": duration,
            "limite": limite,
            "rating": rating,
            "rating_votes": rating_votes
        }

        listOfElement.append(dataOfElem)

    driver.quit()

    insert_data(listOfElement)

    return {
        "statusCode": 200,
        "body": "Data inserted successfully , finishhh"
    }
    
if __name__ == "__main__":
    print(lambda_handler(None, None))
