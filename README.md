# Legislative Data Processor

A Python application that processes publicly available government data to analyze legislator voting patterns on bills.

## Overview

This project collects and organizes legislative data to provide insights into how legislators vote on bills. It processes data about:
- **Person**: Individual legislators (e.g., President Joe Biden, Representative David McKinley)
- **Bill**: Pieces of legislation introduced in the United States Congress
- **Vote**: Votes on particular bills
- **VoteResult**: Individual votes cast by legislators for or against legislation

## Project Structure
```
legislative_data/
├── README.md
├── requirements.txt
├── Dockerfile
├── writeup.md # Explanation of design choices and assumptions
├── data/ # Input CSV files
│ ├── legislators.csv
│ ├── bills.csv
│ ├── votes.csv
│ └── vote_results.csv
├── output/ # Generated output files
│ └── legislators-support-oppose-count.csv
│ └── bills.csv
└── src/
└── tests/
├── init.py
├── models.py # Data models
├── data_loader.py # CSV reading logic
├── processor.py # Business logic
├── writer.py # CSV output logic
└── main.py # Entry point
```

## Docker Setup
Build the Docker image:
```
docker compose build
```
### Docker Execution
```
docker compose up
```

### Run Tests
```
docker-compose run --rm processor pytest tests/ -v
```

### Run Pylint
```
docker-compose run --rm processor pylint src/ --output-format=colorized
```

## Data Schema

### Input Files

**legislators.csv**
- `id` (integer): The id of the legislator
- `name` (string): The name of the legislator

**bills.csv**
- `id` (integer): The id of the bill
- `title` (string): The name of the bill
- `Primary Sponsor` (integer): The id of the primary sponsor (of type Person)

**votes.csv**
- `id` (integer): The id of the Vote
- `bill_id` (integer): The id of the bill that this vote is associated with

**vote_results.csv**
- `id` (integer): The id of the VoteResult
- `legislator_id` (integer): The id of the legislator casting a vote
- `vote_id` (integer): The id of the Vote associated with this cast
- `vote_type` (integer): The type of vote cast - 1 for yea and 2 for nay

### Output Files

**legislators-support-oppose-count.csv**
- `id` (integer): The id of the legislator
- `name` (string): The name of the legislator
- `num_supported_bills` (integer): The number of bills the legislator voted Yea on
- `num_opposed_bills` (integer): The number of bills the legislator voted Nay on

**bills.csv**
- `id` (integer): The id of the bill
- `title` (string): The title of the bill
- `supporter_count` (integer): The number of legislators that supported this bill in the vote for it
- `opposer_count` (integer): The number of legislators that opposed this bill in the vote for it
- `primary_sponsor` (string): The name of the primary sponsor of the bill. If the name of the sponsor is not available in the dataset, the cell will be "Unknown"

## Dependencies

- `python==3.11`
- `pandas==3` - For CSV processing and data manipulation
- `pydantic==2.12.5` - For data validation and modeling