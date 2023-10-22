import os

import streamlit as st

import pandas as pd

from monster import MonsterFactory, EncountMonsters
import settings


def judge(monster_nos, monster_factory, view_detail=False):
    encount_monsters = EncountMonsters(monster_factory, monster_nos)
    msg = encount_monsters.judge_mass()
    return {
        'df': encount_monsters.to_df(view_detail=view_detail),
        'msg': msg
    }


def main():
    st.set_page_config(
        page_title='宝の地図大量発生判定',
        page_icon='🗺'
    )
    st.write('ver.'+settings.version)
    st.title('宝の地図大量発生判定')
    st.write('出現モンスターの図鑑No.を入力してください。')


    if 'monster_factory' in st.session_state:
        monster_factory = st.session_state.get('monster_factory')
    else:
        df = pd.read_csv('monster_list.csv')
        df_sw = pd.read_csv('strength_weakness_list.csv')
        monster_factory = MonsterFactory(df, df_sw)
        st.session_state.monster_factory = monster_factory

    monster_nos = []
    for i in range(12):
        col1, col2 = st.columns([1, 2])
        with col1:
            number = st.number_input(f'モンスター{i+1}', min_value=0, value=0, key=f'monster_{i}')
            monster_nos.append(number)
        with col2:
            try:
                monster = monster_factory.create_monster_by_no(number)
                name = f'{monster.name}（{monster.findability.short_str()},{monster.exp_ratio.value}）'
            except:
                name = ''
            col2.markdown("##")
            col2.markdown(name)

    view_detail = st.checkbox('耐性・弱点表示', key='view_detail')

    if st.button('判定'):

        try:
            result = judge(monster_nos
                # 29,74,121,159,161,166,222,277,326,336,455,520
            , monster_factory, view_detail)

            st.subheader(result['msg'])

            st.table(result['df'])
        except Exception as e:
            st.error(e)



    st.markdown('''
    #### 参考元
- 判定ロジック
  - すずしろ店長様
    - https://twitter.com/Lv20_HP140MP80/status/1709521858377466185
- データソース
  - すずしろ店長様
    - https://docs.google.com/spreadsheets/d/1Hz-v2lBDV5khxgFRMZAhBDWqn65Inv3vjD2NpS8FwsM/edit#gid=1463845531
  - さおちゃん様
    - https://docs.google.com/spreadsheets/d/13oEPbzv0MHVW4CwmC17aL8kbU6_pj5llvO4aHvdh8OA/edit#gid=1889598122''')

if __name__ == '__main__':

    main()
