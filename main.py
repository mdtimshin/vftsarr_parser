import os
import re
from datetime import datetime

import pandas
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


sportsmens = [
    {
        'Book_No': '79505',
        'Name': 'Тимшин_Михаил_Дмитриевич'
    },
    {
        'Book_No': '122664',
        'Name': 'Вавилина_Майя_Алексеевна'
    },
    {
        'Book_No': '114739',
        'Name': 'Мошев_Артем_Игоревич'
    },
    {
        'Book_No': '122691',
        'Name': 'Худяшова_Ирина_Антоновна'
    },
    {
        'Book_No': '159923',
        'Name': 'Хакимов_Тимур_Маратович'
    },
    {
        'Book_No': '151871',
        'Name': 'Маракулина_Александра_Ивановна'
    },
    {
        'Book_No': '203188',
        'Name': 'Шахов_Георгий_Витальевич'
    },
    {
        'Book_No': '203187',
        'Name': 'Шишкина_Мария_Ивановна'
    },
    {
        'Book_No': '164487',
        'Name': 'Садыков_Рустам_Шамилевич'
    },
    {
        'Book_No': '164481',
        'Name': 'Куликова_Маргарита_Алексеевна'
    },
    {
        'Book_No': '203190',
        'Name': 'Захаров_Лука_Ильич'
    },
    {
        'Book_No': '159822',
        'Name': 'Елдашова_Анастасия_Максимовна'
    },
    {
        'Book_No': '146456',
        'Name': 'Литевский_Максим_Георгиевич'
    },
    {
        'Book_No': '151821',
        'Name': 'Шепель_Владислава_Алексеевна'
    },
    {
        'Book_No': '164577',
        'Name': 'Балабанов_Семён_Алексеевич'
    },
    {
        'Book_No': '203083',
        'Name': 'Косвинцева_София_Дмитриевна'
    },
    {
        'Book_No': '122639',
        'Name': 'Гималтдинов_Даниил_Альбертович'
    },
    {
        'Book_No': '136276',
        'Name': 'Щекина_Софья_Александровна'
    },
    {
        'Book_No': '149210',
        'Name': 'Трубин_Макар_Олегович'
    },
    {
        'Book_No': '159921',
        'Name': 'Минеева_Полина_Евгеньевна'
    },
    {
        'Book_No': '122734',
        'Name': 'Никитин_Георгий_Михайлович'
    },
]

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "content-length": "79",
    "content-type": "application/x-www-form-urlencoded",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36"
}
url = "https://dance.vftsarr.ru/index.php"

chrome_options = Options()
driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)

for sportsmen in sportsmens:
    payload = {
        "Book_No": f"{sportsmen['Book_No']}",
        "DancerName": "",
        "id": "0",
        "Do": "Search"
    }

    r = requests.post(url=url, headers=headers, data=payload)

    soup = BeautifulSoup(r.text, "lxml")

    data_tables = soup.find_all("table", class_="bugitable")
    dataframe = pd.DataFrame()

    df1 = pd.read_html(str(data_tables[0]))[0]
    dataframe = dataframe.append(df1, ignore_index=True)

    if len(data_tables) == 3:
        try:
            df2 = pd.read_html(str(data_tables[1]))[0]
            dataframe = dataframe.append(df2, ignore_index=True)
        except:
            pass

    dataframe = dataframe.dropna()
    dataframe = dataframe.transpose()
    dataframe.columns = dataframe.iloc[0]
    dataframe = dataframe[1:]

    sportsmen_name = ''
    sportsmen_age = ''
    partner_book_no = ''

    try:
        if dataframe['Пол:'].iloc[0].tolist()[0] == "Жен.":
            sportsmen_name = dataframe['В паре с:'].tolist()[0].split()[1:3]
            sportsmen_name = ' '.join(sportsmen_name)
            # partner_book_no = dataframe['В паре с:'].tolist()[0].split()[0][1:-1]
        else:
            sportsmen_name = sportsmen['Name'].split('_')[:2]
            sportsmen_name = ' '.join(sportsmen_name)
    except AttributeError:
        if dataframe['Пол:'].iloc[0] == "Жен.":
            sportsmen_name = dataframe['В паре с:'].tolist()[0].split()[1:3]
            sportsmen_name = ' '.join(sportsmen_name)
            # partner_book_no = dataframe['В паре с:'].tolist()[0].split()[0][1:-1]
        else:
            sportsmen_name = sportsmen['Name'].split('_')[:2]
            sportsmen_name = ' '.join(sportsmen_name)

    # TODO: у партнерш не ставится рейтинг, так как танцует в категории выше. Потом сделать сравнение возраста партнеров и посмотреть, у кого из них скопировать рейтинг

    date_of_birth = dataframe['Дата рождения:'].tolist()[0].split('.')
    date_of_birth = datetime(day=int(date_of_birth[0]), month=int(date_of_birth[1]), year=int(date_of_birth[2]))

    sportsmen_age = datetime.now().year - date_of_birth.year

    rating_standard = ''
    rating_standard_url = ''
    rating_latin = ''
    rating_latin_url = ''
    rating_ten_dance = ''
    rating_ten_dance_url = ''

    if sportsmen_age >= 21:
        rating_standard_url = 'https://fdsarr.ru/dance/rating/?itog=Y&type=Itog&age=%D0%9C%D1%83%D0%B6%D1%87%D0%B8%D0%BD%D1%8B%20%20%D0%B8%20%D0%B6%D0%B5%D0%BD%D1%89%D0%B8%D0%BD%D1%8B&program=%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B5%D0%B9%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0'
        rating_latin_url = 'https://fdsarr.ru/dance/rating/?itog=Y&type=Itog&age=%D0%9C%D1%83%D0%B6%D1%87%D0%B8%D0%BD%D1%8B%20%20%D0%B8%20%D0%B6%D0%B5%D0%BD%D1%89%D0%B8%D0%BD%D1%8B&program=%D0%9B%D0%B0%D1%82%D0%B8%D0%BD%D0%BE%D0%B0%D0%BC%D0%B5%D1%80%D0%B8%D0%BA%D0%B0%D0%BD%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0'
        rating_ten_dance_url = 'https://fdsarr.ru/dance/rating/?itog=Y&type=Itog&age=%D0%9C%D1%83%D0%B6%D1%87%D0%B8%D0%BD%D1%8B%20%20%D0%B8%20%D0%B6%D0%B5%D0%BD%D1%89%D0%B8%D0%BD%D1%8B&program=%D0%94%D0%B2%D0%BE%D0%B5%D0%B1%D0%BE%D1%80%D1%8C%D0%B5'
    elif 16 <= sportsmen_age <= 20:
        rating_standard_url = 'https://fdsarr.ru/dance/rating/?itog=Y&type=Itog&age=%D0%AE%D0%BD%D0%B8%D0%BE%D1%80%D1%8B%20%D0%B8%20%D1%8E%D0%BD%D0%B8%D0%BE%D1%80%D0%BA%D0%B8%20(16-20%20%D0%BB%D0%B5%D1%82)&program=%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B5%D0%B9%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0'
        rating_latin_url = 'https://fdsarr.ru/dance/rating/?itog=Y&type=Itog&age=%D0%AE%D0%BD%D0%B8%D0%BE%D1%80%D1%8B%20%D0%B8%20%D1%8E%D0%BD%D0%B8%D0%BE%D1%80%D0%BA%D0%B8%20(16-20%20%D0%BB%D0%B5%D1%82)&program=%D0%9B%D0%B0%D1%82%D0%B8%D0%BD%D0%BE%D0%B0%D0%BC%D0%B5%D1%80%D0%B8%D0%BA%D0%B0%D0%BD%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0'
        rating_ten_dance_url = 'https://fdsarr.ru/dance/rating/?itog=Y&type=Itog&age=%D0%AE%D0%BD%D0%B8%D0%BE%D1%80%D1%8B%20%D0%B8%20%D1%8E%D0%BD%D0%B8%D0%BE%D1%80%D0%BA%D0%B8%20(16-20%20%D0%BB%D0%B5%D1%82)&program=%D0%94%D0%B2%D0%BE%D0%B5%D0%B1%D0%BE%D1%80%D1%8C%D0%B5'
    elif 14 <= sportsmen_age <= 15:
        rating_standard_url = 'https://fdsarr.ru/dance/rating/?itog=Y&type=Itog&age=%D0%AE%D0%BD%D0%BE%D1%88%D0%B8%20%D0%B8%20%D0%B4%D0%B5%D0%B2%D1%83%D1%88%D0%BA%D0%B8%20(14-15%20%D0%BB%D0%B5%D1%82)&program=%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B5%D0%B9%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0'
        rating_latin_url = 'https://fdsarr.ru/dance/rating/?itog=Y&type=Itog&age=%D0%AE%D0%BD%D0%BE%D1%88%D0%B8%20%D0%B8%20%D0%B4%D0%B5%D0%B2%D1%83%D1%88%D0%BA%D0%B8%20(14-15%20%D0%BB%D0%B5%D1%82)&program=%D0%9B%D0%B0%D1%82%D0%B8%D0%BD%D0%BE%D0%B0%D0%BC%D0%B5%D1%80%D0%B8%D0%BA%D0%B0%D0%BD%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0'
        rating_ten_dance_url = 'https://fdsarr.ru/dance/rating/?itog=Y&type=Itog&age=%D0%AE%D0%BD%D0%BE%D1%88%D0%B8%20%D0%B8%20%D0%B4%D0%B5%D0%B2%D1%83%D1%88%D0%BA%D0%B8%20(14-15%20%D0%BB%D0%B5%D1%82)&program=%D0%94%D0%B2%D0%BE%D0%B5%D0%B1%D0%BE%D1%80%D1%8C%D0%B5'
    elif 12 <= sportsmen_age <= 13:
        rating_standard_url = 'https://fdsarr.ru/dance/rating/?itog=Y&type=Itog&age=%D0%AE%D0%BD%D0%BE%D1%88%D0%B8%20%D0%B8%20%D0%B4%D0%B5%D0%B2%D1%83%D1%88%D0%BA%D0%B8%20(12-13%20%D0%BB%D0%B5%D1%82)&program=%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B5%D0%B9%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0'
        rating_latin_url = 'https://fdsarr.ru/dance/rating/?itog=Y&type=Itog&age=%D0%AE%D0%BD%D0%BE%D1%88%D0%B8%20%D0%B8%20%D0%B4%D0%B5%D0%B2%D1%83%D1%88%D0%BA%D0%B8%20(12-13%20%D0%BB%D0%B5%D1%82)&program=%D0%9B%D0%B0%D1%82%D0%B8%D0%BD%D0%BE%D0%B0%D0%BC%D0%B5%D1%80%D0%B8%D0%BA%D0%B0%D0%BD%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0'
        rating_ten_dance_url = 'https://fdsarr.ru/dance/rating/?itog=Y&type=Itog&age=%D0%AE%D0%BD%D0%BE%D1%88%D0%B8%20%D0%B8%20%D0%B4%D0%B5%D0%B2%D1%83%D1%88%D0%BA%D0%B8%20(12-13%20%D0%BB%D0%B5%D1%82)&program=%D0%94%D0%B2%D0%BE%D0%B5%D0%B1%D0%BE%D1%80%D1%8C%D0%B5'
    elif 10 <= sportsmen_age <= 11:
        rating_standard_url = 'https://fdsarr.ru/dance/rating/?itog=Y&type=Itog&age=%D0%9C%D0%B0%D0%BB%D1%8C%D1%87%D0%B8%D0%BA%D0%B8%20%D0%B8%20%D0%B4%D0%B5%D0%B2%D0%BE%D1%87%D0%BA%D0%B8%20(10-11%20%D0%BB%D0%B5%D1%82)&program=%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B5%D0%B9%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0'
        rating_latin_url = 'https://fdsarr.ru/dance/rating/?itog=Y&type=Itog&age=%D0%9C%D0%B0%D0%BB%D1%8C%D1%87%D0%B8%D0%BA%D0%B8%20%D0%B8%20%D0%B4%D0%B5%D0%B2%D0%BE%D1%87%D0%BA%D0%B8%20(10-11%20%D0%BB%D0%B5%D1%82)&program=%D0%9B%D0%B0%D1%82%D0%B8%D0%BD%D0%BE%D0%B0%D0%BC%D0%B5%D1%80%D0%B8%D0%BA%D0%B0%D0%BD%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0'
        rating_ten_dance_url = 'https://fdsarr.ru/dance/rating/?itog=Y&type=Itog&age=%D0%9C%D0%B0%D0%BB%D1%8C%D1%87%D0%B8%D0%BA%D0%B8%20%D0%B8%20%D0%B4%D0%B5%D0%B2%D0%BE%D1%87%D0%BA%D0%B8%20(10-11%20%D0%BB%D0%B5%D1%82)&program=%D0%94%D0%B2%D0%BE%D0%B5%D0%B1%D0%BE%D1%80%D1%8C%D0%B5'
    elif 7 <= sportsmen_age <= 9:
        rating_standard_url = 'https://fdsarr.ru/dance/rating/?itog=Y&type=Itog&age=%D0%9C%D0%B0%D0%BB%D1%8C%D1%87%D0%B8%D0%BA%D0%B8%20%D0%B8%20%D0%B4%D0%B5%D0%B2%D0%BE%D1%87%D0%BA%D0%B8%20(7-9%20%D0%BB%D0%B5%D1%82)&program=%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B5%D0%B9%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0'
        rating_latin_url = 'https://fdsarr.ru/dance/rating/?itog=Y&type=Itog&age=%D0%9C%D0%B0%D0%BB%D1%8C%D1%87%D0%B8%D0%BA%D0%B8%20%D0%B8%20%D0%B4%D0%B5%D0%B2%D0%BE%D1%87%D0%BA%D0%B8%20(7-9%20%D0%BB%D0%B5%D1%82)&program=%D0%9B%D0%B0%D1%82%D0%B8%D0%BD%D0%BE%D0%B0%D0%BC%D0%B5%D1%80%D0%B8%D0%BA%D0%B0%D0%BD%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0'
        rating_ten_dance_url = 'https://fdsarr.ru/dance/rating/?itog=Y&type=Itog&age=%D0%9C%D0%B0%D0%BB%D1%8C%D1%87%D0%B8%D0%BA%D0%B8%20%D0%B8%20%D0%B4%D0%B5%D0%B2%D0%BE%D1%87%D0%BA%D0%B8%20(7-9%20%D0%BB%D0%B5%D1%82)&program=%D0%94%D0%B2%D0%BE%D0%B5%D0%B1%D0%BE%D1%80%D1%8C%D0%B5'

    driver.get(rating_standard_url)
    driver.implicitly_wait(5)
    amount_of_couples_standard = driver.find_element(By.CLASS_NAME, "headinfo").find_elements(By.TAG_NAME, "div")[0].find_elements(By.TAG_NAME, "p")[1].find_element(By.TAG_NAME, "strong").text
    search_input = driver.find_element(By.XPATH, "//input[@type='search']")
    search_input.send_keys(sportsmen_name)
    driver.implicitly_wait(5)
    table = driver.find_element(By.ID, "tableRussia-itog").find_element(By.TAG_NAME, "tbody")
    try:
        rating_standard = table.find_elements(By.TAG_NAME, "td")[1].text
    except IndexError:
        pass

    driver.get(rating_latin_url)
    amount_of_couples_latin = driver.find_element(By.CLASS_NAME, "headinfo").find_elements(By.TAG_NAME, "div")[0].find_elements(By.TAG_NAME, "p")[1].find_element(By.TAG_NAME, "strong").text
    search_input = driver.find_element(By.XPATH, "//input[@type='search']")
    search_input.send_keys(sportsmen_name)
    driver.implicitly_wait(5)
    table = driver.find_element(By.ID, "tableRussia-itog").find_element(By.TAG_NAME, "tbody")
    try:
        rating_latin = table.find_elements(By.TAG_NAME, "td")[1].text
    except IndexError:
        pass

    driver.get(rating_ten_dance_url)
    amount_of_couples_ten_dance = driver.find_element(By.CLASS_NAME, "headinfo").find_elements(By.TAG_NAME, "div")[0].find_elements(By.TAG_NAME, "p")[1].find_element(By.TAG_NAME, "strong").text
    search_input = driver.find_element(By.XPATH, "//input[@type='search']")
    search_input.send_keys(sportsmen_name)
    driver.implicitly_wait(5)
    table = driver.find_element(By.ID, "tableRussia-itog").find_element(By.TAG_NAME, "tbody")

    try:
        rating_ten_dance = table.find_elements(By.TAG_NAME, "td")[1].text
    except IndexError:
        pass

    dataframe['Рейтинг стандарт'] = rating_standard
    dataframe['Пар в рейтинге стандарта'] = amount_of_couples_standard
    dataframe['Рейтинг латина'] = rating_latin
    dataframe['Пар в рейтинге латины'] = amount_of_couples_latin
    dataframe['Рейтинг двоеборье'] = rating_ten_dance
    dataframe['Пар в рейтинге двоеборья'] = amount_of_couples_ten_dance

    if not os.path.isdir(f"{sportsmen['Name']}"):
        os.mkdir(f"{sportsmen['Name']}")
    dataframe.to_csv(f"{sportsmen['Name']}/{sportsmen['Name']}_Данные.csv", sep='\t', encoding='utf-8', index=False,
                     header=True)

    form_url = "https://dance.vftsarr.ru/index.php?id=0&Do=Search"
    form_headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "content-length": "89",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36"
    }

    years = soup.find("select", {"name": "Year"}).find_all("option")
    years = list(map(lambda x: x.text, years))

    ALL_DATAFRAME = pd.DataFrame()

    for year in years:
        form_payload = {
            "Year": str(year),
            "Dancer_Class": "All",
            "Dancer_Program": "0",
            "Book_No": f"{sportsmen['Book_No']}"
        }

        form_response = requests.post(url=form_url, headers=form_headers, data=form_payload)

        soup = BeautifulSoup(form_response.text, "lxml")

        data_tables = soup.find_all("table", class_="bugitable")

        competitions_df = pd.read_html(str(data_tables[-1]))[0]

        competitions_results_df = competitions_df.drop(index=competitions_df.index[::2])

        data = data_tables[-1]
        competitions_trs = data.find_all("tr")[1::2]

        date_list = []
        city_list = []
        status_list = []
        group_list = []

        for tr in competitions_trs:
            date = tr.find_all("b")[0].text[0:10]
            date_list.append(date)

            city = tr.find("a").next_sibling.string
            city = re.sub('|\?|\.|\!|\/|\;|\:|\,', '', city)
            city_list.append(city)

            status = tr.find("b").next_sibling.string
            status_list.append(status)

            group = tr.find_all('a')[-1].text
            group_list.append(group)

        competitions_results_df['Дата'] = date_list
        competitions_results_df['Город'] = city_list
        competitions_results_df['Статус'] = status_list
        competitions_results_df['Группа'] = group_list

        ALL_DATAFRAME = ALL_DATAFRAME.append(competitions_results_df, ignore_index=True)

    ALL_DATAFRAME['Пар в группе'] = ALL_DATAFRAME.apply(lambda x: x['Место в группе'].split('/')[1], axis=1)
    ALL_DATAFRAME['Место в группе'] = ALL_DATAFRAME.apply(lambda x: str(x['Место в группе']).split('/')[0], axis=1)
    ALL_DATAFRAME['Пар в классе'] = ALL_DATAFRAME.apply(lambda x: str(x['Место в классе']).split('/')[1], axis=1)
    ALL_DATAFRAME['Место в классе'] = ALL_DATAFRAME.apply(lambda x: str(x['Место в классе']).split('/')[0], axis=1)

    ALL_DATAFRAME['День'] = ALL_DATAFRAME.apply(lambda x: x['Дата'].split('.')[0], axis=1)
    ALL_DATAFRAME['Месяц'] = ALL_DATAFRAME.apply(lambda x: x['Дата'].split('.')[1], axis=1)
    ALL_DATAFRAME['Год'] = ALL_DATAFRAME.apply(lambda x: x['Дата'].split('.')[2], axis=1)

    ALL_DATAFRAME['Дата'] = ALL_DATAFRAME.apply(lambda x: str(x['Год'] + '-' + x['Месяц'] + '-' + x['День']), axis=1)
    ALL_DATAFRAME['Дата'] = pd.to_datetime(ALL_DATAFRAME['Дата'])
    ALL_DATAFRAME = ALL_DATAFRAME.sort_values(by='Дата')

    ALL_DATAFRAME = ALL_DATAFRAME.reset_index()
    ALL_DATAFRAME['Всего турниров'] = list(ALL_DATAFRAME.index)

    ALL_DATAFRAME['Ранг турнира'] = ALL_DATAFRAME.apply(lambda x: 'РС А' if 'РС А' in x['Статус']
    else ('РС В' if 'РС В' in x['Статус']
          else ('РС С' if 'РС С' in x['Статус']
                else '')), axis=1)

    ALL_DATAFRAME['ВС'] = ALL_DATAFRAME.apply(lambda x: 1 if 'ВС' in x['Статус'] else 0, axis=1)
    ALL_DATAFRAME['КС'] = ALL_DATAFRAME.apply(lambda x: 1 if 'КС' in x['Статус'] else 0, axis=1)
    ALL_DATAFRAME['ПФО'] = ALL_DATAFRAME.apply(lambda x: 1 if 'ПФО' in x['Статус'] else 0, axis=1)
    ALL_DATAFRAME['ЧР'] = ALL_DATAFRAME.apply(lambda x: 1 if 'ЧР' in x['Статус'] else 0, axis=1)
    ALL_DATAFRAME['КР'] = ALL_DATAFRAME.apply(lambda x: 1 if 'КР' in x['Статус'] else 0, axis=1)
    ALL_DATAFRAME['МС'] = ALL_DATAFRAME.apply(lambda x: 1 if 'МС' in x['Статус'] else 0, axis=1)

    ALL_DATAFRAME['Категория группы'] = ALL_DATAFRAME.apply(
        lambda x: 'Открытый класс' if ('Открытый' in x['Группа'] or not re.search('H|E|D|C|B|A', x['Группа']))
        else 'Закрытый класс', axis=1)
    ALL_DATAFRAME['Ранг группы'] = ALL_DATAFRAME.apply(lambda x: 'ВС' if ('ВС' in x['Группа'])
                                                            else 'КС' if ('КС' in x['Группа'] or 'Квалификационные' in x['Группа'])
                                                            else 'ПФО' if ('Приволжского Федерального' in x['Группа'])
                                                            else 'ЧР' if re.search('ЧР|ПР|Первенство России|Чемпионат России', x['Группа'])
                                                            else 'КР' if ('Кубок России' in x['Группа'])
                                                            else 'RS' if 'RS' in x['Группа']
                                                            else '', axis=1)

    ALL_DATAFRAME.to_csv(f"{sportsmen['Name']}/{sportsmen['Name']}.csv", sep='\t', encoding='utf-8', index=False)

driver.close()

directories = next(os.walk('.'))[1]
directories.remove('.idea')

for directory in directories:
    sportsmen_name = ' '.join(directory.split('_'))
    sportsmen_df = pd.read_csv(filepath_or_buffer=f"{directory}/{directory}_Данные.csv", sep='\t')
    
    date_of_birth = sportsmen_df['Дата рождения:'].tolist()[0].split('.')
    date_of_birth = datetime(day=int(date_of_birth[0]), month=int(date_of_birth[1]), year=int(date_of_birth[2]))
    sportsmen_age = datetime.now().year - date_of_birth.year

    partner_name = sportsmen_df['В паре с:'].tolist()[0].split()[1:3]
    names = list(map(lambda x: x if x.split('_')[:2] == partner_name else None, directories))
    list_name = list(filter(lambda x: x is not None, names))
    name = ''
    if len(list_name) == 0:
        continue
    else:
        name = list_name[0]
    partner_df = pd.read_csv(f"{name}/{name}_Данные.csv", sep='\t')

    date_of_birth = partner_df['Дата рождения:'].tolist()[0].split('.')
    date_of_birth = datetime(day=int(date_of_birth[0]), month=int(date_of_birth[1]), year=int(date_of_birth[2]))
    partner_age = datetime.now().year - date_of_birth.year
    
    if partner_age < sportsmen_age:
        partner_df['Рейтинг стандарт'] = sportsmen_df['Рейтинг стандарт']
        partner_df['Рейтинг латина'] = sportsmen_df['Рейтинг латина']
        partner_df['Рейтинг двоеборье'] = sportsmen_df['Рейтинг двоеборье']
        partner_df['Пар в рейтинге стандарта'] = sportsmen_df['Пар в рейтинге стандарта']
        partner_df['Пар в рейтинге латины'] = sportsmen_df['Пар в рейтинге латины']
        partner_df['Пар в рейтинге двоеборья'] = sportsmen_df['Пар в рейтинге двоеборья']
        
        partner_df.to_csv(f"{name}/{name}_Данные.csv", sep='\t', encoding='utf-8', index=False)
