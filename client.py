from time import sleep

from module.browser_worker import Browser
from module.data_objtects import Account, Post
from module.data_objtects import Database

delay_in_hours = 2


def main():
    db = Database()
    account = Account(*db.selectone('select * from accounts'))
    with Browser(account) as worker:
        worker_logined = worker.login()
        if worker_logined:
            while True:
                worker.tweet(Post())
                worker.home_page()
                sleep(60 * 60 * delay_in_hours)
                # sleep(5)


if __name__ == '__main__':
    main()
