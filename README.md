# Legislative Data Processor

A Python application that processes publicly available government data to analyze legislator voting patterns on bills.

## Overview

This project collects and organizes legislative data to provide insights into how legislators vote on bills. It processes data about:
- **Person**: Individual legislators (e.g., President Joe Biden, Representative David McKinley)
- **Bill**: Pieces of legislation introduced in the United States Congress
- **Vote**: Votes on particular bills
- **VoteResult**: Individual votes cast by legislators for or against legislation


## Docker Setup
Build the Docker image:

```
docker compose build
```

### Docker Execution
```
docker compose up
docker run --rm -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output legislative-data-processor
```

## Dependencies

- `pandas==3` - For CSV processing and data manipulation