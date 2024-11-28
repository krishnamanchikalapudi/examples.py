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

## References
- [xgboost_customer_churn](https://sagemaker-examples.readthedocs.io/en/latest/introduction_to_applying_machine_learning/xgboost_customer_churn/xgboost_customer_churn_outputs.html)
- Source code: [https://github.com/aws/amazon-sagemaker-examples/tree/main/introduction_to_applying_machine_learning/xgboost_customer_churn](https://github.com/aws/amazon-sagemaker-examples/tree/main/introduction_to_applying_machine_learning/xgboost_customer_churn)