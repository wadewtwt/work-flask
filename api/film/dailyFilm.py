import requests
from bs4 import BeautifulSoup
import re
from film import addFilmSql
from common.mysql_operate import db

def newestMovieWork():
    url = 'https://movie.douban.com/chart'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    items = soup.find_all('tr', class_='item')
    for item in items:
        a_img = item.find('img')
        imgText = a_img.attrs['src']

        movies = soup.find_all('div', class_='pl2')
        for movie in movies:
            a_tag = movie.find('a')
            hrefText = a_tag.get('href')
            titleText = ''
            for elem in a_tag.contents:
                if elem.name != 'span':
                    titleText += str(elem).strip().replace(" ", "").replace("/", "").replace("\n", "")
            ratingText = movie.find('span', class_='rating_nums').text.strip()

            print(f'Title: {titleText}, Rating: {ratingText}, hrefText:{hrefText}, imgText:{imgText}')
            addFilmSql(titleText, imgText, hrefText, ratingText, "",0, "", 0, 0, 0);



if __name__ == '__main__':
    db.change_db(1)
    newestMovieWork()
