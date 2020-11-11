import time
import csv
import sys
import analyser, db


DB_NAME = 'domains.db'
API_KEY = '2f5ddcfa438447c3a7abf438451754918fc5c53d4a5a2122a2fcd777a574e562'
TIME_DIFF = 30 * 60


def read_csv(csv_path):
    with open(csv_path, newline='') as csvfile:
        rows = [r[0] for r in csv.reader(csvfile)]
    return rows


class Domain:
    def __init__(self, api_key, db_name):
        self.url_data = analyser.UrlData(api_key)
        self.domain_db = db.DB(db_name)

    def check_domain_csv(self, csv_path):
        domains = read_csv(csv_path)
        for domain in domains:
            verdict = self.check_domain(domain)
            print(f"Domain: {domain} is {verdict}")

    def check_domain(self, domain_name):
        res = self.domain_db.get_domain_risk_verdict(domain_name)
        to_insert = False # not in db
        if res is None:
            to_insert = True # in db need to update
        else:
            insert_time = res[1]
            if insert_time + TIME_DIFF > time.time():
                return res[0]  # return verdict
        # pull data

        json = self.url_data.get_data(domain_name)
        categories = analyser.ResponseAnalyzer.get_categories(json)
        votes, verdict = analyser.ResponseAnalyzer.get_votes_and_verdict(json)
        timestamp = analyser.ResponseAnalyzer.get_utc_time(json)

        if to_insert:
            self.domain_db.insert_domain_verdict(domain_name, verdict, timestamp)
            self.domain_db.insert_domain_categories(domain_name, categories)
            self.domain_db.insert_domain_votes(domain_name, votes)
        else:
            self.domain_db.update_domain_verdict(domain_name, verdict, timestamp)
            self.domain_db.update_domain_categories(domain_name, categories)
            self.domain_db.update_domain_votes(domain_name, votes)
        return verdict


if __name__ == "__main__":
    if len(sys.argv) > 1:
        d = Domain(API_KEY, DB_NAME)
        #d.check_domain_csv('domains.csv')
        d.check_domain_csv(sys.argv[1])
        d.domain_db.conn.close()
    else:
        print("Please specify csv file...")