import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint

# Tree Visualisation
from sklearn.tree import export_graphviz
from IPython.display import Image
import graphviz
import math

def convert_to_classes(probability):
    # if probability <= 0.3:
    #     return 1  # Low risk
    # elif 0.3 < probability <= 0.6:
    #     return 2  # Medium risk
    # else:
    #     return 3  # High risk
    return math.ceil(7*probability)
    
# Load the data
data = pd.read_csv("flood.csv")

# Define the features (all columns except 'Flood_Risk')
# X = data.drop(columns=['FloodProbability'])

# # Define the target (flood risk scale)
# y = data['FloodProbability']

# Apply the function to the FloodProbability column to create a new 'FloodRiskClass' column
data['FloodRiskClass'] = data['FloodProbability'].apply(convert_to_classes)

# Now use 'FloodRiskClass' as your target for classification
X = data.drop(columns=['FloodProbability', 'FloodRiskClass'])
y = data['FloodRiskClass']

# Split the dataset into training and testing sets (80% train, 20% test)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


# Initialize the model
# model = RandomForestClassifier(n_estimators=100, random_state=42)

model =  ()


# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# for i in range(3):
#     tree = model.estimators_[i]
#     dot_data = export_graphviz(tree,
#                                feature_names=X_train.columns,  
#                                filled=True,  
#                                max_depth=2, 
#                                impurity=False, 
#                                proportion=True)
#     graph = graphviz.Source(dot_data)
#     display(graph)


print(classification_report(y_test, y_pred))



# New property data (encoded and scaled as necessary)
# new_property = [[27.7616, -82.6265, 10, 500, 0, 30, 2, 0, 1, 2, 0, 0.05, 100, 2, 10000, 2, 1200, 50, 10, 0.2, 30, 100, 1, 0, 5000, 250000, 1, 0.3, 2]]

new_property = [[3,8,6,6,4,4,6,2,3,2,5,10,7,4,2,3,4,3,2,6]]



# # Predict the flood risk
predicted_risk = model.predict(new_property)
print("Predicted Flood Risk (1 to 7 scale):", predicted_risk[0])