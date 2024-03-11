import pandas as pd
import joblib, os


class Color:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    B_BLACK = "\033[90m"
    B_RED = "\033[91m"
    B_GREEN = "\033[92m"
    B_YELLOW = "\033[93m"
    B_BLUE = "\033[94m"
    B_MAGENTA = "\033[95m"
    B_CYAN = "\033[96m"
    B_WHITE = "\033[97m"

    RESET = "\033[0m"
    UNDERLINE = "\033[4m"


def selectMatchType():
    while True:
        print("==========================================")
        print("  PUBG: BATTLEGROUNDS 승률 예측 프로그램")
        print("==========================================")
        print("   매치 타입")
        print(" ----------------")
        print("  1. Solo")
        print("  2. Solo-fpp")
        print("  3. Duo")
        print("  4. Duo-fpp")
        print("  5. Squad")
        print("  6. Squad-fpp")
        print("  0. 종료")
        print(" ----------------")
        matchType = input(" 매치 타입을 선택하세요 : ")
        if matchType.isdecimal() and matchType in [f"{i}" for i in range(7)]:
            matchType = int(matchType)
            break
        else:
            os.system("cls")
            print(Color.B_RED + " 0~6 사이의 정수를 입력하세요." + Color.RESET)
    os.system("cls")
    return matchType


def selectCompetitiveFlag():
    while True:
        print("==========================================")
        print("  PUBG: BATTLEGROUNDS 승률 예측 프로그램")
        print("==========================================")
        print("   게임 타입")
        print(" ----------------")
        print("  1. 랭크 게임")
        print("  2. 일반 게임")
        print("  0. 뒤로가기")
        print(" ----------------")
        competitiveFlag = input(" 게임 타입을 선택하세요 : ")
        if competitiveFlag.isdecimal() and competitiveFlag in [
            f"{i}" for i in range(3)
        ]:
            competitiveFlag = int(competitiveFlag)
            break
        else:
            os.system("cls")
            print(Color.B_RED + " 0~2 사이의 정수를 입력하세요." + Color.RESET)
    os.system("cls")
    return competitiveFlag


def continueCheck():
    print(" 계속하시겠습니까?")
    pass


def importScaler(scaler_name):
    scaler_dir = "./DATA/scaler/"
    scaler_filename = scaler_dir + scaler_name
    try:
        scaler = joblib.load(scaler_filename)
    except:
        scaler = None
    return scaler


def importModel(model_name):
    model_dir = "./DATA/model/"
    model_filename = model_dir + model_name
    model = joblib.load(model_filename)
    return model


def importData(data_name: str, start: int = 0, end: int = 5):
    data_dir = "./DATA/DataFrame/"
    data_filename = data_dir + data_name
    df = pd.read_pickle(data_filename)
    return df.iloc[start:end]


def predictScore(scaler, model, df: pd.DataFrame, matchType: int, competitiveFlag: int):
    drop_features_low_connection = [
        "killPoints",
        "kills",
        "maxPlace",
        "rideDistance",
        "roadKills",
        "swimDistance",
        "vehicleDestroys",
    ]
    drop_features_low_connection_solo = [
        "DBNOs",
        "killPoints",
        "kills",
        "maxPlace",
        "numGroups",
        "revives",
        "rideDistance",
        "roadKills",
        "swimDistance",
        "vehicleDestroys",
    ]

    if matchType in [1, 2] and competitiveFlag == 1:
        selectDF = df.drop(drop_features_low_connection_solo, axis=1)
    else:
        selectDF = df.drop(drop_features_low_connection, axis=1)
    if scaler != None:
        selectDF = scaler.transform(selectDF)
    os.system("cls")
    print("==========================================")
    print("  PUBG: BATTLEGROUNDS 승률 예측 프로그램")
    print("==========================================")
    print("  플레이어의 승률을 예측합니다")
    print("------------------------------------------")

    for i in range(5):
        print(
            f"{i:3}번 플레이어의 승률 : {round(model.predict(selectDF.iloc[i])*100, 2):.2f}"
        )


def main():
    os.system("cls")

    while True:
        scaler_name = "pubg_scaler_"
        model_name = "pubg_"
        data_name = "pubg_test_"
        matchType = selectMatchType()
        if matchType == 1:
            scaler_name += "solo"
            model_name += "solo"
            data_name += "solo"
        elif matchType == 2:
            scaler_name += "solo_fpp"
            model_name += "solo_fpp"
            data_name += "solo_fpp"
        elif matchType == 3:
            scaler_name += "duo"
            model_name += "duo"
            data_name += "duo"
        elif matchType == 4:
            scaler_name += "duo_fpp"
            model_name += "duo_fpp"
            data_name += "duo_fpp"
        elif matchType == 5:
            scaler_name += "squad"
            model_name += "squad"
            data_name += "squad"
        elif matchType == 6:
            scaler_name += "squad_fpp"
            model_name += "squad_fpp"
            data_name += "squad_fpp"
        else:
            print("프로그램을 종료합니다.")
            break

        competitiveFlag = selectCompetitiveFlag()
        if competitiveFlag == 1:
            scaler_name += ".pkl"
            model_name += ".pkl"
            data_name += "DF.pkl"
        elif competitiveFlag == 2:
            scaler_name += "_normal.pkl"
            model_name += "_normal.pkl"
            data_name += "_normalDF.pkl"
        else:
            continue

        model = importModel(model_name)
        data = importData(data_name)
        scaler = importScaler(scaler_name)
        # model.predict()
        # print(model)
        # print(data)
        # print(scaler)
        predictScore(scaler, model, data, matchType, competitiveFlag)
        input()
        os.system("cls")


if __name__ == "__main__":
    main()
