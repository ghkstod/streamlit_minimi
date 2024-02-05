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
    gdf=load_geojsondata()
    # 대시보드 제목
    st.title('부동산 용도별 평균 거래가격 시각화 앱')   
    

    st.header("원하는 금액대 찾기")
    
    min_price, max_price = st.slider('가격 범위 선택:',
                                 int(df['OBJ_AMT'].min()), int(df['OBJ_AMT'].max()), 
                                 (int(df['OBJ_AMT'].min()), int(df['OBJ_AMT'].max())))

    # 선택된 가격 범위에 해당하는 데이터 필터링
    filtered_df = df[(df['OBJ_AMT'] >= min_price) & (df['OBJ_AMT'] <= max_price)]

    # 필터링된 데이터와 GeoDataFrame 병합
    merged_gdf = gdf.merge(filtered_df, left_on='SIG_KOR_NM', right_on='SGG_NM', how='inner')

    # Plotly를 사용하여 지도 시각화
    fig = px.choropleth_mapbox(merged_gdf,
                            geojson=merged_gdf.geometry.__geo_interface__,
                            locations=merged_gdf.index,
                            color='OBJ_AMT',
                            color_continuous_scale="Viridis",
                            mapbox_style="carto-positron",
                            zoom=10,
                            center={"lat": 37.5650172, "lon": 126.9782914})

    # Streamlit에 지도 표시
    st.plotly_chart(fig)
    
if __name__ == "__main__":
    main()