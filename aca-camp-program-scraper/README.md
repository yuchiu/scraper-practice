# ACA-Camp-Program-Scraper

## Quick Links

[Directory Structure](#Directory-Structure)

[Workflow Diagram](#Workflow-Diagram)

[Getting Started](#Getting-Started)

- [Tools & Versions](#Tools-&-Versions)
- [Prerequisites](#Prerequisites)
- [Running Application](#Running-Application)

## Directory Structure

```
root
├───.env
├───.gitignore
├───requirements.txt
├───README.md
├───launcher.sh
└───apps
    ├───main.py
    ├───data-fetcher
    ├───data-deduper
    └───common
```

| **root directory** | **descriptions**                |
| ------------------ | ------------------------------- |
| .env               | global env variables            |
| .gitignore         | files ignored by git            |
| requirements.txt   | project dependency list         |
| README.md          | project's documentations        |
| launcher.sh        | shell script to launch pipeline |
| apps               | application files               |

| **apps directory** | **descriptions**                         |
| ------------------ | ---------------------------------------- |
| main.py            | project's initializer                    |
| data-fetcher       | handles fetching tasks                   |
| data-deduper       | handles deduping tasks                   |
| common             | common files share across apps directory |

---

## Workflow Diagram

![data-flow-img](https://github.com/sleepawaycamper/Data-Pipeline/blob/master/data-flow.png)

---

## Getting Started

### Tools & Versions

| Tools    | Versions  |
| -------- | --------- |
| python3  | 3.6.7     |
| pip3     | 9.0.1     |
| postgres | 10.5      |
| rabbitmq | cloudAMQP |

### Prerequisites

- **!important** .env file is required for setting up environment variables.

- cloudAMQP service API in .env file is registered by personal account therefore could be removed in the future, register your own cloudAMQP service API with the [link](https://www.cloudamqp.com/).

- cloudAMQP service free tier limit 1,000,000 message queue per month.

- Postgres database & authorization needs to be setup before running the application.  
  default database name in .env is: sleepaway_camper  
  default database username in .env is: postgres(Postgres's default username)  
  default database password in .env is: postgres(Postgres's default password)

### Running Application

- install dependencies

```terminal
cd Data-Pipeline
pip3 install -r requirements.txt
```

- Option A. shell script to start data pipeline

```terminal
sh launcher.sh
```

- Option b. start each service individually

```terminal
python3 main.py
```

```terminal
python3 data-fetcher/fetcher.py
```

```terminal
python3 data-deduper/deduper.py
```

---
