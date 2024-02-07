# -*- coding:utf-8 -*-

import streamlit as st 
import pandas as pd
from data_collect import load_data
from data_collect import Range
from data_collect import load_geojsondata
import plotly.express as px 
import plotly.graph_objects as go 

def main():
    df=load_data()
    # 대시보드 제목
    st.title('부동산 용도별 평균 거래가격 시각화 앱')
    st.subheader('법정동별 평균 거래가')
    # 사용자 입력을 위한 selectbox 생성
    selected_house_type = st.selectbox(
        '용도를 선택하세요.',
        options=list(df['HOUSE_TYPE'].unique())
    )
    sgg_nm_sort=sorted(df['SGG_NM'].unique())
    selected_sgg_nm = st.selectbox(
        '구를 선택하세요.',
        options=list(sgg_nm_sort)
    )
    
    # 출력하고자 하는 데이터 선택
    filtered_data = df.loc[(df['SGG_NM'] == selected_sgg_nm)&(df['HOUSE_TYPE']==selected_house_type)]
    grouped_data = filtered_data.groupby('BJDONG_NM')['OBJ_AMT'].mean().reset_index()

    # 막대 그래프 그리기
    fig=go.Figure()
    fig.add_trace(
        go.Bar(x=grouped_data.BJDONG_NM,y=grouped_data.OBJ_AMT,
    	    marker={'color':px.colors.qualitative.Dark24,
                        'line':{'color':'black','width':2},
                        'pattern':{'shape':'/'}})    
    )
    fig.update_layout(go.Layout(title={'text':f'{selected_sgg_nm} 법정동별 부동산 평균 거래가격',
                                  'font':{'color':'blue','size':30}},
                            xaxis={'title':{'text':'법정동 이름'},
                                   'gridwidth':1,'showgrid':True},
                            yaxis={'title':{'text':'평균 거래가격(만 원)'},
                                   'gridwidth':1,'showgrid':True},

    ))
    # 그래프 출력
    st.plotly_chart(fig)
    
    st.subheader('평수별 평균 거래가')
    #평수대별로 데이터 나눠서 새로운 컬럼생성
    df['Pyeong']=df['BLDG_AREA']/3.3
    df['Pyeong']=df['Pyeong'].astype('int64')
    df['Pyeong_range']=df['Pyeong'].apply(Range)
    
    # 사용자 입력을 위한 selectbox 생성
    selected_Pyeong = st.selectbox(
        '평수대를 선택하세요.',
        options=list(df['Pyeong_range'].unique())
    )
    st.write(selected_house_type)
    
    # 출력하고자 하는 데이터 선택
    filtered_data = df.loc[(df['Pyeong_range'] == selected_Pyeong)&(df['HOUSE_TYPE']==selected_house_type)]
    grouped_data = filtered_data.groupby('Pyeong')['OBJ_AMT'].mean().reset_index()
    
    # 막대 그래프 그리기
    fig=go.Figure()
    fig.add_trace(
        go.Bar(x=grouped_data.Pyeong,y=grouped_data.OBJ_AMT,
    	    marker={'color':px.colors.qualitative.Dark24,
                        'line':{'color':'black','width':2},
                        'pattern':{'shape':'/'}})    
    )
    fig.update_layout(go.Layout(title={'text':f'{selected_Pyeong} 부동산 평균 거래가격',
                                  'font':{'color':'blue','size':30}},
                            xaxis={'title':{'text':'평수대'},
                                   'gridwidth':1,'showgrid':True},
                            yaxis={'title':{'text':'평균 거래가격(만 원)'},
                                   'gridwidth':1,'showgrid':True},

    ))
    # 그래프 출력
    st.plotly_chart(fig)
    
    
    st.subheader('시간별 거래가격의 변화')
    st.write(selected_house_type)
    # 날짜 형식을 올바르게 지정하여 datetime으로 변환
    df['YearMonth'] = pd.to_datetime(df['DEAL_YMD'].astype(str).str.slice(0, 6), format='%Y%m').dt.strftime('%Y-%m')

    # 년월 별 OBJ_AMT 평균 계산
    filtered_data=df.loc[df['HOUSE_TYPE']==selected_house_type]
    monthly_avg_obj_amt = filtered_data.groupby('YearMonth')['OBJ_AMT'].mean().reset_index()

    # 선 그래프로 시각화: x축 정보를 'YYYY-MM' 형식으로 표시
    fig=go.Figure()
    fig.add_trace(
        go.Scatter(x=monthly_avg_obj_amt.YearMonth,y=monthly_avg_obj_amt.OBJ_AMT,mode='lines+markers',line_shape='spline')
    )
    fig.update_traces(line_color='blue',
                    line_width=2,
                    )
    
    fig.update_layout(go.Layout(title={'text':f'시간별 거래가격의 변화',
                                  'font':{'color':'blue','size':30}},
                            xaxis={'title':{'text':'시기'},
                                   'gridwidth':1,'showgrid':True},
                            yaxis={'title':{'text':'평균 거래가격(만 원)'},
                                   'gridwidth':1,'showgrid':True},))

    st.plotly_chart(fig)
    
    st.subheader('거래 검색기')
    
    show_list=['SGG_NM','BJDONG_NM','BONBEON','BUBEON','BLDG_NM','OBJ_AMT','BLDG_AREA','FLOOR']
    selected_multi_sgg_nm = st.multiselect(
        '구를 선택하세요.',
        options=list(df['SGG_NM'].unique())
    )
    selected_multi_house_type = st.multiselect(
        '용도를 선택하세요.',
        options=list(df['HOUSE_TYPE'].unique())
    )
    selected_multi_Pyeong = st.multiselect(
        '평수대를 선택하세요.',
        options=list(df['Pyeong_range'].unique())
    )
    
    filtered_data=df.loc[(df['SGG_NM'].isin(selected_multi_sgg_nm))
                         &(df['HOUSE_TYPE'].isin(selected_multi_house_type))
                         &(df['Pyeong_range'].isin(selected_multi_Pyeong)),
                         show_list]
    st.data_editor(filtered_data.head())
    
    st.subheader('gis 시각화')
    #geojson 파일 불러오기
    gdf=load_geojsondata()
    
    st.header('gis시각화')
    
    minn=st.number_input('min price')
    maxx=st.number_input('max price')
    
    floor=st.number_input('층수를 입력하세요',step=1,min_value=-1,max_value=68)
    pyeong=st.number_input('평수를 입력하세요',step=1)
    buildyear=st.number_input('건축연도를 입력하세요',step=1)
    alpha=st.slider('오차범위를 선택하세요',0,5,1)
    
    filtered_df = df.loc[(df['HOUSE_TYPE']=='아파트')&
                         ((df['FLOOR']<=floor+alpha)&(df['FLOOR']>=floor-alpha))&
                         ((df['Pyeong']<=pyeong+alpha)&(df['Pyeong']>=pyeong-alpha))&
                         ((df['BUILD_YEAR']<=buildyear+alpha)&(df['BUILD_YEAR']>=buildyear-alpha))]
    
    avg_obj_amt = filtered_df.groupby('SGG_NM')['OBJ_AMT'].mean().reset_index()
    avg_obj_amt.columns = ['SGG_NM', 'Avg_Obj_Amt']
    #geojson과 데이터프레임 병합
    merged_gdf = gdf.merge(avg_obj_amt, left_on='SIG_KOR_NM', right_on='SGG_NM')
    
    fig = px.choropleth_mapbox(merged_gdf,
                               geojson=merged_gdf.geometry.__geo_interface__,
                               locations=merged_gdf.index,
                               color='Avg_Obj_Amt',
                               color_continuous_scale="Viridis",
                               mapbox_style="carto-positron",
                               zoom=10,
                               center={"lat": 37.5650172, "lon": 126.9782914},
                               opacity=0.5,
                               labels={'Avg_Obj_Amt': '평균 거래액'},
                               hover_data={'SGG_NM': True, 'Avg_Obj_Amt': True}
                               )
    st.plotly_chart(fig)
    
    #k_columns=['접수년도','자치구명','법정동명','지번구분명','본번','부번','건물명','계약일','계약금액','건물면적','전체면적','층','취소일','건축연도','건물용도',
    #        '신고구분','평','평(범주형)','연월']
    select_col=st.multiselect('관심있는 키워드를 선택하세요',df.columns)
    #df.columns=k_columns
    
    
    
    
if __name__ == "__main__":
    main()
    
