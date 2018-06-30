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


# 距离观测点(end_day)1天内、3天内和7天内留存率
def get_register_retention_feature1(start_day, end_day):
    register = user_register_log_df[user_register_log_df.register_day <= end_day][['user_id', 'register_day']]
    retention = register.groupby(['register_day']).agg({'user_id': 'count'}).reset_index()
    for day_cell in [3, 7]:
        app_temp_df = \
            app_launch_log_df[(app_launch_log_df.day <= end_day) & (app_launch_log_df.day > end_day - day_cell)][
                ['user_id']]
        video_temp_df = \
            video_create_log_df[(video_create_log_df.day <= end_day) & (video_create_log_df.day > end_day - day_cell)][
                ['user_id']]
        action_temp_df = \
            user_activity_log_df[
                (user_activity_log_df.day <= end_day) & (user_activity_log_df.day > end_day - day_cell)][
                ['user_id']]
        active_temp = pd.concat([app_temp_df, video_temp_df, action_temp_df], axis=0).drop_duplicates()
        retention_temp = pd.merge(active_temp, register, on=['user_id'], how='left')
        retention_temp = retention_temp.groupby(['register_day']).agg('count').reset_index()
        retention_temp.rename(columns={'user_id': 'r_retention_in_' + str(day_cell)}, inplace=True)
        retention = pd.merge(retention, retention_temp, on=['register_day'], how='left')
        retention['r_retention_in_' + str(day_cell)] = retention['r_retention_in_' + str(day_cell)] / retention.user_id
    retention.rename(columns={'user_id': 'r_cnt_daily'}, inplace=True)
    return retention.fillna(0)


# 距离观测点(end_day)1天、3天和7天留存率
def get_register_retention_feature2(start_day, end_day):
    register = user_register_log_df[user_register_log_df.register_day <= end_day][['user_id', 'register_day']]
    retention = register.groupby(['register_day']).agg({'user_id': 'count'}).reset_index()
    for day_cell in [1, 3, 7]:
        app_temp_df = app_launch_log_df[app_launch_log_df.day == end_day - day_cell + 1][['user_id']]
        video_temp_df = video_create_log_df[video_create_log_df.day == end_day - day_cell + 1][['user_id']]
        action_temp_df = user_activity_log_df[user_activity_log_df.day == end_day - day_cell + 1][['user_id']]
        active_temp = pd.concat([app_temp_df, video_temp_df, action_temp_df], axis=0).drop_duplicates()
        retention_temp = pd.merge(active_temp, register, on=['user_id'], how='left')
        retention_temp = retention_temp.groupby(['register_day']).agg('count').reset_index()
        retention_temp.rename(columns={'user_id': 'r_retention_at_' + str(day_cell)}, inplace=True)
        retention = pd.merge(retention, retention_temp, on=['register_day'], how='left')
        retention['r_retention_at_' + str(day_cell)] = retention['r_retention_at_' + str(day_cell)] / retention.user_id
    retention = retention.drop(['user_id'], axis=1)
    return retention.fillna(0)


# 注册日次日、3天、7天、观测点(end_day)留存率
def get_register_retention_feature3(start_day, end_day):
    register = user_register_log_df[user_register_log_df.register_day <= end_day][['user_id', 'register_day']]
    app_temp_df = app_launch_log_df[app_launch_log_df.day <= end_day][['user_id', 'day']]
    video_temp_df = video_create_log_df[video_create_log_df.day <= end_day][['user_id', 'day']]
    action_temp_df = user_activity_log_df[user_activity_log_df.day <= end_day][['user_id', 'day']]
    active_temp = pd.concat([app_temp_df, video_temp_df, action_temp_df], axis=0).drop_duplicates()
    retention_temp = pd.merge(active_temp, register, on=['user_id'], how='left')
    retention_temp = retention_temp.groupby(['register_day', 'day']).agg('count').reset_index()
    retention_temp.rename(columns={'user_id': 'cnt'}, inplace=True)
    retention = register.groupby(['register_day']).agg({'user_id': 'count'}).reset_index()
    for day in [1, 3, 7, end_day]:
        name = str(day)
        if day == end_day:
            name = 'all'
        retention['r_' + name + '_retention'] = retention.register_day.apply(
            lambda x: x + day if (x + day) < end_day else end_day)
        retention = pd.merge(retention, retention_temp, left_on=['register_day', 'r_' + name + '_retention'],
                             right_on=['register_day', 'day'], how='left')
        retention['r_' + name + '_retention'] = retention.cnt / retention.user_id
        retention = retention.drop(['cnt', 'day'], axis=1)
    return retention.drop(['user_id'], axis=1).fillna(0)


def get_data(start_day, end_day):
    retention1 = get_register_retention_feature1(start_day, end_day)
    retention2 = get_register_retention_feature2(start_day, end_day)
    retention3 = get_register_retention_feature3(start_day, end_day)

    data = pd.merge(retention1, retention2, on=['register_day'], how='left')
    data = pd.merge(data, retention3, on=['register_day'], how='left')

    data.register_day = end_day - data.register_day
    return data.fillna(0)


if __name__ == '__main__':
    INPUT_BASE_PATH = r"C:\\Users\\Administrator\\Desktop\kesci\\Data\\raw_data"
    OUTPUT_BASE_PATH = r"C:\Users\Administrator\Desktop\kesci\Data\retention_data"

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
