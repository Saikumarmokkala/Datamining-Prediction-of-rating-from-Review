# DM_Term_Project
Data Mining Term Project
Below are deployment steps for creating a web application using AmazonAWS endpoint
There are many way we can deploy the model and create an web app but today we will learn how to deploy a model in Amazon Web Services.
Before we proceed further let me tell you the reason why I choose AWS. AWS provides you with a very robust network and the downtime of AWS is almost 0 hence I choose AWS.

Let me now tell you the broad Idea on how we will procced towards building application.

We will deploy the model in aws which after running some aws script will give us an endpoint.(API endpoint)
Once we have an endpoint it very simple, we will just need an html and javascript code which will perform POST method call to our API (sending review text to be predicted) and the recieve a response which will have our predeicted rating.
To achieve above steps we have will be creating JOBLIB file for our model. For people who dont understand what JOBLIB file is just think it of as a briefcase which contains all the information which we have proccesed till now and which is very easy to carry. Now we will deploy the JOBLIB file in AWS Sagemaker. AWS Sagemaker is amazon wing for DATA processing works. To deploy this JOBLIB file there is a very basic amazon scipt that can be found in AWS document which link will be given below.

Once you run that code you model will be deployed and an ENDPOINT will be created where you can send your Review Text and rating will be given out in response.

After creating endpoint in sagemaker you can only use the endpoint or API call from sagemaker environment only. But this doest help us in creating our web app hence we need to make a way do that our endpoint can be contacted from outside of AWS environemnt. To do so we have to follow these steps.

Create a lambda function in AWS and make a connection from the function to our sagemaker endpoint
Create a API in AWS API Gateway Console which will have capabailities of POST method and will be invoking our lambda function.
Once the above steps are done we will have Link ready to which if we send an request with our review text we will get rating as response.

I have done the above steps and the code for lambda function is given in repo.


Now we have done most of the heavy work We just will create an HTML Page which will have have an input box and once user Enters text and clicks button we will send the text to our API and will show the response to the user.








So are you ready to try out the web app ????

I know your are :) Please click here (http://saikumarreddymokkala.uta.cloud/predict.html) to try out the app. Please remember to give in reviews as normal human :P so that you will get good rating prediction.
