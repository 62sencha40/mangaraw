import requests
import os
from bs4 import BeautifulSoup
from concurrent import futures


DIRECTORY = "/Users/sencha/workspace/python/mangaraw/manga"
LOG_FILE = DIRECTORY + "/log.json"


def make_soup(url: str) -> BeautifulSoup:
    target = requests.get(url)
    soup = BeautifulSoup(target.text, "html.parser")

    return soup


def get_img(img_url: str, title: str, episode: str, get_as: str):
    res = requests.get(img_url)

    if os.path.exists(DIRECTORY + "/" + title) is False:
        os.mkdir(DIRECTORY + "/" + title)

    if os.path.exists(DIRECTORY + "/" + title + "/" + episode) is False:
        os.mkdir(DIRECTORY + "/" + title + "/" + episode)

    file = open(DIRECTORY + "/" + title + "/" + episode + "/" + get_as + ".jpg", "wb")
    file.write(res.content)
    file.close()

    print(res)
    print(os.path.getsize(DIRECTORY + "/" + title + "/" + episode + "/" + get_as + ".jpg"))


def get_episode(episode_url: str, title: str, episode: str):
    img_url = []
    page_num = 1
    soup = make_soup(episode_url)

    entry_content = soup.find_all("img", class_="aligncenter")
    for page in range(len(entry_content)):
        if page == 0:
            img_url.append(entry_content[page].get("src"))

        else:
            img_url.append(entry_content[page].get("data-src"))

    for url in img_url:
        get_img(url, title, episode, str(page_num))
        page_num += 1


def get_manga(url: str):
    episode_num = 1
    soup = make_soup(url)

    title = soup.find("h1", class_="entry-title").text
    table = soup.find(class_="table table-hover")

    episode_url_list = [url.get("href") for url in table.find_all("a")]
    episode_url_list.reverse()

    for episode_url in episode_url_list:
        get_episode(episode_url, title, str(episode_num))
        episode_num += 1


def thread_get_manga(url: str):
    future_list = []
    episode_num = 1

    executor = futures.ThreadPoolExecutor(8)
    soup = make_soup(url)

    title = soup.find("h1", class_="entry-title").text
    table = soup.find(class_="table table-hover")

    episode_url_list = [url.get("href") for url in table.find_all("a")]
    episode_url_list.reverse()

    for episode_url in episode_url_list:
        future = executor.submit(get_episode, episode_url, title, str(episode_num))
        future_list.append(future)

        episode_num += 1


def main():
    url = "https://manga1000.com/%e4%b9%85%e4%bf%9d%e3%81%95%e3%82%93%e3%81%af%e5%83%95%e3%82%92%e8%a8%b1%e3%81%95%e3%81%aa%e3%81%84-raw-free/"
    get_manga(url)


if __name__ == '__main__':
    main()