"""
This is an example script to generate the outcome variable given the input dataset.

This script should be modified to prepare your own submission that predicts 
the outcome for the benchmark challenge by changing the clean_df and predict_outcomes function.

The predict_outcomes function takes a Pandas data frame. The return value must
be a data frame with two columns: nomem_encr and outcome. The nomem_encr column
should contain the nomem_encr column from the input data frame. The outcome
column should contain the predicted outcome for each nomem_encr. The outcome
should be 0 (no child) or 1 (having a child).

clean_df should be used to clean (preprocess) the data.

run.py can be used to test your submission.
"""

# List your libraries and modules here. Don't forget to update environment.yml!
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
import training

# loading data (predictors)
# train = pd.read_csv("../training_data/PreFer_train_data.csv", low_memory = False) 
# loading the outcome
# outcome = pd.read_csv("../training_data/PreFer_train_outcome.csv")


def clean_df(df, background_df=None):
    """
    Preprocess the input dataframe to feed the model.
    # If no cleaning is done (e.g. if all the cleaning is done in a pipeline) leave only the "return df" command

    Parameters:
    df (pd.DataFrame): The input dataframe containing the raw data (e.g., from PreFer_train_data.csv or PreFer_fake_data.csv).
    background (pd.DataFrame): Optional input dataframe containing background data (e.g., from PreFer_train_background_data.csv or PreFer_fake_background_data.csv).

    Returns:
    pd.DataFrame: The cleaned dataframe with only the necessary columns and processed variables.
    """

    ## This script contains a bare minimum working example
    # Create new variable with age
    # df["age"] = 2024 - df["birthyear_bg"]

    # Imputing missing values in age with the mean
    # df["age"] = df["age"].fillna(df["age"].mean())
    df["woning_2020"] = df["woning_2020"].fillna(df["woning_2020"].mean())
    df["belbezig_2020"] = df["belbezig_2020"].fillna(df["belbezig_2020"].mean())
    df["oplzon_2020"] = df["oplzon_2020"].fillna(df["oplzon_2020"].mean())
    df["nettoink_f_2020"] = df["nettoink_f_2020"].fillna(df["nettoink_f_2020"].mean())


    # Selecting variables for modelling
    keepcols = [
        "nomem_encr",  # ID variable required for predictions,
        # "age",         # newly created variable
        "woning_2020",       # 
        "belbezig_2020",      # Primary occupation
        # "brutoink",      # Personal gross monthly income in Euros
        # "nettoink",      # Personal net monthly income in Euros (incl. nettocat)
        # "brutocat",      # Personal gross monthly income in categories
        # "nettocat",      # Personal net monthly income in categories
        "oplzon_2020",        # Highest level of education irrespective of diploma
        # "oplmet",        # Highest level of education with diploma
        # "oplcat",        # Level of education in CBS (Statistics Netherlands) categories
        # "simpc",         # does the household have a simpc
        # "brutoink_f",    # Personal gross monthly income in Euros, imputed
        # "netinc",        # Personal net monthly income in Euros
        "nettoink_f_2020",    # Personal net monthly income in Euros, imputed
        # "brutohh_f",     # Gross household income in Euros
        # "nettohh_f",     # Net household income in Euros
        # "gender_bg"
    ] 

    # Keeping data with variables selected
    df = df[keepcols]

    return df

# train_cleaned = clean_df(train)
# training and saving the model
# training.train_save_model(train_cleaned, outcome)

# fake = pd.read_csv("PreFer_fake_data.csv") 

def predict_outcomes(df, background_df=None, model_path="model.joblib"):
    """Generate predictions using the saved model and the input dataframe.

    The predict_outcomes function accepts a Pandas DataFrame as an argument
    and returns a new DataFrame with two columns: nomem_encr and
    prediction. The nomem_encr column in the new DataFrame replicates the
    corresponding column from the input DataFrame. The prediction
    column contains predictions for each corresponding nomem_encr. Each
    prediction is represented as a binary value: '0' indicates that the
    individual did not have a child during 2021-2023, while '1' implies that
    they did.

    Parameters:
    df (pd.DataFrame): The input dataframe for which predictions are to be made.
    background_df (pd.DataFrame): The background dataframe for which predictions are to be made.
    model_path (str): The path to the saved model file (which is the output of training.py).

    Returns:
    pd.DataFrame: A dataframe containing the identifiers and their corresponding predictions.
    """

    ## This script contains a bare minimum working example
    if "nomem_encr" not in df.columns:
        print("The identifier variable 'nomem_encr' should be in the dataset")

    # Load the model
    model = joblib.load(model_path)

    # Preprocess the fake / holdout data
    df = clean_df(df, background_df)

    # Exclude the variable nomem_encr if this variable is NOT in your model
    vars_without_id = df.columns[df.columns != 'nomem_encr']

    # Generate predictions from model, should be 0 (no child) or 1 (had child)
    predictions = model.predict(df[vars_without_id])

    # Output file should be DataFrame with two columns, nomem_encr and predictions
    df_predict = pd.DataFrame(
        {"nomem_encr": df["nomem_encr"], "prediction": predictions}
    )

    # Return only dataset with predictions and identifier
    return df_predict

# print(predict_outcomes(fake))