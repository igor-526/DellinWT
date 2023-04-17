import csv
from datetime import datetime

async def log(id, task, params):
    with open(f'logs/{str(id)}.csv', mode="a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
        file_writer.writerow([str(datetime.now().strftime("%d.%m %H:%M:%S")), f'{str(task)}', f'{str(params)}'])