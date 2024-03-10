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


def importModel(model_name):
    model_dir = "../DATA/"
    model_filename = model_dir + model_name
    model = joblib.load(model_filename)
    return model


def importTestData(num: int = 10):
    pubg_testDF_ori: pd.DataFrame = pd.read_pickle("../DATA/pubg_testDF_ori.pkl")
    drop_features_replace = ["rankPoints", "winPoints"]
    winRankPoints = (
        pubg_testDF_ori["rankPoints"].replace(-1, 0) + pubg_testDF_ori["winPoints"]
    )
    pubg_testDF = pd.concat(
        [
            pubg_testDF_ori.drop(drop_features_replace, axis=1),
            winRankPoints.rename("winRankPoints"),
        ],
        axis=1,
    )
    return pubg_testDF


def selectTarget(df: pd.DataFrame, matchType: str):
    df = df[df.columns["matchType"] == matchType]
    num = df.shape[1] + 1
    drop_features_object = ["Id", "groupId", "matchId"]
    drop_features_low_connection = [
        "killPoints",
        "kills",
        "maxPlace",
        "rideDistance",
        "roadKills",
        "swimDistance",
        "vehicleDestroys",
    ]
    while True:
        print(" 승률 예측 플레이어 선택")
        print(f" 데이터가 준비된 플레이어의 수 : {num}")
        targetNum = input(f"승률을 예측할 플레이어를 선택하세요 : ")
        if targetNum.isdecimal() and (0 <= int(targetNum) < num):
            targetNum = int(targetNum)
            selectDF = df.iloc[[targetNum]]
            playerID = selectDF["id"][0]
            selectDF = selectDF.drop(drop_features_object, axis=1)
            break
        else:
            print(f"0~{num-1} 사이의 정수를 입력하세요.")
    pass


def main():
    while True:
        model_name = "pubg_"
        matchType = selectMatchType()
        if matchType == 1:
            model_name += "solo"
        elif matchType == 2:
            model_name += "solo_fpp"
        elif matchType == 3:
            model_name += "duo"
        elif matchType == 4:
            model_name += "duo_fpp"
        elif matchType == 5:
            model_name += "squad"
        elif matchType == 6:
            model_name += "squad_fpp"
        else:
            print("프로그램을 종료합니다.")
            break

        competitiveFlag = selectCompetitiveFlag()
        if competitiveFlag == 1:
            model_name += ".pkl"
        elif competitiveFlag == 2:
            model_name += "_normal.pkl"
        else:
            continue

        model = importModel(model_name)
        model.predict()
        print(model)


if __name__ == "__main__":
    main()
