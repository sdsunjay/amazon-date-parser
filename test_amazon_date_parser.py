import unittest
from datetime import datetime
from amazon_date_parser import amazon_date_parser

class TestAmazonDateParser(unittest.TestCase):

    def test_amazon_date_parser(self):
        test_dates = [
        "2015-11-24",
        "2022-03-24",
        "2015-11-25",
        "2015-11-25",
        "2015-11-30",
        "2023-W1",
        "2023-W2",
        "2022-W48",
        "2021-W49",
        "2015-W48-WE",
        "2022-W43-WE",
        "2023-W10-WE",
        "2015-11",
        "2016",
        "201X",
        "2017-WI",
        "2019-WI",
        "2015-WI",
        "2022-WI",
        "2022-SP",
        "2023-SP",
        "2023-SU",
        "2023-FA",
        "2015-11-24"
        ]


        expected_outputs = [
        {'startDate': datetime(2015, 11, 24, 0, 0), 'endDate': datetime(2015, 11, 24, 23, 59, 59, 999999)},
        {'startDate': datetime(2022, 3, 24, 0, 0), 'endDate': datetime(2022, 3, 24, 23, 59, 59, 999999)},
        {'startDate': datetime(2015, 11, 25, 0, 0), 'endDate': datetime(2015, 11, 25, 23, 59, 59, 999999)},
        {'startDate': datetime(2015, 11, 25, 0, 0), 'endDate': datetime(2015, 11, 25, 23, 59, 59, 999999)},
        {'startDate': datetime(2015, 11, 30, 0, 0), 'endDate': datetime(2015, 11, 30, 23, 59, 59, 999999)},
        {'startDate': datetime(2023, 1, 2, 0, 0), 'endDate': datetime(2023, 1, 8, 23, 59, 59, 999999)},
        {'startDate': datetime(2023, 1, 9, 0, 0), 'endDate': datetime(2023, 1, 15, 23, 59, 59, 999999)},
        {'startDate': datetime(2022, 11, 28, 0, 0), 'endDate': datetime(2022, 12, 4, 23, 59, 59, 999999)},
        {'startDate': datetime(2021, 12, 6, 0, 0), 'endDate': datetime(2021, 12, 12, 23, 59, 59, 999999)},
        {'startDate': datetime(2015, 12, 5, 0, 0), 'endDate': datetime(2015, 12, 6, 23, 59, 59, 999999)},
        {'startDate': datetime(2022, 10, 29, 0, 0), 'endDate': datetime(2022, 10, 30, 23, 59, 59, 999999)},
        {'startDate': datetime(2023, 3, 11, 0, 0), 'endDate': datetime(2023, 3, 12, 23, 59, 59, 999999)},
        {'startDate': datetime(2015, 11, 1, 0, 0), 'endDate': datetime(2015, 11, 30, 23, 59, 59, 999999)},
        {'startDate': datetime(2016, 1, 1, 0, 0), 'endDate': datetime(2016, 12, 31, 23, 59, 59, 999999)},
        {'startDate': datetime(2010, 1, 1, 0, 0), 'endDate': datetime(2019, 12, 31, 23, 59, 59, 999999)},
        {'startDate': datetime(2017, 12, 1, 0, 0), 'endDate': datetime(2017, 2, 28, 23, 59, 59)},
        {'startDate': datetime(2019, 12, 1, 0, 0), 'endDate': datetime(2019, 2, 28, 23, 59, 59)},
        {'startDate': datetime(2015, 12, 1, 0, 0), 'endDate': datetime(2015, 2, 28, 23, 59, 59)},
        {'startDate': datetime(2022, 12, 1, 0, 0), 'endDate': datetime(2022, 2, 28, 23, 59, 59)},
        {'startDate': datetime(2022, 3, 1, 0, 0), 'endDate': datetime(2022, 5, 31, 23, 59, 59)},
        {'startDate': datetime(2023, 3, 1, 0, 0), 'endDate': datetime(2023, 5, 31, 23, 59, 59)},
        {'startDate': datetime(2023, 6, 1, 0, 0), 'endDate': datetime(2023, 8, 31, 23, 59, 59)},
        {'startDate': datetime(2023, 9, 1, 0, 0), 'endDate': datetime(2023, 11, 30, 23, 59, 59)},
        {'startDate': datetime(2015, 11, 24, 0, 0), 'endDate': datetime(2015, 11, 24, 23, 59, 59, 999999)}
        ]

        for i in range(len(test_dates)):
            with self.subTest(date=test_dates[i]):
                self.assertEqual(amazon_date_parser(test_dates[i]), expected_outputs[i])

if __name__ == '__main__':
    unittest.main()
