import pandas as pd
from joblib import load
from os import system

model_duo = load("./project/pubg_duo.pkl")
model_duo_fpp = load("./model/pubg_duo_fpp.pkl")

pubg_test_duoDF_ori: pd.DataFrame = pd.read_pickle("./project/pubg_test_duoDF.pkl")
pubg_test_duo_fppDF_ori: pd.DataFrame = pd.read_pickle(
    "./DataFrame/pubg_test_duo_fppDF.pkl"
)

drop_features_low_connection = [
    "killPoints",
    "kills",
    "maxPlace",
    "rideDistance",
    "roadKills",
    "swimDistance",
    "vehicleDestroys",
]

pubg_test_duoDF = pubg_test_duoDF_ori.drop(drop_features_low_connection, axis=1)
pubg_test_duo_fppDF = pubg_test_duo_fppDF_ori.drop(drop_features_low_connection, axis=1)

print()
system("cls")

while True:
    print("==========================================")
    print("  PUBG: BATTLEGROUNDS 승률 예측 프로그램")
    print("==========================================")
    print("  매치 타입")
    print("------------------------------------------")
    print("  1. Duo(1인칭)")
    print("  2. Duo(3인칭)")
    print("------------------------------------------")
    matchType = int(input("매치 타입을 선택하세요(종료 : -1) : "))
    system("cls")

    if matchType == -1:
        break

    print("==========================================")
    print("  PUBG: BATTLEGROUNDS 승률 예측 프로그램")
    print("==========================================")
    print("  선택한 플레이어의 승률을 예측합니다")
    print("------------------------------------------")

    num = int(input("승률을 예측할 플레이어의 번호를 입력하세요(뒤로가기 : -1) : "))
    system("cls")

    if num == -1:
        continue

    assists = int(pubg_test_duoDF.iloc[num]["assists"])
    boosts = int(pubg_test_duoDF.iloc[num]["boosts"])
    damageDealt = pubg_test_duoDF.iloc[num]["damageDealt"]
    DBNOs = int(pubg_test_duoDF.iloc[num]["DBNOs"])
    headshotKills = int(pubg_test_duoDF.iloc[num]["headshotKills"])
    heals = int(pubg_test_duoDF.iloc[num]["heals"])
    killPlace = int(pubg_test_duoDF.iloc[num]["killPlace"])
    killStreaks = int(pubg_test_duoDF.iloc[num]["killStreaks"])
    longestKill = pubg_test_duoDF.iloc[num]["longestKill"]
    matchDuration = int(pubg_test_duoDF.iloc[num]["matchDuration"])
    numGroups = int(pubg_test_duoDF.iloc[num]["numGroups"])
    revives = int(pubg_test_duoDF.iloc[num]["revives"])
    teamKills = int(pubg_test_duoDF.iloc[num]["teamKills"])
    walkDistance = pubg_test_duoDF.iloc[num]["walkDistance"]
    weaponsAcquired = int(pubg_test_duoDF.iloc[num]["weaponsAcquired"])
    winRankPoints = int(pubg_test_duoDF.iloc[num]["winRankPoints"])

    print("==========================================")
    print("  PUBG: BATTLEGROUNDS 승률 예측 프로그램")
    print("==========================================")
    print(f"  {num}번 플레이어의 정보")
    print("------------------------------------------")
    print(f"  {num}번 플레이어 assists         : {assists}")
    print(f"  {num}번 플레이어 boosts          : {boosts}")
    print(f"  {num}번 플레이어 damageDealt     : {damageDealt}")
    print(f"  {num}번 플레이어 DBNOs           : {DBNOs}")
    print(f"  {num}번 플레이어 headshotKills   : {headshotKills}")
    print(f"  {num}번 플레이어 heals           : {heals}")
    print(f"  {num}번 플레이어 killPlace       : {killPlace}")
    print(f"  {num}번 플레이어 killStreaks     : {killStreaks}")
    print(f"  {num}번 플레이어 longestKill     : {longestKill}")
    print(f"  {num}번 플레이어 matchDuration   : {matchDuration}")
    print(f"  {num}번 플레이어 numGroups       : {numGroups}")
    print(f"  {num}번 플레이어 revives         : {revives}")
    print(f"  {num}번 플레이어 teamKills       : {teamKills}")
    print(f"  {num}번 플레이어 walkDistance    : {walkDistance}")
    print(f"  {num}번 플레이어 weaponsAcquired : {weaponsAcquired}")
    print(f"  {num}번 플레이어 winRankPoints   : {winRankPoints}")
    print("------------------------------------------")
    print(
        f"  {num}번 플레이어 승률 : {round(model_duo.predict(pubg_test_duoDF.iloc[num])*100, 2):.2f}%"
    )
    print("------------------------------------------")
    input("아무 키나 눌러 계속합니다.")
    system("cls")
