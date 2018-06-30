import datetime
import pandas as pd
import numpy as np


# 加载数据
def load_data(base_path):
    user_register_log_df = pd.read_csv(base_path + '/user_register_log.txt', sep='\t', header=None,
                                       names=['user_id', 'register_day', 'register_type', 'device_type'])
    app_launch_log_df = pd.read_csv(base_path + '/app_launch_log.txt', sep='\t', header=None, names=['user_id', 'day'])
    video_create_log_df = pd.read_csv(base_path + '/video_create_log.txt', sep='\t', header=None,
                                      names=['user_id', 'day'])
    user_activity_log_df = pd.read_csv(base_path + '/user_activity_log.txt', sep='\t', header=None,
                                       names=['user_id', 'day', 'page', 'video_id', 'author_id', 'action_type'])
    return user_register_log_df, app_launch_log_df, video_create_log_df, user_activity_log_df


# 注册特征
def get_register_feature(start_day, end_day):
    register = user_register_log_df[user_register_log_df.register_day <= end_day].copy()
    return register[['user_id']]


# 拍摄 cnt差分 特征
def get_video_cnt_diff_feature(start_day, end_day):
    video = video_create_log_df[['user_id']].drop_duplicates()
    df = video_create_log_df[(video_create_log_df.day >= start_day) & (video_create_log_df.day <= end_day)][
        ['user_id', 'day']]
    df['cnt'] = 1
    df = df.groupby(['user_id', 'day']).agg('sum').reset_index()
    video_temp = df.groupby(['user_id']).aggregate(lambda x: list(x)).reset_index()
    video_temp.cnt = video_temp.cnt.apply(lambda x: np.diff(x))
    video_temp['v_cnt_diff_max'] = video_temp.cnt.apply(lambda x: max(x) if len(x) != 0 else np.nan)
    video_temp['v_cnt_diff_min'] = video_temp.cnt.apply(lambda x: min(x) if len(x) != 0 else np.nan)
    video_temp['v_cnt_diff_mean'] = video_temp.cnt.apply(lambda x: np.mean(x) if len(x) != 0 else np.nan)
    video_temp['v_cnt_diff_std'] = video_temp.cnt.apply(lambda x: np.std(x) if len(x) != 0 else np.nan)
    video_temp['v_cnt_diff_skew'] = video_temp.cnt.apply(lambda x: pd.Series(x).skew())
    video_temp['v_cnt_diff_kurt'] = video_temp.cnt.apply(lambda x: pd.Series(x).kurt())
    video = pd.merge(video, video_temp.drop(['day', 'cnt'], axis=1), on=['user_id'], how='left')
    return video


# 行为 cnt差分 特征
def get_action_cnt_diff_feature(start_day, end_day):
    action = user_activity_log_df[['user_id']].drop_duplicates()
    df = user_activity_log_df[(user_activity_log_df.day >= start_day) & (user_activity_log_df.day <= end_day)][
        ['user_id', 'day']]
    df['cnt'] = 1
    df = df.groupby(['user_id', 'day']).agg('sum').reset_index()
    action_temp = df.groupby(['user_id']).aggregate(lambda x: list(x)).reset_index()
    action_temp.cnt = action_temp.cnt.apply(lambda x: np.diff(x))
    action_temp['a_cnt_diff_max'] = action_temp.cnt.apply(lambda x: max(x) if len(x) != 0 else np.nan)
    action_temp['a_cnt_diff_min'] = action_temp.cnt.apply(lambda x: min(x) if len(x) != 0 else np.nan)
    action_temp['a_cnt_diff_mean'] = action_temp.cnt.apply(lambda x: np.mean(x) if len(x) != 0 else np.nan)
    action_temp['a_cnt_diff_std'] = action_temp.cnt.apply(lambda x: np.std(x) if len(x) != 0 else np.nan)
    action_temp['a_cnt_diff_skew'] = action_temp.cnt.apply(lambda x: pd.Series(x).skew())
    action_temp['a_cnt_diff_kurt'] = action_temp.cnt.apply(lambda x: pd.Series(x).kurt())
    action = pd.merge(action, action_temp.drop(['day', 'cnt'], axis=1), on=['user_id'], how='left')
    return action


def get_data(start_day, end_day):
    # 注册特征群
    register = get_register_feature(start_day, end_day)

    video4 = get_video_cnt_diff_feature(start_day, end_day)

    # 行为特征群
    action5 = get_action_cnt_diff_feature(start_day, end_day)

    data = pd.merge(register, video4, on=['user_id'], how='left')
    data = pd.merge(data, action5, on=['user_id'], how='left')
    return data


if __name__ == '__main__':
    INPUT_BASE_PATH = r"F:\kuaishou\data\raw_data"
    OUTPUT_BASE_PATH = r"F:\kuaishou\data\Input_data"

    # 加载数据
    user_register_log_df, app_launch_log_df, video_create_log_df, user_activity_log_df = load_data(INPUT_BASE_PATH)

    # 训练集
    starttime = datetime.datetime.now()
    train = get_data(1, 15)
    train.to_csv(OUTPUT_BASE_PATH + '/data1.csv', index=False)
    print('========' + str((datetime.datetime.now() - starttime).seconds) + 's,data1 done,shape:' + str(
        train.shape) + '==========')

    # 验证集
    starttime = datetime.datetime.now()
    valid = get_data(9, 23)
    valid.to_csv(OUTPUT_BASE_PATH + '/data2.csv', index=False)
    print('========' + str((datetime.datetime.now() - starttime).seconds) + 's,data2 done,shape:' + str(
        valid.shape) + '==========')

    # 验证集
    starttime = datetime.datetime.now()
    test = get_data(16, 30)
    test.to_csv(OUTPUT_BASE_PATH + '/data3.csv', index=False)
    print('========' + str((datetime.datetime.now() - starttime).seconds) + 's,data3 done,shape:' + str(
        test.shape) + '==========')
