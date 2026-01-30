# Creating Math Problems With LLM

## Creating Dataset

In this project we are able to create a set of valid math problems for Grade 3 and 4 students in Germany.

To run the code, clone this repository and create a virtual environment:

``` python -m venv .venv  ```

Then activate the virtual environment (this works for Linux systems):

``` source .venv/bin/activate  ```

Load the necessary dependancies:

``` pip install -r requirements.txt  ```

Now the code is ready to run:

``` python create_dataset.py <model> <grade> <num_problems> ```

The most up to date resulting dataset can be found inside of problems/version_2.

For more details about the API calls, and the actual prompt take a look at our code.

## Results Analysis

We have attached the R code, for the analysis of the results along with the results of the survey that we obtained (user_study_results.xlsx)
