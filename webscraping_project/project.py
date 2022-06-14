import requests
from bs4 import BeautifulSoup
import re

def create_soup(url):
    res = requests.get(url)
    res.raise_for_status
    soup = BeautifulSoup(res.text, "lxml")
    return soup


def scrape_weather():
    print("[오늘의 날씨]")
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8"
    soup = create_soup(url)
    #흐림, 어제보다 OO° 높아요 
    cast = soup.find("p", attrs={"class":"summary"}).get_text()
    # 현재 OO° (최저 OO° / 최고 OO°)
    curr_temp = soup.find("div", attrs={"class":"temperature_text"}).get_text()
    min_temp = soup.find("span", attrs={"class":"lowest"}).get_text() # 체감 온도
    max_temp = soup.find("span", attrs={"class":"highest"}).get_text() # 
    
    # 오전 강수확룔 OO%° / 오후 강수확률 OO%°
    morning_rain_rate = soup.find("span", attrs={"class":"weather_left"}).get_text().strip()
    afternoon_rain_rate = soup.find_all("span", attrs={"class":"weather_left"})[2].get_text().strip()

    # 미세먼지
    dust = soup.find("ul", attrs={"class":"today_chart_list"})
    pm10 = dust.find_all("li")[0].get_text().strip() #미세먼지
    pm25 = dust.find_all("li")[1].get_text().strip()
    # 출력
    print(cast)
    print("현재 {} ({} / {})".format(curr_temp, min_temp, max_temp))
    print("{} / {}".format(morning_rain_rate, afternoon_rain_rate))
    print()
    print(pm10)
    print(pm25)
    print()

def scrape_headline_news():
    print("헤드라인 뉴스")
    url = "https://news.naver.com"
    soup = create_soup(url)
    news_list = soup.find("div", attrs={"class":"cjs_channel_card"}).find_all("div", attrs={"class":"cjs_journal_wrap _item_contents"})
    for index, news in enumerate(news_list):
        title = news.find("div", attrs={"class":"cjs_t"}).get_text()
        link = news.find("a")["href"]
        print("{}. {}".format(index+1, title))
        print("     (링크 :{})".format(link))  
        print()
    
def scrape_english():
    print("[오늘의 영어 회화")
    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english"
    soup = create_soup(url)

    sentences = soup.find_all("div", attrs={"id":re.compile("^conv_kor_t")})
    print("(영어지문)")
    for sentence in sentences[len(sentences)//2:]: # 8문장이 있다고 가정할 때, 5~8까지 잘라서 가져옴, index 기준 4~7 까지 잘라서
        print(sentence.get_text().strip())
    
    print()
    print("(한글 지문)")
    for sentence in sentences[:len(sentences)//2:]: # 8문장이 있다고 가정할 때, 5~8까지 잘라서 가져옴, index 기준 0~3 까지 잘라서
        print(sentence.get_text().strip())
        



if __name__ == "__main__":
    scrape_weather() # 오늘의 날씨 정보 가져오기
    scrape_headline_news()
    scrape_english() #오늘의 영어 회화 가져오기