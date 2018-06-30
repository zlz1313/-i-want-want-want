import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from pandas import DataFrame as DF
import xgboost as xgb
import lightgbm as lgb
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier as GBC


import warnings
warnings.filterwarnings("ignore")
from sklearn.cross_validation import cross_val_score as cv
train = pd.read_csv('f_train_20180204.csv',encoding='gbk')
test = pd.read_csv('f_test_a_20180204.csv',encoding='gbk')

'''-------------------------------------------------------------------'''
del train['id']
del test['id']
feature_name = [i for i in train.columns if i!='label']

def get_pic(model,feature_name):
    ans = DF()
    ans['name'] = feature_name
    ans['score'] = model.feature_importances_
#     print(ans[ans['score']>0].shape)
    return ans.sort_values(by=['score'],ascending=False).reset_index(drop=True)
	
def get_model(nums,cv_fold):
    feature_name1 = train_data[feature_name].columns
    get_ans_face = list(set(get_pic(gbc_model,feature_name1).head(nums)['name'])&set(get_pic(xgb_model,feature_name1).head(nums)['name'])&set(get_pic(lgb_model,feature_name1).head(nums)['name']))
    print('New Feature: ',len(get_ans_face))
    if 'SNP32*SNP34' not in get_ans_face:
        get_ans_face.append('SNP32*SNP34')
    print('New Feature: ',len(get_ans_face))
    new_lgb_model = lgb.LGBMClassifier(objective='binary',n_estimators=300,max_depth=3,min_child_samples=6,learning_rate=0.102,random_state=1)
    cv_model = cv(new_lgb_model, train_data[get_ans_face], train_label,  cv=cv_fold, scoring='f1')
    new_lgb_model.fit(train_data[get_ans_face], train_label)
    m1 = cv_model.mean()

    new_xgb_model1 = xgb.XGBClassifier(objective='binary:logistic',n_estimators=300,max_depth=4,learning_rate=0.101,random_state=1)
    cv_model = cv(new_xgb_model1, train_data[get_ans_face].values, train_label,  cv=cv_fold, scoring='f1')
    new_xgb_model1.fit(train_data[get_ans_face].values, train_label)
    m2 = cv_model.mean()

    new_gbc_model = GBC(n_estimators=310,subsample=1,min_samples_split=2,max_depth=3,learning_rate=0.1900,min_weight_fraction_leaf=0.1)
    kkk = train_data[get_ans_face].fillna(7)
    cv_model = cv(new_gbc_model, kkk[get_ans_face], train_label,  cv=cv_fold, scoring='f1')
    new_gbc_model.fit(kkk.fillna(7),train_label)

    m3 = cv_model.mean()
    print((m1+m2+m3)/3)
    pro1 = new_lgb_model.predict_proba(test_data[get_ans_face])
    pro2 = new_xgb_model1.predict_proba(test_data[get_ans_face].values)
    pro3 = new_gbc_model.predict_proba(test_data[get_ans_face].fillna(7).values)
    ans = (pro1+pro2+pro3)/3
    return ans

def find_best_feature(feature_name,cv_fold):
    get_ans_face = feature_name
    new_lgb_model = lgb.LGBMClassifier(objective='binary',n_estimators=300,max_depth=3,min_child_samples=6,learning_rate=0.102,random_state=1)
    cv_model = cv(new_lgb_model, train_data[get_ans_face], train_label,  cv=cv_fold, scoring='f1')
    new_lgb_model.fit(train_data[get_ans_face], train_label)
    m1 = cv_model.mean()

    new_xgb_model1 = xgb.XGBClassifier(objective='binary:logistic',n_estimators=300,max_depth=4,learning_rate=0.101,random_state=1)
    cv_model = cv(new_xgb_model1, train_data[get_ans_face].values, train_label,  cv=cv_fold, scoring='f1')
    new_xgb_model1.fit(train_data[get_ans_face].values, train_label)
    m2 = cv_model.mean()

    new_gbc_model = GBC(n_estimators=310,subsample=1,min_samples_split=2,max_depth=3,learning_rate=0.1900,min_weight_fraction_leaf=0.1)
    kkk = train_data[get_ans_face].fillna(7)
    cv_model = cv(new_gbc_model, kkk[get_ans_face], train_label,  cv=cv_fold, scoring='f1')
    new_gbc_model.fit(kkk.fillna(7),train_label)
    m3 = cv_model.mean()
    return (m1+m2+m3)/3

def train_best_feature(feature_name):
    get_ans_face = feature_name
    new_lgb_model = lgb.LGBMClassifier(objective='binary',n_estimators=300,max_depth=3,min_child_samples=6,learning_rate=0.102,random_state=1)
    new_lgb_model.fit(train_data[get_ans_face], train_label)

    new_xgb_model1 = xgb.XGBClassifier(objective='binary:logistic',n_estimators=300,max_depth=4,learning_rate=0.101,random_state=1)
    new_xgb_model1.fit(train_data[get_ans_face].values, train_label)

    new_gbc_model = GBC(n_estimators=310,subsample=1,min_samples_split=2,max_depth=3,learning_rate=0.1900,min_weight_fraction_leaf=0.1)
    kkk = train_data[get_ans_face].fillna(7)
    new_gbc_model.fit(kkk.fillna(7),train_label)
    
    pro1 = new_lgb_model.predict_proba(test_data[get_ans_face])
    pro2 = new_xgb_model1.predict_proba(test_data[get_ans_face].values)
    pro3 = new_gbc_model.predict_proba(test_data[get_ans_face].fillna(7).values)
    ans = (pro1+pro2+pro3)/3

    return ans

train_data = pd.concat([train],axis=0)
train_label = train_data['label']
del train_data['label']
test_data = test[feature_name]


feature_SNP = [i for i in feature_name if 'SNP' in i]
feature_no_SNP = list(set(feature_name)-set(feature_SNP))
train_no_SNP_mean = train.describe().T[['mean','min','max']].T[feature_no_SNP]
train_no_SNP = train[feature_no_SNP]
train_SNP = train[feature_SNP]
test_no_SNP_mean = test.describe().T[['mean','min','max']].T[feature_no_SNP]
test_SNP = test[feature_SNP]
test_no_SNP = test[feature_no_SNP]

train_no_SNP.to_csv('train_no_SNP.csv',index=False)
test_no_SNP.to_csv('test_no_SNP.csv',index=False)
train_SNP.to_csv('train_SNP.csv',index=False)
test_SNP.to_csv('test_SNP.csv',index=False)


def get_division_feature(data,feature_name):
    new_feature = []
    new_feature_name = []
    for i in range(len(data[feature_name].columns)-1):
        for j in range(i+1,len(data[feature_name].columns)):
            new_feature_name.append(data[feature_name].columns[i] + '/' + data[feature_name].columns[j])
            new_feature_name.append(data[feature_name].columns[i] + '*' + data[feature_name].columns[j])
            new_feature_name.append(data[feature_name].columns[i] + '+' + data[feature_name].columns[j])
            new_feature_name.append(data[feature_name].columns[i] + '-' + data[feature_name].columns[j])
            new_feature.append(data[data[feature_name].columns[i]]/data[data[feature_name].columns[j]])
            new_feature.append(data[data[feature_name].columns[i]]*data[data[feature_name].columns[j]])
            new_feature.append(data[data[feature_name].columns[i]]+data[data[feature_name].columns[j]])
            new_feature.append(data[data[feature_name].columns[i]]-data[data[feature_name].columns[j]])
            
    
    temp_data = DF(pd.concat(new_feature,axis=1))
    temp_data.columns = new_feature_name
    data = pd.concat([data,temp_data],axis=1).reset_index(drop=True)
    
    print(data.shape)
    
    return data.reset_index(drop=True)

def get_square_feature(data,feature_name):
    new_feature = []
    new_feature_name = []
    for i in range(len(data[feature_name].columns)):
        new_feature_name.append(data[feature_name].columns[i] + '**2')
        new_feature_name.append(data[feature_name].columns[i] + '**1/2')
        new_feature.append(data[data[feature_name].columns[i]]**2)
        new_feature.append(data[data[feature_name].columns[i]]**(1/2))
        
    temp_data = DF(pd.concat(new_feature,axis=1))
    temp_data.columns = new_feature_name
    data = pd.concat([data,temp_data],axis=1).reset_index(drop=True)
    
    print(data.shape)
    
    return data.reset_index(drop=True)

train_data = get_square_feature(train_no_SNP,feature_no_SNP)
test_data = get_square_feature(test_no_SNP,feature_no_SNP)

train_data_SNP = get_division_feature(train_SNP,train_SNP.columns)
train_data_no_SNP = get_division_feature(train_no_SNP,train_no_SNP.columns)
train_data = pd.concat([train_data_SNP,train_data_no_SNP,train_data],axis=1)
test_data_SNP = get_division_feature(test_SNP,test_SNP.columns)
test_data_no_SNP = get_division_feature(test_no_SNP,test_no_SNP.columns)
test_data = pd.concat([test_data_SNP,test_data_no_SNP,test_data],axis=1)

feature_name = [i for i in train_data.columns if i!='label']
print(len(train_data.columns))
print(train_data.shape)
print(test_data.shape)

lgb_model = lgb.LGBMClassifier(objective='binary',n_estimators=120,subsample=0.9,nthread=4)
# cv_model = cv(lgb_model, train_data[feature_name], train_label,  cv=10, scoring='f1')
lgb_model.fit(train_data[feature_name], train_label)




xgb_model = xgb.XGBClassifier(objective='binary:logistic',n_estimators=120,subsample=0.9,nthread=4)
# cv_model = cv(xgb_model, train_data[feature_name].values, train_label,  cv=10, scoring='f1')
xgb_model.fit(train_data[feature_name].values, train_label)

gbc_model = GBC(n_estimators=200,subsample=0.9,min_samples_split=2)
kkk = train_data[feature_name].fillna(7)
kkk.replace(np.inf,999,inplace=True)
# cv_model = cv(gbc_model, kkk[feature_name], train_label,  1cv=10, scoring='f1')
gbc_model.fit(kkk.fillna(7),train_label)

nums = 45
feature_name1 = train_data[feature_name].columns
get_ans_face = list(set(get_pic(lgb_model,feature_name1).head(nums)['name'])|set(get_pic(xgb_model,feature_name1).head(nums)['name'])|set(get_pic(gbc_model,feature_name1).head(nums)['name']))
print('New Feature: ',len(get_ans_face))


now_feature = []
check = 0
for i in range(len(get_ans_face)):
    now_feature.append(get_ans_face[i])
    jj = find_best_feature(now_feature,6)
    if jj>check:
        print('目前特征长度为',len(now_feature),' 目前帅气的cv值是',jj,' 成功加入第',i+1,'个','增值为',jj-check)
        check = jj
    else:
        now_feature.pop()	
		
now_feature2 = []
check = 0
for i in range(len(get_ans_face)):
    now_feature2.append(get_ans_face[len(get_ans_face)-i-1])
    jj = find_best_feature(now_feature2,6)
    if jj>check:
        print('目前特征长度为',len(now_feature2),' 目前帅气的cv值是',jj,' 成功加入第',i+1,'个','增值为',jj-check)
        check = jj
    else:
        now_feature2.pop()
