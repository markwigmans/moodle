
# Moodle Essay Assignment Processing Guide

This guide details the process for handling Moodle essay assignment files and organizing them by marker.

## Overview
The tool is designed to process files from Moodle essay assignments and create a separate directory for each marker's submissions.

## Steps to Follow
1. **Configuration Setup:**
   - Copy `config.ini-template` to `config.ini`.
   - Modify the fields in `config.ini` as required.

2. **Data Retrieval:**
   - Download the necessary data from the Moodle assignment.

3. **Data Organization:**
   - Transfer all downloaded data to the directory defined in `config.ini` (under 'files', 'data').

4. **Script Execution:**
   - Run `main.py` to process the data and organize it by marker.

## Moodle Download Instructions
To download submissions for a specific assignment, follow these steps:

1. Navigate to the assignment on Moodle.
2. Click on 'View all submissions'.
3. Select 'Download all submissions'.

## Configuration Parameters

Structure the `config.ini` file using the following settings:

| Group  | Field         | Description                                              | Default            |
|--------|---------------|----------------------------------------------------------|-------------------:|
| grades | file          | Excel file with student and marker data                  | grades.xlsx        |
| grades | worksheet     | Worksheet name in the *grades.files* file                | Essay Assignment   |
| grades | header        | Number of header lines (0-indexed)                       | 0                  |
| grades | id_offset     | Offset for the reference number prefix                   | 1                  | 
| files  | data          | Directory with all student submissions                   | data               |
| files  | output        | Directory for organized submissions by marker            | markers            |
| files  | overview      | Excel file summarizing the process                       | overview.xlsx      |
| files  | not_processed | Excel file listing students without submissions          | not_processed.xlsx |
| files  | refnr_length  | Length of the file prefix number                         | 2                  |
