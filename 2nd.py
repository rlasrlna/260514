import streamlit as st
import pandas as pd
import plotly.express as px
from pandas.api.types import CategoricalDtype

st.set_page_config(page_title="MBTI 세계지도", layout="wide")
st.title("🌍 국가별 MBTI 유형 분포 지도")

# 1. CSV 파일 불러오기

file_path = "countriesMBTI_16types.csv"
df = pd.read_csv(file_path)

# 2. MBTI 16개 유형 정의

mbti_types = [
"INTJ", "INTP", "ENTJ", "ENTP",
"INFJ", "INFP", "ENFJ", "ENFP",
"ISTJ", "ISFJ", "ESTJ", "ESFJ",
"ISTP", "ISFP", "ESTP", "ESFP"
]

# 3. 국가별 Top1 MBTI 추출

df["Top1"] = df[mbti_types].idxmax(axis=1)

# 4. Top1 유형별 국가 수 계산

top1_counts = df["Top1"].value_counts()
top1_counts_df = top1_counts.reset_index()
top1_counts_df.columns = ['MBTI', 'Countries_with_Top1']

# 5. "INFP (109개국)" 형식의 범례 라벨 생성

top1_label_map = {
row["MBTI"]: f"{row['MBTI']} ({row['Countries_with_Top1']}개국)"
for _, row in top1_counts_df.iterrows()
}
df["Top1_label"] = df["Top1"].map(top1_label_map)

# 6. 범례 순서를 국가 수 많은 순으로 지정

ordered_labels = [top1_label_map[mbti] for mbti in top1_counts.index]
df["Top1_label"] = df["Top1_label"].astype(CategoricalDtype(categories=ordered_labels, ordered=True))

# 7. 색상 지정 (16개 MBTI)

mbti_colors = {
"INTJ": "#1f77b4", "INTP": "#ff7f0e", "ENTJ": "#2ca02c", "ENTP": "#d62728",
"INFJ": "#9467bd", "INFP": "#8c564b", "ENFJ": "#e377c2", "ENFP": "#7f7f7f",
"ISTJ": "#bcbd22", "ISFJ": "#17becf", "ESTJ": "#aec7e8", "ESFJ": "#ffbb78",
"ISTP": "#98df8a", "ISFP": "#ff9896", "ESTP": "#c5b0d5", "ESFP": "#c49c94"
}

# 8. 범례 라벨에 맞춘 색상 매핑

color_map = {
top1_label_map[mbti]: mbti_colors[mbti]
for mbti in top1_counts.index
}

# 9. Hover 텍스트 생성 (소수점 2자리)

def make_hover_text(row):
top3 = row[mbti_types].sort_values(ascending=False).head(3)
lines = [f"{i+1}️⃣ {mbti}: {pct:.2f}%" for i, (mbti, pct) in enumerate(top3.items())]
return f"<b>{row['Country']}</b><br>" + "<br>".join(lines)

df["hover_text"] = df.apply(make_hover_text, axis=1)

# 10. Plotly 지도 시각화

fig = px.choropleth(
df,
locations="Country",
locationmode="country names",
color="Top1_label",
hover_name="Country",
hover_data={"hover_text": True, "Country": False},
color_discrete_map=color_map,
title="🗺️ 국가별 최다 MBTI 유형 (Top1 기준)"
)

fig.update_traces(
hovertemplate="%{customdata[0]}<extra>%{location}</extra>"
)

fig.update_layout(
legend_title_text="Top1 MBTI 유형 (국가 수 기준)",
geo=dict(showframe=False, showcoastlines=False),
margin={"r":0,"t":50,"l":0,"b":0}
)

# 11. 지도 출력

st.plotly_chart(fig, use_container_width=True)
