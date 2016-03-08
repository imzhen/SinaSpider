import bs4
import re


class WeiboParser:

    def __init__(self, session, url):
        self.session = session
        self.initial_url = url
        self.id = self.initial_url.split("/")[-1]

    def loop_through_page(self):
        soup = bs4.BeautifulSoup(self.session.get(self.initial_url).text, "html.parser")
        user_info = self.parse_user_info(soup)

        total_page = soup.find_all("input")[0]["value"]
        tweets_info_total = []

        current_page = 1
        while current_page <= int(total_page):
            tweets_info_total += self.extract_info(self.initial_url + "?page=" + str(current_page))
            print(current_page)
            current_page += 1

        return user_info, tweets_info_total

    def extract_info(self, url):
        soup = bs4.BeautifulSoup(self.session.get(url).text, "html.parser")
        tweets = soup.find_all('div', class_='c')

        tweet_info_subtotal = []

        for tweet in tweets:
            try:
                tweet_id = tweet["id"]
                divs = tweet.find_all('div')
                divs_len = len(divs)
                if divs_len == 1:
                    tweet_info = self.parse_no_fwd_no_pic(divs)
                elif divs_len == 2:
                    fwd_check = divs[0].find_all('span', class_='cmt')
                    if fwd_check:
                        tweet_info = self.parse_fwd_no_pic(divs)
                    else:
                        tweet_info = self.parse_no_fwd_pic(divs)
                elif divs_len == 3:
                    tweet_info = self.parse_fwd_pic(divs)
                tweet_info["id"] = tweet_id
                tweet_info_subtotal.append(tweet_info)
            except KeyError:
                pass

        return tweet_info_subtotal

    def parse_user_info(self, soup):
        user_info = soup.find_all("div", class_='ut')[0]
        basic = list(user_info.children)[0].get_text()
        basic = basic.replace(u'\xa0', u' ')
        [name, sex_and_location] = basic.split(" ")[0:2]
        [sex, location] = sex_and_location.split("/")

        user_social_info = soup.find_all("div", class_='tip2')[0]
        total_weibo, connect, fans = self.parse_social_info(user_social_info)
        return {"id": self.id, "name": name, "sex": sex, "location": location,
                "total_weibo": total_weibo, "connection": connect, "fans": fans}

    @staticmethod
    def parse_social_info(social_info):
        [like, forward, comment] = [item[1:-1] for item in re.findall(r'\[\d+\]', social_info.get_text())][:3]
        return like, forward, comment

    @staticmethod
    def parse_time_device_info(time_device_info):
        time, device = time_device_info.split("\xa0")
        return time, device[2:]

    def parse_no_fwd_no_pic(self, divs):
        main_text = divs[0].find_all('span')[0].get_text()
        time_device_info = divs[0].find_all('span')[1].get_text()
        time, device = self.parse_time_device_info(time_device_info)
        social_info = divs[0].find_all('a', class_="cc")[0].parent
        like, forward, comment = self.parse_social_info(social_info)
        return {"text": main_text, "like": like, "forward": forward,
                "comment": comment, "time": time, "device": device, "initial": True}

    def parse_no_fwd_pic(self, divs):
        main_text = divs[0].find_all('span')[0].get_text()
        time_device_info = divs[1].find_all('span')[0].get_text()
        time, device = self.parse_time_device_info(time_device_info)
        social_info = divs[1].find_all('a', class_="cc")[0].parent
        like, forward, comment = self.parse_social_info(social_info)
        return {"text": main_text, "like": like, "forward": forward,
                "comment": comment, "time": time, "device": device, "initial": True}

    def parse_fwd_no_pic(self, divs):
        main_text = divs[1].find_all('span')[0].nextSibling
        time_device_info = divs[1].find_all('span')[1].get_text()
        time, device = self.parse_time_device_info(time_device_info)
        social_info = divs[1].find_all('a', class_="cc")[0].parent
        like, forward, comment = self.parse_social_info(social_info)
        return {"text": main_text, "like": like, "forward": forward,
                "comment": comment, "time": time, "device": device, "initial": False}

    def parse_fwd_pic(self, divs):
        main_text = divs[2].find_all('span')[0].nextSibling
        time_device_info = divs[2].find_all('span')[1].get_text()
        time, device = self.parse_time_device_info(time_device_info)
        social_info = divs[2].find_all('a', class_="cc")[0].parent
        like, forward, comment = self.parse_social_info(social_info)
        return {"text": main_text, "like": like, "forward": forward,
                "comment": comment, "time": time, "device": device, "initial": False}
