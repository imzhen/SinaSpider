import weibo_login
import weibo_parser
import write_to_csv

if __name__ == '__main__':
    username_m = input("username: ")
    password_m = input("password: ")
    login = weibo_login.WeiboLogin("imzhenr@gmail.com", "910808pps")
    session = login.login()
    parser = weibo_parser.WeiboParser(session, "http://weibo.cn/qiurilushi")
    user_info, tweet_info_total = parser.loop_through_page()
    writer = write_to_csv.WriteToCsv(tweet_info_total, "test.csv")
    writer.write_to_csv()
