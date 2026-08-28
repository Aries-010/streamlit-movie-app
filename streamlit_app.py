import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="원작 기반 영상화 검색",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        background-color: #fafafa;
    }

    .header {
        background: transparent;
        border-bottom: none;
        padding: 5px 0;
        margin-bottom: 15px;
        box-shadow: none;
    }

    .logo {
        text-align: center;
        font-size: 36px;
        font-weight: 700;
        color: #00c73c;
        margin-bottom: 12px;
    }

    .search-container {
        text-align: center;
        margin-bottom: 20px;
    }

    .card {
        background: white;
        border-radius: 8px;
        padding: 14px;
        border: 1px solid #e5e5e5;
        transition: box-shadow 0.2s;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 10px;
    }

    .card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }

    .card-rank {
        display: inline-block;
        background: #00c73c;
        color: white;
        padding: 3px 8px;
        border-radius: 3px;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .card-rank-worst {
        background: #ff6b6b;
    }

    .card-title {
        font-size: 14px;
        font-weight: 700;
        color: #000;
        margin-bottom: 6px;
        line-height: 1.3;
    }

    .card-meta {
        font-size: 11px;
        color: #666;
        margin-bottom: 8px;
        line-height: 1.4;
    }

    .card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 8px;
        border-top: 1px solid #e5e5e5;
    }

    .score-value {
        font-size: 16px;
        font-weight: 700;
        color: #00c73c;
    }

    .score-value-worst {
        color: #ff6b6b;
    }

    .section-title {
        font-size: 16px;
        font-weight: 700;
        color: #333;
        margin-bottom: 12px;
    }

    .list-item {
        background: white;
        display: flex;
        align-items: center;
        padding: 10px;
        border-bottom: 1px solid #e5e5e5;
        border-radius: 4px;
        margin-bottom: 6px;
    }

    .list-rank {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        background: #f0f0f0;
        border-radius: 50%;
        font-weight: 700;
        color: #333;
        margin-right: 10px;
        font-size: 11px;
    }

    .list-info {
        flex: 1;
    }

    .list-title {
        font-size: 13px;
        font-weight: 700;
        color: #000;
        margin-bottom: 3px;
    }

    .list-meta {
        font-size: 11px;
        color: #999;
    }

    .list-score {
        font-size: 14px;
        font-weight: 700;
        color: #00c73c;
        margin-left: 12px;
        text-align: right;
        min-width: 50px;
    }

    .divider {
        height: 1px;
        background: #e5e5e5;
        margin: 20px 0;
    }

    .rank-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 영화 데이터
movies_data = [
    {"title": "쇼생크 탈출", "year": 1994, "director": "Frank Darabont", "genre": ["드라마"], "critic": 82, "audience": 95},
    {"title": "포레스트 검프", "year": 1994, "director": "Robert Zemeckis", "genre": ["드라마", "로맨스"], "critic": 71, "audience": 87},
    {"title": "쥐라기 공원", "year": 1993, "director": "Steven Spielberg", "genre": ["SF", "모험"], "critic": 91, "audience": 88},
    {"title": "배트맨 리턴즈", "year": 1992, "director": "Tim Burton", "genre": ["슈퍼히어로", "액션"], "critic": 80, "audience": 77},
    {"title": "타이타닉", "year": 1997, "director": "James Cameron", "genre": ["로맨스", "드라마"], "critic": 89, "audience": 91},
    {"title": "The Green Mile", "year": 1999, "director": "Frank Darabont", "genre": ["드라마"], "critic": 79, "audience": 86},
    {"title": "The Mummy", "year": 1999, "director": "Stephen Sommers", "genre": ["모험", "액션"], "critic": 61, "audience": 81},
    {"title": "해리포터1", "year": 2001, "director": "Chris Columbus", "genre": ["판타지", "드라마"], "critic": 81, "audience": 83},
    {"title": "반지의제왕1", "year": 2001, "director": "Peter Jackson", "genre": ["판타지", "모험"], "critic": 91, "audience": 95},
    {"title": "라라크로프트", "year": 2001, "director": "Simon West", "genre": ["액션", "모험"], "critic": 20, "audience": 56},
    {"title": "반지의제왕2", "year": 2002, "director": "Peter Jackson", "genre": ["판타지", "모험"], "critic": 88, "audience": 95},
    {"title": "해리포터2", "year": 2002, "director": "Chris Columbus", "genre": ["판타지", "드라마"], "critic": 82, "audience": 82},
    {"title": "스파이더맨", "year": 2002, "director": "Sam Raimi", "genre": ["슈퍼히어로", "액션"], "critic": 80, "audience": 84},
    {"title": "X-Men", "year": 2000, "director": "Bryan Singer", "genre": ["슈퍼히어로", "액션"], "critic": 82, "audience": 81},
    {"title": "반지의제왕3", "year": 2003, "director": "Peter Jackson", "genre": ["판타지", "모험"], "critic": 93, "audience": 95},
    {"title": "해리포터3", "year": 2004, "director": "Alfonso Cuarón", "genre": ["판타지", "드라마"], "critic": 90, "audience": 86},
    {"title": "X2", "year": 2003, "director": "Bryan Singer", "genre": ["슈퍼히어로", "액션"], "critic": 85, "audience": 87},
    {"title": "배트맨 비긴즈", "year": 2005, "director": "Christopher Nolan", "genre": ["슈퍼히어로", "액션"], "critic": 84, "audience": 88},
    {"title": "수퍼맨 리턴즈", "year": 2006, "director": "Bryan Singer", "genre": ["슈퍼히어로", "액션"], "critic": 76, "audience": 72},
    {"title": "다빈치 코드", "year": 2006, "director": "Ron Howard", "genre": ["드라마", "미스터리"], "critic": 25, "audience": 77},
    {"title": "미녀는 괴로워", "year": 2006, "director": "김윤석", "genre": ["드라마", "로맨스"], "critic": 79, "audience": 80},
    {"title": "아이언맨", "year": 2008, "director": "Jon Favreau", "genre": ["슈퍼히어로", "액션"], "critic": 79, "audience": 79},
    {"title": "다크나이트", "year": 2008, "director": "Christopher Nolan", "genre": ["슈퍼히어로", "범죄"], "critic": 94, "audience": 90},
    {"title": "헐크", "year": 2008, "director": "Louis Leterrier", "genre": ["슈퍼히어로", "액션"], "critic": 67, "audience": 71},
    {"title": "Star Trek", "year": 2009, "director": "J.J. Abrams", "genre": ["SF", "액션"], "critic": 82, "audience": 83},
    {"title": "해리포터6", "year": 2009, "director": "David Yates", "genre": ["판타지", "드라마"], "critic": 78, "audience": 84},
    {"title": "드래곤볼", "year": 2009, "director": "James Wong", "genre": ["액션", "판타지"], "critic": 12, "audience": 19},
    {"title": "해리포터7", "year": 2011, "director": "David Yates", "genre": ["판타지", "드라마"], "critic": 84, "audience": 90},
    {"title": "토르", "year": 2011, "director": "Kenneth Branagh", "genre": ["슈퍼히어로", "판타지"], "critic": 77, "audience": 78},
    {"title": "캡틴아메리카1", "year": 2011, "director": "Joe Johnston", "genre": ["슈퍼히어로", "액션"], "critic": 80, "audience": 81},
    {"title": "어벤져스", "year": 2012, "director": "Joss Whedon", "genre": ["슈퍼히어로", "액션"], "critic": 92, "audience": 91},
    {"title": "스파이더맨2012", "year": 2012, "director": "Marc Webb", "genre": ["슈퍼히어로", "액션"], "critic": 66, "audience": 72},
    {"title": "호빗1", "year": 2012, "director": "Peter Jackson", "genre": ["판타지", "모험"], "critic": 58, "audience": 74},
    {"title": "헝거게임", "year": 2012, "director": "Gary Ross", "genre": ["SF", "액션"], "critic": 84, "audience": 84},
    {"title": "신과함께", "year": 2017, "director": "김용화", "genre": ["드라마", "판타지"], "critic": 81, "audience": 85},
    {"title": "아이언맨3", "year": 2013, "director": "Shane Black", "genre": ["슈퍼히어로", "액션"], "critic": 79, "audience": 79},
    {"title": "울버린", "year": 2013, "director": "James Mangold", "genre": ["슈퍼히어로", "액션"], "critic": 71, "audience": 75},
    {"title": "맨오브스틸", "year": 2013, "director": "Zack Snyder", "genre": ["슈퍼히어로", "액션"], "critic": 56, "audience": 77},
    {"title": "헝거게임2", "year": 2013, "director": "Francis Lawrence", "genre": ["SF", "액션"], "critic": 83, "audience": 84},
    {"title": "호빗2", "year": 2013, "director": "Peter Jackson", "genre": ["판타지", "모험"], "critic": 59, "audience": 74},
    {"title": "패션왕", "year": 2014, "director": "이성규", "genre": ["드라마"], "critic": 18, "audience": 22},
    {"title": "캡틴아메리카2", "year": 2014, "director": "Russo", "genre": ["슈퍼히어로", "액션"], "critic": 89, "audience": 91},
    {"title": "메이즈러너", "year": 2014, "director": "Wes Ball", "genre": ["SF", "액션"], "critic": 66, "audience": 78},
    {"title": "다이버전트", "year": 2014, "director": "Neil Burger", "genre": ["SF", "액션"], "critic": 41, "audience": 80},
    {"title": "가디언즈", "year": 2014, "director": "James Gunn", "genre": ["슈퍼히어로", "코미디"], "critic": 92, "audience": 92},
    {"title": "어벤져스2", "year": 2015, "director": "Joss Whedon", "genre": ["슈퍼히어로", "액션"], "critic": 66, "audience": 83},
    {"title": "앤트맨", "year": 2015, "director": "Peyton Reed", "genre": ["슈퍼히어로", "코미디"], "critic": 80, "audience": 83},
    {"title": "캡틴아메리카3", "year": 2016, "director": "Russo", "genre": ["슈퍼히어로", "액션"], "critic": 91, "audience": 89},
    {"title": "배트맨VS슈퍼맨", "year": 2016, "director": "Zack Snyder", "genre": ["슈퍼히어로", "액션"], "critic": 27, "audience": 63},
    {"title": "닥터스트레인지", "year": 2016, "director": "Scott Derrickson", "genre": ["슈퍼히어로", "판타지"], "critic": 89, "audience": 87},
    {"title": "신데렐라", "year": 2015, "director": "Kenneth Branagh", "genre": ["판타지", "로맨스"], "critic": 85, "audience": 85},
    {"title": "수어사이드스쿼드", "year": 2016, "director": "David Ayer", "genre": ["슈퍼히어로", "액션"], "critic": 26, "audience": 60},
    {"title": "원더우먼", "year": 2017, "director": "Patty Jenkins", "genre": ["슈퍼히어로", "액션"], "critic": 92, "audience": 80},
    {"title": "토르라그나로크", "year": 2017, "director": "Taika Waititi", "genre": ["슈퍼히어로", "코미디"], "critic": 93, "audience": 89},
    {"title": "스파이더맨홈커밍", "year": 2017, "director": "Jon Watts", "genre": ["슈퍼히어로", "액션"], "critic": 92, "audience": 87},
    {"title": "블랙팬서", "year": 2018, "director": "Ryan Coogler", "genre": ["슈퍼히어로", "액션"], "critic": 96, "audience": 86},
    {"title": "아쿠아맨", "year": 2018, "director": "James Wan", "genre": ["슈퍼히어로", "모험"], "critic": 65, "audience": 86},
    {"title": "어벤져스인피니티", "year": 2018, "director": "Russo", "genre": ["슈퍼히어로", "액션"], "critic": 84, "audience": 91},
    {"title": "이태원클라쓰", "year": 2020, "director": "이창동", "genre": ["드라마", "액션"], "critic": 82, "audience": 84},
    {"title": "어벤져스엔드게임", "year": 2019, "director": "Russo", "genre": ["슈퍼히어로", "액션"], "critic": 84, "audience": 90},
    {"title": "조커", "year": 2019, "director": "Todd Phillips", "genre": ["범죄", "드라마"], "critic": 68, "audience": 89},
    {"title": "무빙", "year": 2023, "director": "이준혁", "genre": ["드라마", "액션"], "critic": 88, "audience": 89},
    {"title": "DP", "year": 2021, "director": "이준혁", "genre": ["드라마", "액션"], "critic": 86, "audience": 82},
    {"title": "스파이더맨파프롬홈", "year": 2019, "director": "Jon Watts", "genre": ["슈퍼히어로", "액션"], "critic": 90, "audience": 91},
    {"title": "스파이더맨노웨이홈", "year": 2021, "director": "Jon Watts", "genre": ["슈퍼히어로", "액션"], "critic": 90, "audience": 93},
    {"title": "블랙팬서와칸다", "year": 2022, "director": "Ryan Coogler", "genre": ["슈퍼히어로", "액션"], "critic": 84, "audience": 88},
    {"title": "닥터스트레인지멀티버스", "year": 2022, "director": "Sam Raimi", "genre": ["슈퍼히어로", "공포"], "critic": 88, "audience": 85},
    {"title": "더배트맨", "year": 2022, "director": "Matt Reeves", "genre": ["슈퍼히어로", "범죄"], "critic": 84, "audience": 77},
    {"title": "더라스트오브어스", "year": 2023, "director": "Craig Mazin", "genre": ["드라마", "액션"], "critic": 95, "audience": 92},
    {"title": "토르사랑과천둥", "year": 2022, "director": "Taika Waititi", "genre": ["슈퍼히어로", "코미디"], "critic": 63, "audience": 68},
    {"title": "가디언즈3", "year": 2023, "director": "James Gunn", "genre": ["슈퍼히어로", "코미디"], "critic": 84, "audience": 90},
    {"title": "인어공주", "year": 2023, "director": "Rob Marshall", "genre": ["판타지", "로맨스"], "critic": 53, "audience": 69},
    {"title": "플래시", "year": 2023, "director": "Andy Muschietti", "genre": ["슈퍼히어로", "액션"], "critic": 55, "audience": 61},
    {"title": "원피스", "year": 2023, "director": "Marc Jobst", "genre": ["모험", "드라마"], "critic": 82, "audience": 85},
    {"title": "폴아웃", "year": 2024, "director": "Jonathan Nolte", "genre": ["드라마", "SF"], "critic": 94, "audience": 88}
]

df = pd.DataFrame(movies_data)
df['avg_score'] = (df['critic'] + df['audience']) / 2

# 헤더
st.markdown('<div class="header">', unsafe_allow_html=True)
st.markdown('<div class="logo">🎬 영상화 검색</div>', unsafe_allow_html=True)

# 검색
search_query = st.text_input("", placeholder="영화 제목, 감독명 검색", label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)

# 필터 - Expander
col1, col2 = st.columns(2)

with col1:
    with st.expander("📅 연도별 필터", expanded=False):
        selected_years = st.multiselect(
            "연도 선택",
            sorted(df['year'].unique()),
            default=sorted(df['year'].unique()),
            label_visibility="collapsed"
        )

with col2:
    with st.expander("🎭 장르별 필터", expanded=False):
        all_genres = sorted(list(set(g for genres_list in df['genre'] for g in genres_list)))
        selected_genres = st.multiselect(
            "장르 선택",
            all_genres,
            default=all_genres,
            label_visibility="collapsed"
        )

# 필터 적용
filtered_df = df.copy()

if search_query:
    filtered_df = filtered_df[
        (filtered_df['title'].str.contains(search_query, case=False, na=False)) |
        (filtered_df['director'].str.contains(search_query, case=False, na=False))
    ]

filtered_df = filtered_df[filtered_df['year'].isin(selected_years)]
filtered_df = filtered_df[filtered_df['genre'].apply(lambda x: any(g in selected_genres for g in x))]

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 인기순위 / 낮은순위
col_best, col_worst = st.columns(2)

# TOP 순위
with col_best:
    with st.expander("🏆 인기순위", expanded=True):
        top_10 = filtered_df.nlargest(10, 'avg_score').reset_index(drop=True)

        for idx, (i, movie) in enumerate(top_10.iterrows(), 1):
            st.markdown(f"""
                <div class="card">
                    <div class="card-rank">TOP {idx}</div>
                    <div class="card-title">{movie['title']}</div>
                    <div class="card-meta">
                        {movie['director']}<br>
                        {movie['year']} · {', '.join(movie['genre'][:1])}
                    </div>
                    <div class="card-footer">
                        <div style="font-size: 10px; color: #999;">
                            {movie['critic']}% / {movie['audience']}%
                        </div>
                        <div class="score-value">{movie['avg_score']:.1f}%</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# WORST 순위
with col_worst:
    with st.expander("📉 낮은순위", expanded=True):
        worst_10 = filtered_df.nsmallest(10, 'avg_score').reset_index(drop=True)

        for idx, (i, movie) in enumerate(worst_10.iterrows(), 1):
            st.markdown(f"""
                <div class="card">
                    <div class="card-rank card-rank-worst">LOW {idx}</div>
                    <div class="card-title">{movie['title']}</div>
                    <div class="card-meta">
                        {movie['director']}<br>
                        {movie['year']} · {', '.join(movie['genre'][:1])}
                    </div>
                    <div class="card-footer">
                        <div style="font-size: 10px; color: #999;">
                            {movie['critic']}% / {movie['audience']}%
                        </div>
                        <div class="score-value score-value-worst">{movie['avg_score']:.1f}%</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 전체 목록
st.markdown(f'<div class="section-title">📽️ 전체 목록 ({len(filtered_df)}개)</div>', unsafe_allow_html=True)

sorted_df = filtered_df.sort_values('avg_score', ascending=False).reset_index(drop=True)

for idx, (i, movie) in enumerate(sorted_df.iterrows(), 1):
    st.markdown(f"""
        <div class="list-item">
            <div class="list-rank">{idx}</div>
            <div class="list-info">
                <div class="list-title">{movie['title']}</div>
                <div class="list-meta">{movie['director']} · {movie['year']}</div>
            </div>
            <div class="list-score">{movie['avg_score']:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)
