import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load the data from a csv file into a Pandas DataFrame
df = pd.read_csv("user_preferences.csv")

# Preprocess the data by converting categorical variables into dummy variables
df = pd.get_dummies(df, columns=["Website", "Product", "Category"], prefix=["website", "product", "category"])

# Calculate the cosine similarity matrix
cosine_similarity_matrix = cosine_similarity(df.drop("User", axis=1))


# Function to recommend websites or products based on user preferences
def recommend_items(user_id, cosine_similarity_matrix, df):
    # Get the indices of the websites or products liked by the user
    liked_items = df[df["User"] == user_id].drop("User", axis=1).nonzero()[1]

    # Calculate the similarity scores for the websites or products liked by the user
    similarity_scores = cosine_similarity_matrix[liked_items].mean(axis=0)

    # Sort the websites or products by similarity score and return the top 5
    return df.columns[1:][pd.Series(similarity_scores).sort_values(ascending=False).head(5).index]


# Example usage
user_id = 1
recommended_items = recommend_items(user_id, cosine_similarity_matrix, df)
print("Recommended items for user {}: {}".format(user_id, recommended_items))