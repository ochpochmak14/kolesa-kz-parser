from bs4 import BeautifulSoup
import requests
import pandas as pd


def correction_text(text: str) -> str:
    text = text.replace(" ", '-')
    return text.lower()


class Car:
    mark = None
    model = None
    city = None
    price1 = 1
    price2 = 900000000000

    def __init__(self, mark, model, city, price1, price2):
        self.mark = correction_text(mark)
        self.model = correction_text(model)
        self.city = correction_text(city)
        self.price1 = price1
        self.price2 = price2

    def print_data(self):
        car_options = {
            'mark': self.mark,
            'model': self.model,
            'city': self.city,
            'start_price': self.price1,
            'finish_price': self.price2,
        }
        print("Car options: ")
        print(car_options)


def get_data():
    mark = input("Enter mark of car: ")
    model = input("Enter model of car: ")
    city = input("Enter your city: ")
    price1 = int(input("Enter start price: "))
    price2 = int(input("Enter finish price: "))
    my_car = Car(mark, model, city, price1, price2)

    return my_car


def main_url(car: Car) -> str:
    mainurl = f"https://kolesa.kz/cars/{car.mark.lower()}/{car.model.lower()}/{car.city.lower()}/?price%5Bfrom%5D={car.price1}&price%5Bto%5D={car.price2}&sort_by=year-desc" #&page={page}
    return mainurl


def get_html(url: str):
    _html = requests.get(url).text
    soup = BeautifulSoup(_html, 'lxml')
    return soup


def get_number_of_pages(soup) -> int:
    try:
        soup2 = soup.find('div', class_="paginator clearfix")
        pages = soup2.find_all('li')
    except AttributeError:
        return int(1)
    else:
        return int(pages[len(pages) - 1].text)


def parser(page_amount: int, main_url: str) -> None:

    my_data = []
    for page in range(1, page_amount):
        url1 = main_url + f"&page={page}"
        my_response = requests.get(url1).text
        my_soup = BeautifulSoup(my_response, 'lxml')
        cars = my_soup.find_all('div', class_="a-list__item")

        for car in cars:
            try:
                year = str(car.find('p', class_="a-card__description").text)
                price = car.find('span', class_="a-card__price").text
                link = car.find('a', class_="a-card__link").get('href')
                dataa = car.find('span', class_="a-card__param a-card__param--date").text

                my_soup2 = get_html("https://kolesa.kz/" + str(link))
                item_name = my_soup2.find('span', itemprop="brand").text

                pok = my_soup2.find('dt', title="Поколение")

                generation = pok.find('dd', class_="value").text

                my_data.append([item_name, year, price, generation, link])

            except AttributeError:
                pass

    df = pd.DataFrame(my_data, columns=['TITLE', 'YEAR', 'PRICE', 'GENERATION', 'LINK'])
    print(df)


def main():
    try:
        car = get_data()
        mainurl = main_url(car)
        souup = get_html(mainurl)
        number_pages = get_number_of_pages(souup)
        parser(number_pages, mainurl)
    except Exception:
        print("--- Check your car characteristics) ---")


main()
