# Intro MLOps

## Notebook
- churn_prediction.ipynb

## Homework 
### problem
<ol>
<li>Based on the model that you built in the workshop, create a working inference service (Docker container).</li>
<li>The service answers to the  /predict call</li>
<li>The service will get data in JSON format 
    <ul>
        <li>you can use pandas .to_json for the input. 
        <li>example - df.sample(1).to_json(orient='records')
    </ul>
</li>
<li>It will respond with the churn probability</li>
<li>Bonus:
    <ul>
        <li>Support a batch of requests</li>
        <li>Use artifactory to save your trained model</li>
        <li>Use artifactory for your built container</li>
    </ul>
</li>
</ol>

### Solution
- Update [notebook](churn_prediction.ipynb) 
`````
xgb.save_model
`````
- Flask API in the [solution[(solution)] folder 