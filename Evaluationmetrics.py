

# create a differenced series
def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return np.array(diff)
 
# invert differenced value
def inverse_difference(history, yhat, interval=1):
    return yhat + history[-interval]


def EvaluatePerformance_ARIMA(model_fit_object,
                              differenced,
                              y_train,
                              y_test):
  

    """This function is used to evaluate performance of an ARIMA model
    
    Args:
        model_fit_object (ARIMA .fit object): The return value of the .fit call of ARIMA
        differenced (numpy array): The array with y_train differenced using d value
        y_train (pandas dataframe): pandas dataframe containing y_train 
        y_test (pandas dataframe): pandas dataframe containing y_test 
    
    
    Returns:
        return_dict: Dictionary containing the metrics and the predicted dataframe
    
    """    
  

    
    #Make sure you use the command below to install latest version of scikit learn
    # conda install -c conda-forge scikit-learn  
    
    from sklearn.metrics import mean_poisson_deviance,mean_squared_error
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
    
    Mean_poission_dev = mean_poisson_deviance(y_true, y_pred)
    print("The Mean_poission_dev of the model with the test data is",Mean_poission_dev)
    
    return_dict = { "Root mean squared error" : RMSE,
                     "prediction_dataframe" : predicted_df,
                     "mean_poisson_deviance":Mean_poission_dev}
    
    
    return return_dict
    
    


def EvaluatePerformance_fbprophet(model,test,y_true):
    """ Evaluating model performance of fb prophet
    
    
    Args:
        model (fbprophetmodel): fb prophet model fit on the training data
        test (pandas dataframe): X_test predicted dataframes
        y_true (pandas dataframe): True values dataframe
    
    
    Returns:
        return_dict: Dictionary containing the metrics and the predicted dataframe
    
    """    

    
    
    #Make sure you use the command below to install latest version of scikit learn
    # conda install -c conda-forge scikit-learn  
    
    from sklearn.metrics import mean_poisson_deviance,mean_squared_error
    test_dataset = pd.DataFrame()
    test_dataset['ds'] = pd.to_datetime(test["Date"])
    predicted_df = model.predict(test_dataset) #Get the predicted data frame on test
    y_pred = predicted_df['yhat'] #yhat is the output column name in fbprophet
    print("y_pred is \n",y_pred)
    
    
    RMSE = mean_squared_error(y_true, y_pred,squared= False)
    print("The RMSE of the model with the test data is",RMSE)
    
    Mean_poission_dev = mean_poisson_deviance(y_true, y_pred)
    print("The Mean_poission_dev of the model with the test data is",Mean_poission_dev)
    
    return_dict = { "Root mean squared error" : RMSE,
                    "prediction_dataframe" : y_pred,
                    "mean_poisson_deviance":Mean_poission_dev}
    
    
    return return_dict

    
def split_train_test(X,y,train_size=0.75):
    """This function is used to split X,y into train test dataframes
    similar to scikit learn's train test split but only for time series to maintain
    the follow up of test after train.
    
    Args:
        X (pandas dataframe): X data to be split
        y (pandas dataframe): y data to be split
        train_size (float, optional): Train fraction between 0 and 1. Defaults to 0.75.
    
    
    Returns:
        X_train, X_test, y_train, y_test: The 4 pandas dataframes 
    
    """    
    
    assert ((0 <train_size<=1.0) ,"Please give train size between 0 and 1")
    train_length =  int(train_size*len(y))
    print("Length of the train dataset is",train_length)
    X_train = X.iloc[:train_length]
    y_train = y.iloc[:train_length]
    
    X_test = X.iloc[train_length:]
    y_test = y.iloc[train_length:]
    
    print("Length of y_test is",len(y_test))
    
    return X_train, X_test, y_train, y_test