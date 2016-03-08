import csv
import os


class WriteToCsv:

    def __init__(self, tweet_info_total, file_path):
        self.tweet_info_total = tweet_info_total
        self.file_path = os.path.join(os.path.dirname(__file__), file_path)

    def write_to_csv(self):
        with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, self.tweet_info_total[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(self.tweet_info_total)
