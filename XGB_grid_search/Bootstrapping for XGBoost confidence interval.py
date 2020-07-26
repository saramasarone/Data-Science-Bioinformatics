import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

prot = pd.read_csv('/Users/smasarone/Desktop/Trauma_data_scripts/data_final/data_last_modifications/raw_data_proteins_filtered.csv',header = 0, index_col = 0)
clin = pd.read_csv('/Users/smasarone/Desktop/Trauma_data_scripts/data_final/data_last_modifications/clin_ready.csv', header = 0, index_col=0)

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
print(len(list_groups))
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
X.head(3)

#Bootstrapping critical vs all the others
groups['Severity_2'] = groups['Severity'].replace({"Control":0,  "Low":0, "Moderate":0, "Severe": 0, "Critical":1})
X['y']= (groups['Severity_2'])

import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.utils import resample

# configure bootstrap using the parameters obtained by apocrita GridSearchCV
n_iterations = 60
n_size = int(len(X) * 0.70) #training 70%
values = X.values

stats = list()
for i in range(n_iterations):

    train = resample(values, n_samples=n_size)
    test = np.array([x for x in values if x.tolist() not in train.tolist()])

    dtrain = xgb.DMatrix(train[:,:-1], label= train[:,-1])
    dtest = xgb.DMatrix(test[:,:-1], label= test[:,-1])
    param = {'colsample_bytree': 0.2, 'learning_rate': 0.15, 'max_depth': 3, 'num_boosting_rounds': 60, 'subsample': 0.8}
    param['eval_metric'] = 'auc'
    evallist = [(dtest, 'eval'), (dtrain, 'train')]
    num_round = 45 #fix this
    bst = xgb.train(param, dtrain, num_round, evallist, verbose_eval=False)
    ypred = bst.predict(dtest)
    stats.append(bst.eval(dtest, iteration=35))
print(stats)


new_list =[]
for i in stats:
    new_list.append(float(i.split(':')[1]))
print(new_list)

plt.hist(new_list)
plt.title("XGBoost performance")
plt.xlabel("performance accuracy")
plt.ylabel("number of iterations")

#plot distplot
sns.distplot(new_list)

# confidence intervals - 95CI -
alpha = 0.95
p = ((1.0-alpha)/2.0) * 100
lower = max(0.0, np.percentile(new_list, p))
p = (alpha+((1.0-alpha)/2.0)) * 100
upper = min(1.0, np.percentile(new_list, p))
print('%.1f confidence interval %.1f%% and %.1f%%' % (alpha*100, lower*100, upper*100))

############### Second Part #####################

#Bootstrapping critical/control together
groups['Severity_3'] = groups['Severity'].replace({"Control":0,  "Low":0, "Moderate":0, "Severe": 1, "Critical":1})
X['y']= (groups['Severity_3'])

#Parameters were modified after running a GridSearch on Apocrita. The results were used here.
# configure bootstrap
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.utils import resample

n_iterations = 60
n_size = int(len(X) * 0.70)
values = X.values

stats = list()
for i in range(n_iterations):

    train = resample(values, n_samples=n_size)
    test = np.array([x for x in values if x.tolist() not in train.tolist()])

    dtrain = xgb.DMatrix(train[:,:-1], label= train[:,-1])
    dtest = xgb.DMatrix(test[:,:-1], label= test[:,-1])
    param = {'max_depth': 5, "colsample_bytree": 0.3, "learning_rate": 0.15, "subsample": 0.8, 'objective': 'binary:logistic'}
    param['nthread'] = 4
    param['eval_metric'] = 'auc'
    evallist = [(dtest, 'eval'), (dtrain, 'train')]
    num_round = 50
    bst = xgb.train(param, dtrain, num_round, evallist, verbose_eval=False)
    ypred = bst.predict(dtest)
    stats.append(bst.eval(dtest, iteration=35))
print(stats)


new_list =[]
for i in stats:
    new_list.append(float(i.split(':')[1]))
print(new_list)


plt.hist(new_list)
plt.title("XGBoost performance")
plt.xlabel("performance accuracy")
plt.ylabel("number of iterations")

# confidence intervals
alpha = 0.95
p = ((1.0-alpha)/2.0) * 100
lower = max(0.0, np.percentile(new_list, p))
p = (alpha+((1.0-alpha)/2.0)) * 100
upper = min(1.0, np.percentile(new_list, p))
print('%.1f confidence interval %.1f%% and %.1f%%' % (alpha*100, lower*100, upper*100))
