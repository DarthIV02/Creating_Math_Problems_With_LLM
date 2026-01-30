# Creating_Math_Problems_With_LLM

In this project we are able to create a set of valid math problems for Grade 3 and 4 students in Germany.

To run the code, clone this repository and create a virtual environment:

``` python -m venv .venv  ```

Then activate the virtual environment (this works for Linux systems):

``` source .venv/bin/activate  ```

Load the necessary dependancies:

``` pip install -r requirements.txt  ```

Now the code is ready to run:

``` python create_dataset.py <model> <grade> <num_problems> ```

For more details, take a look at our code.