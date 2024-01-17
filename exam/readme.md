
# Moodle Exam Processing Guide

This guide provides instructions for processing Moodle exam files and organizing them by marker.

## Overview
The tool processes Moodle exam files and creates a directory for each marker, facilitating the evaluation process.

## Steps to Follow
1. **Configure Settings:**
   - Rename `config.ini-template` to `config.ini`.
   - Update the fields in `config.ini` as needed.

2. **Retrieve Data:**
   - Download the necessary data from Moodle.

3. **Organize Data:**
   - Place all downloaded data in the directory specified in `config.ini` (under 'files', 'data' element).

4. **Execute Script:**
   - Run `main.py` to process and organize the data.

## Moodle Download Settings

Configure your Moodle export with these settings:

| Setting                    | Value               |
|----------------------------|---------------------|
| Set folder hierarchy       | Essay question wise |
| Include text response file | Yes                 |
| Include question text file | Yes                 |

## Configuration Parameters

Configure the `config.ini` file using the following format:

| Group  | Field         | Description                                          | Default            |
|--------|---------------|------------------------------------------------------|-------------------:|
| grades | file          | Excel file with student and marker data              |                    |
| grades | worksheet     | Worksheet name in the *grades.files* file            | Final Exam         |
| grades | header        | Number of header lines (0-indexed)                   | 0                  |
| files  | data          | Directory with all student submissions               | data               |
| files  | output        | Directory for submissions sorted by marker           | markers            |
| files  | overview      | Excel file summarizing the process                   | overview.xlsx      |
| files  | not_processed | Excel file listing students without submissions      | not_processed.xlsx |
| files  | min_length    | Minimum length of text in a exam to make it count    | 50                 |
