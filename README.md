# Archytas Data Resolution Detection Demo
Small demo of using archytas to perform analysis on a dataset, leveraging the cartwright library. Can extract the date column, and geo columns from the dataset, and pass them into cartwright to detect geo and temporal resolutions of the data.

## Prereqs
tested with python 3.10
- install requirements:
    ```
    pip install -r requirements.txt
    ```

- download data:
    ```
    ./wget-20230628064657.sh -s
    ```

## Usage
```
python archy_data_demo.py
```