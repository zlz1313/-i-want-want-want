import datetime
import pandas as pd


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
    register = user_register_log_df[(user_register_log_df.register_day >= start_day) & (user_register_log_df.register_day <= end_day)].copy()
    return register[['user_id']]


# 行为 视频和作者 特征
def get_action_video_author_feature(start_day, end_day):
    action = user_activity_log_df[['user_id']].drop_duplicates()
    df = user_activity_log_df[(user_activity_log_df.day >= start_day) & (user_activity_log_df.day <= end_day)][
        ['user_id', 'day', 'video_id', 'author_id']]
    df.day = end_day - df.day
    for day in [1, 3, 7, end_day - start_day + 1]:
        # 看过的不同视频数量
        action_temp_df = df[df.day < day][['user_id', 'video_id']]
        action_temp_df = action_temp_df.groupby(['user_id']).aggregate(lambda x: list(set(x))).reset_index()
        action_temp_df['a_video_set_cnt_in_' + str(day)] = action_temp_df.video_id.apply(lambda x: len(x))
        action_temp_df = action_temp_df.drop(['video_id'], axis=1)
        action = pd.merge(action, action_temp_df, on=['user_id'], how='left')
        # 看过的不同作者数量
        action_temp_df = df[df.day < day][['user_id', 'author_id']]
        action_temp_df = action_temp_df.groupby(['user_id']).aggregate(lambda x: list(set(x))).reset_index()
        action_temp_df['a_author_set_cnt_in_' + str(day)] = action_temp_df.author_id.apply(lambda x: len(x))
        action_temp_df = action_temp_df.drop(['author_id'], axis=1)
        action = pd.merge(action, action_temp_df, on=['user_id'], how='left')
    return action.fillna(0)


def get_data(start_day, end_day):
    register = get_register_feature(start_day, end_day)
    action = get_action_video_author_feature(start_day, end_day)
    data = pd.merge(register, action, on=['user_id'], how='left')
    return data.fillna(0)


if __name__ == '__main__':
    INPUT_BASE_PATH = r"C:\\Users\\Administrator\\Desktop\kesci\\Data\\raw_data_b"
    OUTPUT_BASE_PATH = r"C:\Users\Administrator\Desktop\kesci\Data\a_va_set_cnt_data"

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
    test = get_data(1, 30)
    test.to_csv(OUTPUT_BASE_PATH + '/data3.csv', index=False)
    print('========' + str((datetime.datetime.now() - starttime).seconds) + 's,data3 done,shape:' + str(
        test.shape) + '==========')

