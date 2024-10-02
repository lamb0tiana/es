# Scripts:
This contains 3 apps:
* __The csv puller__

_This pull remote ftp client csv and handle by ELK._

run and edit .env file:

```
cd puller && cp .env.dist .env
```



_define cron in :_ __./puller/csv_puller__

```
0 2 * * * /bin/bash /script/puller.sh >> /var/log/pull_csv_$(date +\%Y-\%m-\%d_\%H-\%M).log 2>&1

```

_**Note: For now, it is only based on the riester CSV format (tab as the separator; the unnecessary first line needs to be removed._**


* __The matching_data script__

_This create a contact or set set exist contact in Elasticsearch periodically._

run and edit .env file:
```
cd app && cp .env.dist .env
```

_to defined cron, edit __./app/cron___

```
0 3 * * * /usr/local/bin/python3 /app/app.py >> /var/log/matching_data_$(date +\%Y-\%m-\%d_\%H-\%M).log 2>&1

```

* __Contact api webservice__


_go to_ http://localhost:8000/docs

