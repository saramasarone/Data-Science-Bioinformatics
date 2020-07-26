#gridsearch for xgboost crit vs all the others
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import GridSearchCV

#read data
prot = pd.read_csv('/Users/smasarone/Desktop/Trauma_data_scripts/data_final/data_last_modifications/raw_data_proteins_filtered.csv',header = 0, index_col = 0)
clin = pd.read_csv('/Users/smasarone/Desktop/Trauma_data_scripts/data_final/data_last_modifications/clin_ready.csv', header = 0, index_col=0)

#define groups
list_groups = []
for i in clin['iss']:
    if i<=3:
        list_groups.append("Control")
    elif i>3 and i<= 8:
        list_groups.append("Low")
    elif i>=9 and i<=15:
        list_groups.append("Moderate")
    elif i>15 and i<25:
        list_groups.append("Severe")
    else:
        list_groups.append("Critical")

groups = pd.DataFrame(list_groups, columns  = (['Severity']))
groups = groups.set_index(clin.index)
clin =  clin.join(groups)

#scaling data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(prot)
X= scaler.transform(prot)
X= pd.DataFrame(X)
X.columns= prot.columns
X = X.set_index(prot.index)

groups['Severity_2'] = groups['Severity'].replace({"Control":0,  "Low":0, "Moderate":0, "Severe": 0, "Critical":1})
y = groups['Severity_2']


#setting xgboost
gbm_param_grid = {'learning_rate': [0.15, 0.20, 0.25, 0.30],
                  'num_boosting_rounds' :[10, 15,20, 25, 30],
                  'subsample':[0.2, 0.3, 0.5, 0.8, 0.9],
                  'colsample_bytree':[0.2, 0.25, 0.30, 0.35],
                  'max_depth':[2, 3, 5]}

gbm = xgb.XGBRFClassifier()
grid_roc = GridSearchCV(estimator=gbm, param_grid=gbm_param_grid, scoring= "accuracy", cv = 3)
grid_roc.fit(X, y)
print("Best parameters found are", grid_roc.best_params_)
print("best roc score found", grid_roc.best_score_)
