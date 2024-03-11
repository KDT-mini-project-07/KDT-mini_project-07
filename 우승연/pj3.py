#module import

from joblib import *
from sklearn.preprocessing import StandardScaler

# 전역변수
nsoloFPP = '../model/pubg_normal_solo_fpp.pkl'
nduoFPP = '../model/pubg_normal_duo_fpp.pkl'
nsquadFPP = '../model/pubg_normal_nsquad_fpp.pkl'
nsolo = '../model/pubg_normal_solo.pkl'
nduo = '../model/pubg_normal_duo.pkl'
nsquad = '../model/pubg_normal_nsquad.pkl'

#스케일러
nscaler = StandardScaler()

#모델 로딩
md_nsolofpp = load(nsoloFPP)
md_nduofpp = load(nduoFPP)
md_nsquadfpp = load(nsquadFPP)
md_nsolo = load(nsolo)
md_nduo = load(nduo)
md_nsquad = load(nsquad)

# 정보 입력

matchtype = input('Enter the data:Matchtype')
data = input('Enter the data:'
             'assists, boost,damagedealt, DBNOS, headshotkills, heals, killplace, killstreaks, longestkill,'
             'matchDuration, numGroups, revives, teamkills, walkdistance, weaponsAquired, winplacePerc, winRank ')
if len(data):
    datalist = list(map(float, data.split(',')))