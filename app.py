import os

import streamlit as st
import pandas as pd
from io import StringIO

from monster import MonsterFactory, EncountMonsters



def judge(monster_nos, monster_factory):
    encount_monsters = EncountMonsters(monster_factory, monster_nos)
    msg = encount_monsters.judge_mass()
    return {
        'df': encount_monsters.to_df(),
        'msg': msg
    }


def main():

    st.title('宝の地図大量発生判定')

    df = pd.read_csv('monster_list.csv')
    monster_factory = MonsterFactory(df)

    monster_nos = []
    for i in range(12):
        col1, col2 = st.columns([1, 3])
        with col1:
            col1.markdown("##")
            col1.markdown(f'モンスター{i+1}:')
            #st.write(f'モンスター{i+1}:')
        with col2:
            # スタイルを適用してスリムな入力欄を作成
            number = st.number_input(f'モンスター{i+1}', value=0, key=f'monster_{i}', label_visibility='hidden')
            monster_nos.append(number)


    if st.button('判定'):

        result = judge(monster_nos
            # 29,74,121,159,161,166,222,277,326,336,455,520
        , monster_factory)

        st.write(result['msg'])

        st.dataframe(result['df'])






if __name__ == '__main__':
    main()
