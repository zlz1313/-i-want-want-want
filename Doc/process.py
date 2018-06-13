0604:
    +- OnlineTest:  feature_num:45 
        --F1 Score: 0.805, yuzhi: 0.35 
        --pre_user_num: 28028 
    +- OffLineTest 
        --F1 Sroce: 0.79697794, yuzhi:0.6
    +-OnLine
        --F1 Score：0.8101 
		
0605-1:
	# drop:'login_arg', 'login_week_arg_cnt','login_cnt','login_max'
    +- OnlineTest:  feature_num:41    
        --F1 Score: 0.803, yuzhi: 0.35
        --pre_user_num: 27000
    +- OffLineTest 
    +-OnLine
        --F1 Score：0.808
		
0605-2:
    +- OnlineTest:  feature_num:45 
        --F1 Score: 0.8052, yuzhi: 0.36
        --pre_user_num: 27000 
    +- OffLineTest 
    +-OnLine
        --F1 Score：0.8125
		
0606-1:
    +- OnlineTest:  feature_num:45 
        --F1 Score: 0.8037, yuzhi: 0.4
        --pre_user_num: 26238    
    +- OffLineTest 
    +-OnLine
        --F1 Score：0.815211

0606-2:
	# add: device_map (0.5)
	# drop: device_type
    +- OnlineTest:  feature_num:45 
        --F1 Score: 0.8067130, yuzhi: 0.38
        --pre_user_num: 26896 
    +- OffLineTest 
    +-OnLine
        --F1 Score：0.8127

0607-1:
	# add: device_map (0.5)
	# drop: device_type
    +- OnlineTest:  feature_num:45 
        --F1 Score: 0.8056409, yuzhi: 0.4
        --pre_user_num: 26146 
    +- OffLineTest 
    +-OnLine
        --F1 Score：0.814669
		
0608-1:
	# 调参
    +- OnlineTest:  feature_num:45 
        --F1 Score: 0.8082, yuzhi: 0.4
        --pre_user_num: 27747 
    +- OffLineTest 
    +-OnLine
        --F1 Score：0.811905
		
0608-2:
	# 数据集划分  data1：1-15，16-22； data2:9-23， 24-30； data3：1-30
	# drop： 'login_sum','login_max','loginvar','loginmean','login_3_cnt','login_week_cnt'
    +- OnlineTest:  feature_num:48 
        --F1 Score: 0.801976005, yuzhi: 0.4
        --pre_user_num: 24368 
    +- OffLineTest 
    +-OnLine
        --F1 Score：0.819586
		
0609-1:
	# 数据集划分  data1：1-15，16-22； data2:9-23， 24-30； data3：1-30
	# drop： 'login_sum','login_max','loginvar','loginmean','login_3_cnt','login_week_cnt'
	# add:	'page_0_sigle', 'page_1_sigle', 'page_2_sigle', 'page_3_sigle',
	#	   'page_4_sigle', 'page_0_all', 'page_1_all', 'page_2_all', 'page_3_all',
	#	   'page_4_all', 'action_type_0_sigle', 'action_type_1_sigle',
	#	   'action_type_2_sigle', 'action_type_3_sigle', 'action_type_4_sigle',
	#	   'action_type_5_sigle', 'action_type_0_all', 'action_type_1_all',
	#	   'action_type_2_all', 'action_type_3_all', 'action_type_4_all',
	#	   'action_type_5_all'
    +- OnlineTest:  feature_num:59 
        --F1 Score: 0.80172018, yuzhi: 0.4
        --pre_user_num: 24358 
    +- OffLineTest 
    +-OnLine
        --F1 Score：0.818883
		
0610-1:
	# 数据集划分  data1：1-15，16-22； data2:9-23， 24-30； data3：1-30
	# drop： 'login_sum','login_max','loginvar','loginmean','login_3_cnt','login_week_cnt'
	# add:	'page_0_sigle', 'page_1_sigle', 'page_2_sigle', 'page_3_sigle',
	#	   'page_4_sigle', 'page_0_all', 'page_1_all', 'page_2_all', 'page_3_all',
	#	   'page_4_all', 'action_type_0_sigle', 'action_type_1_sigle',
	#	   'action_type_2_sigle', 'action_type_3_sigle', 'action_type_4_sigle',
	#	   'action_type_5_sigle', 'action_type_0_all', 'action_type_1_all',
	#	   'action_type_2_all', 'action_type_3_all', 'action_type_4_all',
	#	   'action_type_5_all'
	# 特征选择
    +- OnlineTest:  feature_num:43 
        --F1 Score: 0.80159289, yuzhi: 0.4
        --pre_user_num: 24253 
    +- OffLineTest 
    +-OnLine
        --F1 Score：0.818549
0608-2:
	# 为了复现0.819586, 且把register_day改成距离窗口截点的距离
	# 数据集划分  data1：1-15，16-22； data2:9-23， 24-30； data3：1-30
	# drop： 'login_sum','login_max','loginvar','loginmean','login_3_cnt','login_week_cnt'
    +- OnlineTest:  feature_num: 48 
        --F1 Score: 0.8020, yuzhi: 0.4
        --pre_user_num: 24485 
    +- OffLineTest 
    +-OnLine
        --F1 Score：0.819837

0611-1:
	# 0608-2的基础上
	#drop：'login_sum','login_max','loginvar','loginmean','login_3_cnt','login_week_cnt','page_sum','page_0_sigle','page_1_sigle','page_2_sigle','page_3_sigle','page_4_sigle','action_type_sum','action_type_0_sigle','action_type_1_sigle','action_type_2_sigle','action_type_3_sigle','action_type_4_sigle','action_type_5_sigle'
	# 特征选择
	# 调参
    +- OnlineTest:  feature_num: 41 
        --F1 Score: 0.8034, yuzhi: 0.4
        --pre_user_num: 24800 
    +- OffLineTest 
    +-OnLine
        --F1 Score：0.82000066
		
0612-1:
	# 0608-2的基础上
	#drop：'login_sum','login_max','loginvar','loginmean','login_3_cnt','login_week_cnt','page_sum','page_0_sigle','page_1_sigle','page_2_sigle','page_3_sigle','page_4_sigle','action_type_sum','action_type_0_sigle','action_type_1_sigle','action_type_2_sigle','action_type_3_sigle','action_type_4_sigle','action_type_5_sigle'
	#调参：
		''' max_depth=6,
            n_estimators = 280,
            learning_rate =0.05,     
            objective = 'binary',
            num_leaves=25,
			boosting_type = 'dart',
			feature_fraction=0.5,
			lambda_l1=1,
			lambda_l2=0.5,
			subsample=0.7'''
    +- OnlineTest:  feature_num: 103 
        --F1 Score: 0.8030053, yuzhi: 0.4
        --pre_user_num: 24949 
    +- OffLineTest 
    +-OnLine
        --F1 Score：0.820363
		
0612-2:
	# 0608-2的基础上
	#drop：'login_sum','login_max','loginvar','loginmean','login_3_cnt','login_week_cnt'
	#调参：
		''' max_depth=6,
            n_estimators = 280,
            learning_rate =0.05,     
            objective = 'binary',
            num_leaves=25,
			boosting_type = 'dart',
			feature_fraction=0.5,
			lambda_l1=1,
			lambda_l2=0.5,
			subsample=0.7'''
    +- OnlineTest:  feature_num: 48 
        --F1 Score: 0.802220, yuzhi: 0.4
        --pre_user_num: 24911 
    +- OffLineTest 
    +-OnLine
        --F1 Score：
		
0613-1:
	# 0608-2的基础上
	#drop：'login_sum','login_max','loginvar','loginmean','login_3_cnt','login_week_cnt'
	# 特征选择：
		'''
		   'login_day_min', 'device_type', 'login_week_arg_cnt', 'register_type',
		   'act_last_cnt', 'login_day_std', 'action_type_0', 'act_week_cnt',
		   'page_1', 'act_3_cnt', 'login_cnt', 'page_0', 'act_day_std', 'actmean',
		   'page_2', 'login_3_arg_cnt', 'register_day', 'act_sum', 'act_cnt',
		   'action_type_1', 'action_type_2', 'act_day_min', 'actvar',
		   'act_day_max', 'act_max', 'page_3', 'video_last_cnt', 'action_type_3',
		   'page_4', 'video_3_cnt', 'videomean', 'video_sum', 'is_author',
		   'page_3_7_cnt', 'action_type_1_7_cnt', 'video_day_min',
		   'video_week_cnt', 'action_type_0_7_cnt', 'video_day_max', 'video_cnt',
		   'videovar', 'action_type_2_7_cnt', 'page_3_3_cnt', 'video_day_std',
		   'action_type_0_1_cnt', 'action_type_0_3_cnt', 'action_type_5',
		   'action_type_1_3_cnt', 'page_0_1_cnt', 'video_max', 'page_0_7_cnt',
		   'page_0_3_cnt'
		'''
	#调参：
		''' max_depth=6,
            n_estimators = 280,
            learning_rate =0.05,     
            objective = 'binary',
            num_leaves=25,
			boosting_type = 'dart',
			feature_fraction=0.5,
			lambda_l1=1,
			lambda_l2=0.5,
			subsample=0.7
		'''
    +- OnlineTest:  feature_num: 52 
        --F1 Score: 0.8026616, yuzhi: 0.4
        --pre_user_num: 24902 
    +- OffLineTest 
    +-OnLine
        --F1 Score：

