
# Moodle Forum Processing Guide

This guide outlines the process for generating an overview of student posts in Moodle forums, which is particularly useful for forums where students are graded based on their participation.

## Overview
The tool processes files exported from Moodle forums and compiles an overview of each student's posts. This is helpful for assessing participation in forums where posts contribute to student grades.

## Configuration Steps
1. **Prepare Configuration File:**
   - Duplicate the `config.ini-template` file.
   - Rename the copy to `config.ini`.
   - Update the fields in `config.ini` as required.

2. **Process Each Moodle Forum:**
   - For every forum, follow these steps:
     1. Retrieve the relevant data from Moodle.
     2. Save the exported data to the location specified in the `config.ini` file (under the 'forum.' section, 'file' element).

3. **Run the Script:**
   - Execute `main.py` to process the data.

## Export Settings for Moodle Forums

When exporting data from a Moodle forum, use the following settings:

| Setting              | Value                     |
| -------------------- | ------------------------- |
| Users                | All users (default)       |
| Discussions          | All discussions (default) |
| Format               | CSV (default)             |
| Remove HTML          | Yes                       |
| Human-readable dates | Yes                       |

## Configuration File Format

The `config.ini` file should be structured as follows:

| Group    | Field       | Description                                         | Default            |
| -------- | ----------- | --------------------------------------------------- | ------------------ |
| students | file        | Excel file with student and marker data             |                    |
| students | worksheet   | Worksheet name with 'participation' information     | Participation      |
| output   | file        | Excel file for the compiled results                 | participation.xlsx |
| forum.*  | title       | Title for the worksheet description                 | (none)             |
| forum.*  | description | Description of the forum for the 'readme' worksheet | (none)             |
| forum.*  | file        | CSV file containing forum postings                  | (none)             |

### Note:
- Each forum configuration block should start with `forum.` followed by a unique identifier.
- The part after `forum.` is for human readability and does not affect the processing.

## Configuration Example

Here is an example of how to configure the `config.ini` file for two forums:

```ini
[forum.1]
title = P-1
description = "Session 4 - Creating Money"
file = discussion-1.csv

[forum.2]
title = P-2
description = "Session 6 - Securitization"
file = discussion-2.csv
```
