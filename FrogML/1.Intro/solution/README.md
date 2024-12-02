# Solution: Churn Prediction Service



## BUILD
### Script
#### Compile and UnitTest
`````
./api.sh SRC
`````
#### Flask Service and Test Api
`````
./api.sh API-TEST
`````

### Step-By-Step
#### install from the given requirements file
`````
pip install -r requirements.txt
`````

#### compile
``````````
python -m compileall -l ./
``````````

#### unit test
`````
python3 -m unittest tests/ApiTest.py 
`````

#### Run Api
`````
flask --app src/PredictApi.py run
`````

#### TEST Api
`````
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:5000/     
`````

## Docker
### Build container
`````
docker image build -f Dockerfile -t frogml-churn-predict:latest .
`````
### Run container
`````
docker run -p 5000:5000 frogml-churn-predict:latest
`````
### Test container service
`````
curl -X POST -H "Content-Type: application/json" -d '[{"feature1": 0.5, "feature2": 1.2, "feature3": 3.4}]' http://localhost:5000/predict
`````


## References
- [Python Module](https://docs.python.org/3/py-modindex.html)
- [Python unitests](https://docs.python.org/3/library/unittest.html#module-unittest)