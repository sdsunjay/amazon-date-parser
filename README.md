
# Amazon Date Parser
[AMAZON.DATE](https://developer.amazon.com/en-US/docs/alexa/custom-skills/slot-type-reference.html#date) slot normalizer in Python3

## Introduction
This Python script, `amazon_date_parser.py`, is designed to parse and extract date information from the Amazon Alexa Date slot type. It processes and converts date strings into UTC datetime objects. It handles various formats including specific cases like ISO week numbers, simple YYYY-MM-DD dates, and more complex scenarios involving partial date strings. This script is particularly useful for applications requiring accurate date computations across different timezones, such as data parsing for Amazon Alexa Date slot.

## Requirements
- Python 3.6+
- `pytz` for timezone calculations

## Installation
To use this script, ensure Python is installed on your machine. Install the necessary Python library using pip:

```bash
pip install pytz
```

## Usage
The script includes several functions to handle date parsing and timezone conversions. Below are examples of how to use the script to parse different types of date strings:

```python
from amazon_date_parser import amazon_date_parser

# Parsing a simple date string
simple_date = amazon_date_parser('2023-05-14', 'America/Los_Angeles')
print(simple_date)

# Parsing an ISO week date string
iso_week_date = amazon_date_parser('2023-W20', 'America/Phoenix')
print(iso_week_date)

# Parsing a year and season date string
iso_season_date = amazon_date_parser('2022-SP', 'Europe/Amsterdam')
print(iso_season_date)
```

Adjust the import statement based on your project structure.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
