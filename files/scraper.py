import csv
import boto3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--window-size=1920x1080")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--user-agent=Mozilla/5.0")

def scrape_imdb():
    driver = webdriver.Chrome(options=chrome_options)
    imdb = 'https://www.imdb.com/chart/top/?sort=release_date%2Cdesc'
    driver.get(imdb)
#     time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "ipc-metadata-list-summary-item__c")))

    items = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item__c")

    listOfElement = []

    def get_duration(film_duration):
        try:
            return int(film_duration.split("h")[0]) * 60 + int(film_duration.split()[1][:-1])
        except:
            try:
                return int(film_duration.split("h")[0]) * 60
            except:
                return int(film_duration[:-1])

    def get_rating(rating_text):
        rating_votes = rating_text[2:-2]
        if rating_text[-2] != 'K':
            rating_votes = int(float(rating_votes) * 1000)
        return rating_votes 
    for i in range(len(items)):
#         print(i)
        film = items[i].text.split('\n')

        name = film[0].split(".")[1].strip()
        year = film[1]
        duration = get_duration(film[2])

        if len(film) == 7:
            limite = film[3]
            rating = film[4]
            rating_votes = get_rating(film[5])
        else:
            limite = "Not Rated"
            rating = film[3]
            rating_votes = get_rating(film[4])

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

    return listOfElement

def save_to_s3(data, bucket_name, file_name):
    keys = data[0].keys()
    with open('./movies_data.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    s3_client = boto3.client('s3')
    s3_client.upload_file('./movies_data.csv', bucket_name, file_name)

if __name__ == "__main__":
    data = scrape_imdb()
    save_to_s3(data, 'bucketimdb', 'movies_data.csv')
    print("finishh") 
