from enum import Enum
from dataclasses import dataclass

import pandas as pd

class Findability(Enum):
    VERY_OFTEN = 'a.とてもよく見かける'
    OFTEN = 'b.よく見かける'
    SOMETIMES = 'c.ときどき見かける'
    RARELY = 'd.あまり見かけない'
    VERY_RARELY = 'e.めったに見かけない'
    RARELY_METAL = 'm.あまり見かけない（メタル系）'
    NOT_APPLICABLE = 'z.地図での出現なし（未登録）'

    def short_str(self):
        if self == Findability.VERY_OFTEN:
            return 'とて'
        if self == Findability.OFTEN:
            return 'よく'
        if self == Findability.SOMETIMES:
            return 'とき'
        if self == Findability.RARELY:
            return 'あま'
        if self == Findability.VERY_RARELY:
            return 'めっ'
        if self == Findability.RARELY_METAL:
            return 'メタ'
        if self == Findability.NOT_APPLICABLE:
            return '未登録'
        return '不明'


class ExpRatio(Enum):
    P_ZERO = '1.0倍'
    P_ONE = '1.1倍'
    P_TWO = '1.2倍'
    NO_DATA = 'データなし'

    def short_str(self):
        if self == ExpRatio.P_ZERO:
            return '1.0'
        if self == ExpRatio.P_ONE:
            return '1.1'
        if self == ExpRatio.P_TWO:
            return '1.2'
        if self == ExpRatio.NO_DATA:
            return '-'
        return '不明'

class StrengthWeakness:

    def __init__(self, frizz: float = None, sizz: float = None, bang: float = None, crack: float = None, woosh: float = None, zap: float = None, zam: float = None, crag: float = None):
        # ja:メラ	ギラ	イオ	ヒャド	バギ	デイン	ドルマ	ジバリア
        # en:Frizz    Sizz	Bang	Crack	Woosh	Zap	Zam	Crag
        self.frizz = frizz
        self.sizz = sizz
        self.bang = bang
        self.crack = crack
        self.woosh = woosh
        self.zap = zap
        self.zam = zam
        self.crag = crag

    def to_list(self):
        arr = []
        # float to str
        for elem in [self.frizz, self.sizz, self.bang, self.crack, self.woosh, self.zap, self.zam, self.crag]:
            if elem is not None:
                arr.append(str(elem).rstrip('0').rstrip('.'))
            else:
                arr.append('-')

        return arr

    @staticmethod
    def to_column(ja=True):
        if ja:
            return ['メラ', 'ギラ', 'イオ', 'ヒャ', 'バギ', 'デイ', 'ドル', 'ジバ']
        else:
            return ['Frizz', 'Sizz', 'Bang', 'Crack', 'Woosh', 'Zap', 'Zam', 'Crag']


@dataclass
class Monster:
    no: int
    name: str
    exp_ratio: str
    findability: Findability
    strength_weakness: StrengthWeakness


class MonsterFactory():
    def __init__(self, df, df_sw):
        #self.df = df
        #self.df_sw = df_sw
        merged = df.merge(df_sw[['図鑑No.','メラ','ギラ','イオ','ヒャド','バギ','デイン','ドルマ','ジバリア']],
                          on='図鑑No.', how='left', suffixes=('', '_right'))
        for col in df.columns:
            if col + "_right" in merged.columns:
                merged[col] = merged[col + "_right"]
        self.df = merged.drop(columns=[col for col in merged.columns if "_right" in col])


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

            # 耐性・弱点
            def trans(val):
                if val == '-':
                    return None
                if val == '無効':
                    return 0.0
                return float(val)

            frizz = trans(target['メラ'])
            sizz = trans(target['ギラ'])
            bang = trans(target['イオ'])
            crack = trans(target['ヒャド'])
            woosh = trans(target['バギ'])
            zap = trans(target['デイン'])
            zam = trans(target['ドルマ'])
            crag = trans(target['ジバリア'])
            strength_weakness = StrengthWeakness(frizz, sizz, bang, crack, woosh, zap, zam, crag)

            return Monster(
                no=target['図鑑No.'],
                name=target['モンスター名'],
                exp_ratio=exp_ratio_elem,
                findability=findability_elem,
                strength_weakness=strength_weakness
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

            # 耐性・弱点
            def trans(val):
                if val == '-':
                    return None
                if val == '無効':
                    return 0.0
                return float(val)

            frizz = trans(target['メラ'])
            sizz = trans(target['ギラ'])
            bang = trans(target['イオ'])
            crack = trans(target['ヒャド'])
            woosh = trans(target['バギ'])
            zap = trans(target['デイン'])
            zam = trans(target['ドルマ'])
            crag = trans(target['ジバリア'])
            strength_weakness = StrengthWeakness(frizz, sizz, bang, crack, woosh, zap, zam, crag)

            return Monster(
                no=target['図鑑No.'],
                name=target['モンスター名'],
                exp_ratio=exp_ratio_elem,
                findability=findability_elem,
                strength_weakness=strength_weakness
            )
        else:
            raise ValueError(f'図鑑No.{monster_no} は存在しません。')
