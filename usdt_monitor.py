import sched
import time
import requests

schedule = sched.scheduler(time.time, time.sleep)


def get_current_avg_price():
    # define args
    url = 'https://api-otc.huobi.pro/v1/otc/trade/list/public?coinId=2&tradeType=1&currentPage=1' \
          '&payWay=&country=&merchant=0&online=1&range=0'
    headers = {'user-agent': ''}
    r = requests.get(url, headers=headers)

    # if request is failed
    if r.status_code != 200:
        return -1

    # parse price list
    try:
        data = r.json()['data']
        total = 0
        for d in data:
            total += d['price']
        avg = total / len(data)
        print(avg)
        return avg
    except Exception as e:
        print(e)
        return -1
    finally:
        enqueue_new_task()


def enqueue_new_task():
    delay_time = 3
    priority_time = 0
    schedule.enter(delay_time, priority_time, get_current_avg_price)


def start_cycle_runner():
    enqueue_new_task()
    schedule.run()


start_cycle_runner()
