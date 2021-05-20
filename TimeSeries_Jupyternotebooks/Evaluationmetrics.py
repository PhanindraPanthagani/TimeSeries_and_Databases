
def EvaluatePerformance_ARIMA(model_fit_object,
                              differenced,
                              y_train,
                              y_test):
    """
    This function is used to evaluate performance of an ARIMA model
    
    
    """    
    


    
    #Make sure you use the command below to install latest version of scikit learn
    # conda install -c conda-forge scikit-learn  
    
    from sklearn.metrics import mean_absolute_percentage_error,mean_squared_error
    days_for_prediction  = len(y_test) 
    y_test.fillna(0,inplace=True)
    y_true =np.array(y_test)
    
    
    # multi-step out-of-sample forecast
    start_index = len(differenced)
    end_index = start_index + days_for_prediction -1
    
    forecast = model_fit_object.predict(start=start_index, end=end_index) #Get the predicted data frame on test
    
    # invert the differenced forecast to something usable
    #Since we differenced it,  we need to add it back to previous value to get next value
    history = [x for x in y_train]
    y_pred =[]
    day = 1
    for yhat in forecast:
        inverted = inverse_difference(history, yhat, 1)
        history.append(inverted)
        y_pred.append(inverted)
        day += 1
    print("Length of predictions is",len(y_pred))
    
    #Create a dataframe which can be used to store predictions 
    temp = X_test['Date'].reset_index().drop(columns='index')
 
    predicted_df = pd.DataFrame(index = range(0,days_for_prediction))
    predicted_df['Date'] = temp
    #Making sure that index is matched so that it starts at 0 
    predicted_df['Predicted_value'] = inverted_list

    predicted_df
    
    
    #Calculate the metrics
    
    RMSE = mean_squared_error(y_true, y_pred,squared= False)
    print("The RMSE of the model with the test data is",RMSE)
    
    
    return_dict = { "Root mean squared error" : RMSE,
                     "prediction_dataframe" : predicted_df}
    
    
    return return_dict
    