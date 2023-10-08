from enum import Enum
from dataclasses import dataclass


class Findability(Enum):
    VERY_OFTEN = 'とてもよく'
    OFTEN = 'よく'
    SOMETIMES = 'ときどき'
    RARELY = 'あまり'
    VERY_RARELY = 'めったに'
    RARELY_METAL = 'あまりメタル系'
    NOT_APPLICABLE = '地図での出現なし'


class ExpRatio(Enum):
    P_ZERO = '1.0倍'
    P_ONE = '1.1倍'
    P_TWO = '1.2倍'
    NO_DATA = 'データなし'


@dataclass
class Monster:
    no: int
    name: str
    exp_ratio: str
    findability: Findability


class MonsterFactory():
    def __init__(self, df):
        self.df = df

    def create_monster_by_name(self, monster_name: str):
        filtered_df = self.df[self.df['モンスター名'] == monster_name]
        if not filtered_df.empty:
            target = filtered_df.iloc[0]

            for findability_elem in Findability:
                if findability_elem.value == target['見かけやすさ（地図）']:
                    break

            for exp_ratio_elem in ExpRatio:
                if exp_ratio_elem.value == target['経験値倍率']:
                    break

            return Monster(
                no=target['図鑑No.'],
                name=target['モンスター名'],
                exp_ratio=exp_ratio_elem,
                findability=findability_elem
            )
        else:
            raise ValueError(f'{monster_name} は存在しません。')

    def create_monster_by_no(self, monster_no: str):
        filtered_df = self.df[self.df['図鑑No.'] == monster_no]
        if not filtered_df.empty:
            target = filtered_df.iloc[0]

            for findability_elem in Findability:
                if findability_elem.value == target['見かけやすさ（地図）']:
                    break

            for exp_ratio_elem in ExpRatio:
                if exp_ratio_elem.value == target['経験値倍率']:
                    break

            return Monster(
                no=target['図鑑No.'],
                name=target['モンスター名'],
                exp_ratio=exp_ratio_elem,
                findability=findability_elem
            )
        else:
            raise ValueError(f'図鑑No.{monster_no} は存在しません。')
