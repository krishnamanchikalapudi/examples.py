# Solution: Churn Prediction Service



## BUILD
#### install from the given requirements file
`````
pip install -r requirements.txt
`````
## compile
``````````
python -m compileall -l ./
``````````
#### unit test
`````
python3 -m unittest tests/ApiTest.py 
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



## TEST
