def EvaluatePerformance_fbprophet(model,test,y_true):

    
    
    
    #Make sure you use the command below to install latest version of scikit learn
    # conda install -c conda-forge scikit-learn  
    
    from sklearn.metrics import mean_absolute_percentage_error,mean_squared_error
    test_dataset = pd.DataFrame()
    test_dataset['ds'] = pd.to_datetime(test["Date"])
    predicted_df = model.predict(test_dataset) #Get he predicted data frame on test
    y_pred = predicted_df['yhat']
    print("y_pred is \n",y_pred)
    
    
    RMSE = mean_squared_error(y_true, y_pred,squared= False)
    print("The RMSE of the model with the test data is",RMSE)
    
    MAPE =  mean_absolute_percentage_error(y_true, y_pred)
    print("The MAPE of the model with the test data is",MAPE)
    
    return_dict = { "Root mean squared error" : RMSE,
                     "mean_absolute_percentage_error" : MAPE}
    
    
    return return_dict
    