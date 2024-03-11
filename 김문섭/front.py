import joblib
import os
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

RELEASE = False

def load_model(gametype = 'squad', isnormal = False):
    models = {}
    for x in os.listdir('./project/'):
        normal = x.find("normal") >= 0
        if x.split('.')[-1] == 'pkl' and x.find(gametype) >= 0 and normal == isnormal:
            models[x] = joblib.load('./project/'+x)
    return models

def return_menu(failed = False):
    if failed:
        print("잘못된 입력입니다. 엔터를 눌러 매뉴로 돌아가세요")
        input("")
    print("\033[2J\033[H", end="", flush=True)

def clearConsole():
    pass

def ans_squad(questionList, questionDescribe):
    print("==========================================")
    print("  PUBG: BATTLEGROUNDS 승률 예측 프로그램")
    print("==========================================")
    print("  매치 타입")
    print("------------------------------------------")
    print("  1. (1인칭)")
    print("  3. (3인칭)")
    print("------------------------------------------")
    user = input("")
    answerList = []
    perspective = -1
    if user.isnumeric() and  (int(user) == 1 or int(user) == 3):
        perspective = int(user)
    else:
        return_menu(True)
        return (answerList, perspective)
    
    for idx, x in enumerate(questionList):
        print(x + " 를 입력하세요(숫자만)" )
        print(f"{x}는 {questionDescribe[idx]} 입니다.")
        usernum = input('')
        if usernum.replace('.', '', 1).isnumeric():
            usernum = float(usernum)
        else:
            usernum = np.nan
        print(f"{usernum}이 입력으로 들어갑니다.")
        answerList.append(usernum)
    return (answerList, perspective)

def ans_custom(questionList, questionDescribe, RELEASE, debug_list):
    print("==========================================")
    print("  PUBG: BATTLEGROUNDS 승률 예측 프로그램")
    print("==========================================")
    print("  매치 타입")
    print("------------------------------------------")
    print("  1. (1인칭)")
    print("  3. (3인칭)")
    print("------------------------------------------")
    user = input("")
    answerList = []
    perspective = -1
    howmuchpeople = -1
    if user.isnumeric() and  (int(user) == 1 or int(user) == 3):
        perspective = int(user)
    else:
        # return_menu(True)
        return (answerList, perspective, howmuchpeople)
    print("==========================================")
    print("  PUBG: BATTLEGROUNDS 승률 예측 프로그램")
    print("==========================================")
    print("  인원수")
    print("------------------------------------------")
    print("  1. 1인 (solo)")
    print("  2. 2인 (duo)")
    print("  4. 4인 (squad)")
    print("------------------------------------------")
    
    user = input("")
    if user.isnumeric()  and  (int(user) == 1 or int(user) == 2 or int(user) == 4):
        howmuchpeople = int(user)
    else:
        # return_menu(True)
        perspective = -1
        return (answerList, perspective, howmuchpeople)

    if RELEASE:
        for idx, x in enumerate(questionList):
            print(x + " 를 입력하세요(숫자만)" )
            print(f"{x}는 {questionDescribe[idx]} 입니다.")
            usernum = input('')
            if usernum.replace('.', '', 1).isnumeric():
                usernum = float(usernum)
            else:
                usernum = np.nan
            print(f"{usernum}이 입력으로 들어갑니다.")
            answerList.append(usernum)
    else:
        answerList = debug_list
    return (answerList, perspective, howmuchpeople)



def main_squad():
    models = load_model()
    isfailed = False
    cols = ['assists', 'boosts', 'damageDealt', 'headshotKills', 'heals',
       'killPlace', 'killStreaks', 'longestKill', 'matchDuration', 'numGroups',
       'teamKills', 'walkDistance', 'weaponsAcquired', 'groupkillplace',
       'groupwalkDisance', 'groupkillStreaks', 'groupweaponsAcquired', 'score',
       ]

    cols_describe = [
        f"{i+1}번째 설명" for i in range(len(cols))
    ]
    
    user = [np.nan, np.nan,  172.9,  1.0,  np.nan,
        28.0, 1.0, 98.2, 1840.0, 25.0,
        np.nan,  2687.0,  7.0, 48.77777777777778,
        1806.0, 0.3333333333333333,  6.222222222222222,  1490.0,
    ]
    
    answerList = []
    perspacetive = 1
    if RELEASE:
        (answerList, perspacetive) = ans_squad(cols, cols_describe)
        user = answerList
    # if not RELEASE or len(answerList) == len(cols):
    useranswer = pd.DataFrame(dict(zip(cols, [[x] for x in user])))
    
    if perspacetive != -1:
        # print(models['pubg_squad_fpp.pkl'].predict(useranswer))

        if RELEASE:
            modelwhere = [(1,'fpp'), (3,'tpp')]
            for idx, modelstr in modelwhere:
                if idx == perspacetive:
                    model = models[f'pubg_squad_{modelstr}.pkl']
                    result = model.predict(useranswer)
            # print(f"{result[0]}")
        else:
            ### print(models.keys())
            result = models[list(models.keys())[0]].predict(useranswer)
        # print(f"상위 {(1 - result[0]) * 100:.2f}% 의 실력으로 예상됩니다.")
        print("==========================================")
        print("  PUBG: BATTLEGROUNDS 승률 예측 프로그램")
        print("==========================================")
        for idx, value in enumerate(answerList):
            print(f"플레이어의 {str(cols[idx]):25s} : {value}")
            
        print(f"상위 {(1 - result[0]) * 100:.2f}% 의 실력으로 예상됩니다.")
        input("엔터를 눌러 메인매뉴로 돌아가세요")
    else:
        print("입력이 잘못되었습니다.")
        isfailed = True
    
    return_menu(isfailed)

def main_duo():
    models = load_model('duo')
    # for name, value in models.items():
    #     print(value)
    # cols = ['assists', 'boosts', 'damageDealt', 'headshotKills', 'heals',
    #    'killPlace', 'killStreaks', 'longestKill', 'matchDuration', 'numGroups',
    #    'teamKills', 'walkDistance', 'weaponsAcquired', 'groupkillplace',
    #    'groupwalkDisance', 'groupkillStreaks', 'groupweaponsAcquired', 'score',
    #    ]
    cols = [
        'assists', 'boosts', 'damageDealt', 'DBNOs', 'headshotKills', 
        'heals', 'killPlace', 'killStreaks', 'longestKill', 'matchDuration', 
        'numGroups', 'revives', 'teamKills', 'walkDistance', 'weaponsAcquired', 
        'winRankPoints'
    ]
    

    cols_describe = [
        f"{i+1}번째 설명" for i in range(len(cols))
    ]
    
    user = [
        0.0, 2.0, 202.7, 1.0, 0.0,
        1.0, 60.0, 0.0, 0.0, 1931.0,
        45.0, 1.0, 0.0, 940.6, 8.0,
        1510.0
    ]
    
    answerList = []
    perspacetive = 1
    if RELEASE:
        (answerList, perspacetive) = ans_squad(cols, cols_describe)
        user = answerList
    # if not RELEASE or len(answerList) == len(cols):
    useranswer = pd.DataFrame(dict(zip(cols, [[x] for x in user])))

    if perspacetive != -1:
        # print(models['pubg_squad_fpp.pkl'].predict(useranswer))

        if RELEASE:
            modelwhere = [(1,'fpp'), (3,'tpp')]
            for idx, modelstr in modelwhere:
                if idx == perspacetive:
                    model =  models[f'pubg_duo_{modelstr}.pkl']
                    result = model.predict(useranswer)
            # print(f"{result[0]}")
        else:
            ### print(models.keys())
            result = models[list(models.keys())[0]].predict(useranswer)
        # print(f"상위 {(1 - result[0]) * 100:.2f}% 의 실력으로 예상됩니다.")
        print("==========================================")
        print("  PUBG: BATTLEGROUNDS 승률 예측 프로그램")
        print("==========================================")
        for idx, value in enumerate(answerList):
            print(f"플레이어의 {str(cols[idx]):25s} : {value}")
            
        print(f"상위 {(1 - result[0]) * 100:.2f}% 의 실력으로 예상됩니다.")
        input("엔터를 눌러 메인매뉴로 돌아가세요")
    else:
        print("입력이 잘못되었습니다.")
    
    return_menu()
    

def main_single():
    models = load_model('solo')
    # for name, value in models.items():
    #     print(value)
    # cols = ['assists', 'boosts', 'damageDealt', 'headshotKills', 'heals',
    #    'killPlace', 'killStreaks', 'longestKill', 'matchDuration', 'numGroups',
    #    'teamKills', 'walkDistance', 'weaponsAcquired', 'groupkillplace',
    #    'groupwalkDisance', 'groupkillStreaks', 'groupweaponsAcquired', 'score',
    #    ]
    cols = ['assists', 'boosts', 'damageDealt', 'headshotKills', 'heals',
       'killPlace', 'killStreaks', 'longestKill', 'matchDuration',
       'walkDistance', 'weaponsAcquired', 'winRankPoints']
    cols_describe = [
        f"{i+1}번째 설명" for i in range(len(cols))
    ]
    
    user = [0.0, 0.0, 323.2, 2.0, 0.0, 12.0, 1.0, 81.09, 1347.0, 108.8, 2.0, 1517.0]
    
    answerList = []
    perspacetive = 1
    if RELEASE:
        (answerList, perspacetive) = ans_squad(cols, cols_describe)
        user = answerList
    # if not RELEASE or len(answerList) == len(cols):
    useranswer = pd.DataFrame(dict(zip(cols, [[x] for x in user])))


    if perspacetive != -1:
        # print(models['pubg_squad_fpp.pkl'].predict(useranswer))

        if RELEASE:
            modelwhere = [(1,'fpp'), (3,'tpp')]
            for idx, modelstr in modelwhere:
                if idx == perspacetive:
                    model =  models[f'solo{modelstr}_model.pkl']
                    result = model.predict(useranswer)
            # print(f"{result[0]}")
        else:
            ### print(models.keys())
            result = models[list(models.keys())[0]].predict(useranswer)
        # print(f"상위 {(1 - result[0]) * 100:.2f}% 의 실력으로 예상됩니다.")
        print("==========================================")
        print("  PUBG: BATTLEGROUNDS 승률 예측 프로그램")
        print("==========================================")
        for idx, value in enumerate(answerList):
            print(f"플레이어의 {str(cols[idx]):25s} : {value}")
            
        print(f"상위 {(1 - result[0]) * 100:.2f}% 의 실력으로 예상됩니다.")
        input("엔터를 눌러 메인매뉴로 돌아가세요")
    else:
        print("입력이 잘못되었습니다.")
    
    return_menu()
    pass

def main_others():
    isfailed = False
    models = load_model('normal', True)
    # for name, value in models.items():
    #     print(value)
    # cols = ['assists', 'boosts', 'damageDealt', 'headshotKills', 'heals',
    #    'killPlace', 'killStreaks', 'longestKill', 'matchDuration', 'numGroups',
    #    'teamKills', 'walkDistance', 'weaponsAcquired', 'groupkillplace',
    #    'groupwalkDisance', 'groupkillStreaks', 'groupweaponsAcquired', 'score',
    #    ]
    cols = ['assists', 'boosts', 'damageDealt', 'DBNOs', 'headshotKills', 'heals',
       'killPlace', 'killStreaks', 'longestKill', 'matchDuration', 'numGroups',
       'revives', 'teamKills', 'walkDistance', 'weaponsAcquired',
       'winPlacePerc'
    ]

    cols_describe = [
        f"{i+1}번째 설명" for i in range(len(cols))
    ]
    
    user = [
            2.0, 0.0, 540.3, 0.0, 0.0, 2.0,
            31.0, 1.0, 71.35, 793.0, 18.0,
            0.0, 0.0, 1404.0, 15.0,
            0.3721
    ]
    
    answerList = []
    perspacetive = 1
    (answerList, perspacetive, howmuchpeople) = ans_custom(cols, cols_describe, RELEASE, user)
    user = answerList
    # if not RELEASE or len(answerList) == len(cols):
    useranswer = pd.DataFrame(dict(zip(cols, [[x] for x in user])))
    peopledefine = [
        (1, 'solo'),
        (2, 'duo'),
        (4, 'squad'),
    ]
    if perspacetive != -1:
        # print(models['pubg_squad_fpp.pkl'].predict(useranswer))

        if RELEASE:
            modelwhere = [(1,'fpp'), (3,'tpp')]
            for idx, modelstr in modelwhere:
                for idxpeople, peoplestr in peopledefine:
                    if idx == perspacetive and idxpeople == howmuchpeople:
                        model =  models[f'pubg_normal_{peoplestr}_{modelstr}.pkl']
                        result = model.predict(useranswer)
            # print(f"{result[0]}")
        else:
            ### print(models.keys())
            result = models[list(models.keys())[0]].predict(useranswer)
        # print(f"상위 {(1 - result[0]) * 100:.2f}% 의 실력으로 예상됩니다.")
        print("==========================================")
        print("  PUBG: BATTLEGROUNDS 승률 예측 프로그램")
        print("==========================================")
        for idx, value in enumerate(answerList):
            print(f"플레이어의 {str(cols[idx]):25s} : {value}")
            
        print(f"이 사람의 획득 예상 점수는 {float(result[0]):.2f} 입니다.")
        input("엔터를 눌러 메인매뉴로 돌아가세요")
    else:
        print("입력이 잘못되었습니다.")
        isfailed = True
        
    return_menu(isfailed)
    pass

def main():
    global RELEASE
    return_menu()
    print("==========================================")
    print("  PUBG: BATTLEGROUNDS 승률 예측 프로그램")
    print("==========================================")
    print("  선택한 플레이어의 승률을 예측합니다")
    print("------------------------------------------")
    print(f"Release Mode 여부 : {RELEASE}")
    print("------------------------------------------")
    print("1. 스쿼드 모드\n2. 듀오 모드\n3. 싱글 모드\n4. 노멀 플레이 모드\n5. 릴리즈모드 전환\n0. 종료\n\n")
    print("원하시는 매뉴를 선택해주세요")
    user = input("")
    
    if user.isnumeric():
        switch = int(user)
        if switch == 1:
            main_squad()
        elif switch == 2:
            main_duo()
        elif switch == 3:
            main_single()
        elif switch == 4:
            main_others()
        elif switch == 5:
            RELEASE = True if RELEASE == False else False
        elif switch == 0:
            return False
        else:
            print("잘못된 입력입니다.")
    else:
        print("잘못된 입력입니다.")
    return True

if __name__ == '__main__':
    program = True
    while program:
        program = main()
    
    print("프로그램을 종료합니다. 감사합니다.")
        
