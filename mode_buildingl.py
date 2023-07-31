import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression , Lasso
from sklearn.ensemble import RandomForestRegressor
import statsmodels.api as sm
from sklearn.metrics import mean_absolute_error
import pickle

df = pd.read_csv('data\Data Scientist_cleaned.csv')

df.columns

df_model = df[['avg_salary','Rating','hourly','Location','python','job_simp','seniority','desc_len']]

df_dum = pd.get_dummies(df_model)

# Fill NaN values before the split
df_dum = df_dum.fillna(0)

# Split dataset into training and test
X = df_dum.drop('avg_salary', axis =1)
y = df_dum.avg_salary.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 42)


#Multiple linear regression

X_sm = X = sm.add_constant(X)
# X_sm = X_sm.fillna(0)
X_sm = X_sm.astype(int)
model = sm.OLS(y,X_sm)
model.fit().summary()

#Sklearn Linear Regression
lm = LinearRegression()
lm.fit(X_train, y_train)

np.mean(cross_val_score(lm,X_train,y_train,scoring = 'neg_mean_absolute_error',cv=3))

#   Lasso Regression
lm_l = Lasso()
np.mean(cross_val_score(lm_l,X_train,y_train,scoring = 'neg_mean_absolute_error',cv=3))

alpha =[]
error = []

for i in range(1500,1800,10):
    alpha.append(i)
    lm_l = Lasso(alpha=(i))
    error.append(np.mean(cross_val_score(lm_l,X_train,y_train,scoring = 'neg_mean_absolute_error',cv=3)))

plt.plot(alpha, error)

err = tuple(zip(alpha,error))

df_err = pd.DataFrame(err, columns = ['alpha','error'])
df_err[df_err.error == max(df_err.error)]
#Best Alpha at 1620
lm_l = Lasso(alpha=1620)  # Use the optimal alpha value you've determined
lm_l.fit(X_train, y_train)
#Random Forest
rf = RandomForestRegressor()
np.mean(cross_val_score(rf, X_train,y_train,scoring = 'neg_mean_absolute_error',cv=3))

#Use grid search to tune model
parameters = {'n_estimators':range(10,300,10), 'criterion':('mse','absolute_error'), 'max_features':('auto','sqrt','log2')}

gs = GridSearchCV(rf,parameters,scoring='neg_mean_absolute_error',cv=3)
gs.fit(X_train,y_train)

gs.best_score_
gs.best_estimator_


# test ensembles 
tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

#Measure mean absolute errors
mean_absolute_error(y_test,tpred_lm)
mean_absolute_error(y_test,tpred_lml)
mean_absolute_error(y_test,tpred_rf)

mean_absolute_error(y_test,(tpred_lm+tpred_rf)/2)


pickl = {'model': gs.best_estimator_}
pickle.dump( pickl, open( 'model_file' + ".p", "wb" ) )

file_name = "model_file.p"
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']

model.predict(np.array(list(X_test.iloc[1,:])).reshape(1,-1))[0]

list(X_test.iloc[1,:])