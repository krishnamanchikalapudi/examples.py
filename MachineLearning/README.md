# Introduction
Machine Learning (ML) allows the user to feed a computer algorithm an immense amount of data and have the computer analyze and make data-driven recommendations and decisions based on only the input data.

Machine learning is made up of three parts:
* The computational algorithm at the core of making determinations.
* Variables and features that make up the decision.
* Base knowledge for which the answer is known that enables (trains) the system to learn.

Machine learning process at high level
1. Get data: collecting data from various sources
2. Clean, prepare, & manipulate data: Data cleaning feature engineering
3. Train model: Model building for selecting correct ML algorithm
4. Test data: Evaluate model
5. Improve: Improving the performance.

Broadly, there are 3 types of Machine Learning algorithms
1. Supervised Learning
   * [Linear Regression](docs/supervised/linear.md)
   * [Logistic Regression](docs/supervised/logistic.md)
   * [Decision Tree](docs/supervised/decision.md)
   * [Random Forest](docs/supervised/random.md)
   * [KNN](docs/supervised/knn.md)
2. Unsupervised Learning
   * [Apriori](docs/unsupervised/apriori.md)
   * [K-means](docs/unsupervised/kmeans.md)
3. Reinforcement Learning
   * [Markov Decision Process](docs/reinforcement/markov.md)

## Pre-requisite
- [X] Python 3.7 or higher
- [X] make
``````terminal
brew install make 
xcode-select --install
``````

## Source folder structure
`````
python
  |___ docs              --> Package reference documentation
  |___ src               --> Source code
  |___ tests             --> Package integration and unit tests
  |___ Makefile          --> Generic management tasks
  |___ requirements.txt  --> Development dependencies
  |___ setup.py          --> Package and distribution management
  |___ README.md
`````

## Code
#### Install
-[X] install from the given requirements file
`````
pip3 install -r requirements.txt
`````

-[X] compile
`````
python3 -m compileall -l ./src/
`````

-[X] unit test
`````
python3 -m unittest tests/util/UtilsTest.py
`````


## My Learnings
- [X] [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course/ml-intro)

## Data
- [X] [Company Ticker](https://www.sec.gov/files/company_tickers.json)
- [X] [Data distribution](https://www.sec.gov/data.json)
