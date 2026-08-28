import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="원작 기반 영상화 검색 플랫폼",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 3em;
        color: #667eea;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        color: #999;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    .toggle-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        color: white;
    }
    .toggle-title {
        font-size: 1.5em;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .best-worst-section {
        display: flex;
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    .best-card, .worst-card {
        flex: 1;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
    }
    .best-card {
        background: linear-gradient(135deg, #81C784 0%, #4CAF50 100%);
        color: white;
    }
    .worst-card {
        background: linear-gradient(135deg, #FF7043 0%, #E64A19 100%);
        color: white;
    }
    .card-title {
        font-size: 1.5em;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .movie-item {
        background: white;
        padding: 0.7rem;
        margin: 0.5rem 0;
        border-radius: 6px;
        color: #333;
        font-size: 0.95em;
    }
    .movie-rank {
        font-size: 1.2em;
        font-weight: bold;
        display: inline-block;
        width: 30px;
        text-align: center;
    }
    .movie-info {
        display: inline-block;
        margin-left: 0.8rem;
        vertical-align: middle;
    }
    .movie-title {
        font-weight: bold;
        font-size: 1em;
        margin-bottom: 0.2rem;
    }
    .movie-meta {
        font-size: 0.8em;
        color: #666;
    }
    .movie-score {
        float: right;
        font-weight: bold;
        font-size: 1em;
    }
    </style>
    """, unsafe_allow_html=True)

# 영화 데이터
movies_data = [
    {"title": "쇼생크 탈출", "year": 1994, "director": "Frank Darabont", "genre": ["드라마"], "critic": 82, "audience": 95, "origin": "Stephen King", "dist": "Columbia"},
    {"title": "포레스트 검프", "year": 1994, "director": "Robert Zemeckis", "genre": ["드라마", "로맨스"], "critic": 71, "audience": 87, "origin": "Winston Groom", "dist": "Paramount"},
    {"title": "쥐라기 공원", "year": 1993, "director": "Steven Spielberg", "genre": ["SF", "모험"], "critic": 91, "audience": 88, "origin": "Michael Crichton", "dist": "Universal"},
    {"title": "배트맨 리턴즈", "year": 1992, "director": "Tim Burton", "genre": ["슈퍼히어로", "액션"], "critic": 80, "audience": 77, "origin": "DC", "dist": "Warner Bros"},
    {"title": "타이타닉", "year": 1997, "director": "James Cameron", "genre": ["로맨스", "드라마"], "critic": 89, "audience": 91, "origin": "역사", "dist": "Paramount"},
    {"title": "The Green Mile", "year": 1999, "director": "Frank Darabont", "genre": ["드라마"], "critic": 79, "audience": 86, "origin": "Stephen King", "dist": "Warner Bros"},
    {"title": "The Mummy", "year": 1999, "director": "Stephen Sommers", "genre": ["모험", "액션"], "critic": 61, "audience": 81, "origin": "순창작", "dist": "Universal"},
    {"title": "해리포터1", "year": 2001, "director": "Chris Columbus", "genre": ["판타지", "드라마"], "critic": 81, "audience": 83, "origin": "J.K. Rowling", "dist": "Warner Bros"},
    {"title": "반지의제왕1", "year": 2001, "director": "Peter Jackson", "genre": ["판타지", "모험"], "critic": 91, "audience": 95, "origin": "J.R.R. Tolkien", "dist": "New Line"},
    {"title": "라라크로프트", "year": 2001, "director": "Simon West", "genre": ["액션", "모험"], "critic": 20, "audience": 56, "origin": "게임", "dist": "Paramount"},
    {"title": "반지의제왕2", "year": 2002, "director": "Peter Jackson", "genre": ["판타지", "모험"], "critic": 88, "audience": 95, "origin": "J.R.R. Tolkien", "dist": "New Line"},
    {"title": "해리포터2", "year": 2002, "director": "Chris Columbus", "genre": ["판타지", "드라마"], "critic": 82, "audience": 82, "origin": "J.K. Rowling", "dist": "Warner Bros"},
    {"title": "스파이더맨", "year": 2002, "director": "Sam Raimi", "genre": ["슈퍼히어로", "액션"], "critic": 80, "audience": 84, "origin": "마블", "dist": "Sony"},
    {"title": "X-Men", "year": 2000, "director": "Bryan Singer", "genre": ["슈퍼히어로", "액션"], "critic": 82, "audience": 81, "origin": "마블", "dist": "Fox"},
    {"title": "반지의제왕3", "year": 2003, "director": "Peter Jackson", "genre": ["판타지", "모험"], "critic": 93, "audience": 95, "origin": "J.R.R. Tolkien", "dist": "New Line"},
    {"title": "해리포터3", "year": 2004, "director": "Alfonso Cuarón", "genre": ["판타지", "드라마"], "critic": 90, "audience": 86, "origin": "J.K. Rowling", "dist": "Warner Bros"},
    {"title": "X2", "year": 2003, "director": "Bryan Singer", "genre": ["슈퍼히어로", "액션"], "critic": 85, "audience": 87, "origin": "마블", "dist": "Fox"},
    {"title": "배트맨 비긴즈", "year": 2005, "director": "Christopher Nolan", "genre": ["슈퍼히어로", "액션"], "critic": 84, "audience": 88, "origin": "DC", "dist": "Warner Bros"},
    {"title": "수퍼맨 리턴즈", "year": 2006, "director": "Bryan Singer", "genre": ["슈퍼히어로", "액션"], "critic": 76, "audience": 72, "origin": "DC", "dist": "Warner Bros"},
    {"title": "다빈치 코드", "year": 2006, "director": "Ron Howard", "genre": ["드라마", "미스터리"], "critic": 25, "audience": 77, "origin": "Dan Brown", "dist": "Sony"},
    {"title": "미녀는 괴로워", "year": 2006, "director": "김윤석", "genre": ["드라마", "로맨스"], "critic": 79, "audience": 80, "origin": "만화", "dist": "CJ"},
    {"title": "아이언맨", "year": 2008, "director": "Jon Favreau", "genre": ["슈퍼히어로", "액션"], "critic": 79, "audience": 79, "origin": "마블", "dist": "Disney"},
    {"title": "다크나이트", "year": 2008, "director": "Christopher Nolan", "genre": ["슈퍼히어로", "범죄"], "critic": 94, "audience": 90, "origin": "DC", "dist": "Warner Bros"},
    {"title": "헐크", "year": 2008, "director": "Louis Leterrier", "genre": ["슈퍼히어로", "액션"], "critic": 67, "audience": 71, "origin": "마블", "dist": "Universal"},
    {"title": "Star Trek", "year": 2009, "director": "J.J. Abrams", "genre": ["SF", "액션"], "critic": 82, "audience": 83, "origin": "TV", "dist": "Paramount"},
    {"title": "해리포터6", "year": 2009, "director": "David Yates", "genre": ["판타지", "드라마"], "critic": 78, "audience": 84, "origin": "J.K. Rowling", "dist": "Warner Bros"},
    {"title": "드래곤볼", "year": 2009, "director": "James Wong", "genre": ["액션", "판타지"], "critic": 12, "audience": 19, "origin": "만화", "dist": "Fox"},
    {"title": "해리포터7", "year": 2011, "director": "David Yates", "genre": ["판타지", "드라마"], "critic": 84, "audience": 90, "origin": "J.K. Rowling", "dist": "Warner Bros"},
    {"title": "토르", "year": 2011, "director": "Kenneth Branagh", "genre": ["슈퍼히어로", "판타지"], "critic": 77, "audience": 78, "origin": "마블", "dist": "Disney"},
    {"title": "캡틴아메리카1", "year": 2011, "director": "Joe Johnston", "genre": ["슈퍼히어로", "액션"], "critic": 80, "audience": 81, "origin": "마블", "dist": "Disney"},
    {"title": "어벤져스", "year": 2012, "director": "Joss Whedon", "genre": ["슈퍼히어로", "액션"], "critic": 92, "audience": 91, "origin": "마블", "dist": "Disney"},
    {"title": "스파이더맨2012", "year": 2012, "director": "Marc Webb", "genre": ["슈퍼히어로", "액션"], "critic": 66, "audience": 72, "origin": "마블", "dist": "Sony"},
    {"title": "호빗1", "year": 2012, "director": "Peter Jackson", "genre": ["판타지", "모험"], "critic": 58, "audience": 74, "origin": "Tolkien", "dist": "New Line"},
    {"title": "헝거게임", "year": 2012, "director": "Gary Ross", "genre": ["SF", "액션"], "critic": 84, "audience": 84, "origin": "소설", "dist": "Lionsgate"},
    {"title": "신과함께", "year": 2017, "director": "김용화", "genre": ["드라마", "판타지"], "critic": 81, "audience": 85, "origin": "웹툰", "dist": "CJ"},
    {"title": "아이언맨3", "year": 2013, "director": "Shane Black", "genre": ["슈퍼히어로", "액션"], "critic": 79, "audience": 79, "origin": "마블", "dist": "Disney"},
    {"title": "울버린", "year": 2013, "director": "James Mangold", "genre": ["슈퍼히어로", "액션"], "critic": 71, "audience": 75, "origin": "마블", "dist": "Fox"},
    {"title": "맨오브스틸", "year": 2013, "director": "Zack Snyder", "genre": ["슈퍼히어로", "액션"], "critic": 56, "audience": 77, "origin": "DC", "dist": "Warner Bros"},
    {"title": "헝거게임2", "year": 2013, "director": "Francis Lawrence", "genre": ["SF", "액션"], "critic": 83, "audience": 84, "origin": "소설", "dist": "Lionsgate"},
    {"title": "호빗2", "year": 2013, "director": "Peter Jackson", "genre": ["판타지", "모험"], "critic": 59, "audience": 74, "origin": "Tolkien", "dist": "New Line"},
    {"title": "패션왕", "year": 2014, "director": "이성규", "genre": ["드라마"], "critic": 18, "audience": 22, "origin": "웹툰", "dist": "Daum"},
    {"title": "캡틴아메리카2", "year": 2014, "director": "Russo", "genre": ["슈퍼히어로", "액션"], "critic": 89, "audience": 91, "origin": "마블", "dist": "Disney"},
    {"title": "메이즈러너", "year": 2014, "director": "Wes Ball", "genre": ["SF", "액션"], "critic": 66, "audience": 78, "origin": "소설", "dist": "Fox"},
    {"title": "다이버전트", "year": 2014, "director": "Neil Burger", "genre": ["SF", "액션"], "critic": 41, "audience": 80, "origin": "소설", "dist": "Summit"},
    {"title": "가디언즈", "year": 2014, "director": "James Gunn", "genre": ["슈퍼히어로", "코미디"], "critic": 92, "audience": 92, "origin": "마블", "dist": "Disney"},
    {"title": "어벤져스2", "year": 2015, "director": "Joss Whedon", "genre": ["슈퍼히어로", "액션"], "critic": 66, "audience": 83, "origin": "마블", "dist": "Disney"},
    {"title": "앤트맨", "year": 2015, "director": "Peyton Reed", "genre": ["슈퍼히어로", "코미디"], "critic": 80, "audience": 83, "origin": "마블", "dist": "Disney"},
    {"title": "캡틴아메리카3", "year": 2016, "director": "Russo", "genre": ["슈퍼히어로", "액션"], "critic": 91, "audience": 89, "origin": "마블", "dist": "Disney"},
    {"title": "배트맨VS슈퍼맨", "year": 2016, "director": "Zack Snyder", "genre": ["슈퍼히어로", "액션"], "critic": 27, "audience": 63, "origin": "DC", "dist": "Warner Bros"},
    {"title": "닥터스트레인지", "year": 2016, "director": "Scott Derrickson", "genre": ["슈퍼히어로", "판타지"], "critic": 89, "audience": 87, "origin": "마블", "dist": "Disney"},
    {"title": "신데렐라", "year": 2015, "director": "Kenneth Branagh", "genre": ["판타지", "로맨스"], "critic": 85, "audience": 85, "origin": "동화", "dist": "Disney"},
    {"title": "수어사이드스쿼드", "year": 2016, "director": "David Ayer", "genre": ["슈퍼히어로", "액션"], "critic": 26, "audience": 60, "origin": "DC", "dist": "Warner Bros"},
    {"title": "원더우먼", "year": 2017, "director": "Patty Jenkins", "genre": ["슈퍼히어로", "액션"], "critic": 92, "audience": 80, "origin": "DC", "dist": "Warner Bros"},
    {"title": "토르라그나로크", "year": 2017, "director": "Taika Waititi", "genre": ["슈퍼히어로", "코미디"], "critic": 93, "audience": 89, "origin": "마블", "dist": "Disney"},
    {"title": "스파이더맨홈커밍", "year": 2017, "director": "Jon Watts", "genre": ["슈퍼히어로", "액션"], "critic": 92, "audience": 87, "origin": "마블", "dist": "Sony"},
    {"title": "블랙팬서", "year": 2018, "director": "Ryan Coogler", "genre": ["슈퍼히어로", "액션"], "critic": 96, "audience": 86, "origin": "마블", "dist": "Disney"},
    {"title": "아쿠아맨", "year": 2018, "director": "James Wan", "genre": ["슈퍼히어로", "모험"], "critic": 65, "audience": 86, "origin": "DC", "dist": "Warner Bros"},
    {"title": "어벤져스인피니티", "year": 2018, "director": "Russo", "genre": ["슈퍼히어로", "액션"], "critic": 84, "audience": 91, "origin": "마블", "dist": "Disney"},
    {"title": "이태원클라쓰", "year": 2020, "director": "이창동", "genre": ["드라마", "액션"], "critic": 82, "audience": 84, "origin": "웹툰", "dist": "JTBC"},
    {"title": "어벤져스엔드게임", "year": 2019, "director": "Russo", "genre": ["슈퍼히어로", "액션"], "critic": 84, "audience": 90, "origin": "마블", "dist": "Disney"},
    {"title": "조커", "year": 2019, "director": "Todd Phillips", "genre": ["범죄", "드라마"], "critic": 68, "audience": 89, "origin": "DC", "dist": "Warner Bros"},
    {"title": "무빙", "year": 2023, "director": "이준혁", "genre": ["드라마", "액션"], "critic": 88, "audience": 89, "origin": "웹툰", "dist": "Disney+"},
    {"title": "DP", "year": 2021, "director": "이준혁", "genre": ["드라마", "액션"], "critic": 86, "audience": 82, "origin": "웹툰", "dist": "Netflix"},
    {"title": "스파이더맨파프롬홈", "year": 2019, "director": "Jon Watts", "genre": ["슈퍼히어로", "액션"], "critic": 90, "audience": 91, "origin": "마블", "dist": "Sony"},
    {"title": "스파이더맨노웨이홈", "year": 2021, "director": "Jon Watts", "genre": ["슈퍼히어로", "액션"], "critic": 90, "audience": 93, "origin": "마블", "dist": "Sony"},
    {"title": "블랙팬서와칸다", "year": 2022, "director": "Ryan Coogler", "genre": ["슈퍼히어로", "액션"], "critic": 84, "audience": 88, "origin": "마블", "dist": "Disney"},
    {"title": "닥터스트레인지멀티버스", "year": 2022, "director": "Sam Raimi", "genre": ["슈퍼히어로", "공포"], "critic": 88, "audience": 85, "origin": "마블", "dist": "Disney"},
    {"title": "더배트맨", "year": 2022, "director": "Matt Reeves", "genre": ["슈퍼히어로", "범죄"], "critic": 84, "audience": 77, "origin": "DC", "dist": "Warner Bros"},
    {"title": "더라스트오브어스", "year": 2023, "director": "Craig Mazin", "genre": ["드라마", "액션"], "critic": 95, "audience": 92, "origin": "게임", "dist": "HBO"},
    {"title": "토르사랑과천둥", "year": 2022, "director": "Taika Waititi", "genre": ["슈퍼히어로", "코미디"], "critic": 63, "audience": 68, "origin": "마블", "dist": "Disney"},
    {"title": "가디언즈3", "year": 2023, "director": "James Gunn", "genre": ["슈퍼히어로", "코미디"], "critic": 84, "audience": 90, "origin": "마블", "dist": "Disney"},
    {"title": "인어공주", "year": 2023, "director": "Rob Marshall", "genre": ["판타지", "로맨스"], "critic": 53, "audience": 69, "origin": "동화", "dist": "Disney"},
    {"title": "플래시", "year": 2023, "director": "Andy Muschietti", "genre": ["슈퍼히어로", "액션"], "critic": 55, "audience": 61, "origin": "DC", "dist": "Warner Bros"},
    {"title": "원피스", "year": 2023, "director": "Marc Jobst", "genre": ["모험", "드라마"], "critic": 82, "audience": 85, "origin": "만화", "dist": "Netflix"},
    {"title": "폴아웃", "year": 2024, "director": "Jonathan Nolte", "genre": ["드라마", "SF"], "critic": 94, "audience": 88, "origin": "게임", "dist": "Prime"}
]

df = pd.DataFrame(movies_data)
df['avg_score'] = (df['critic'] + df['audience']) / 2

# 메인 화면
st.markdown("<div class='main-title'>🎬 영상화 작품</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>1990-2026년 75개 영화·드라마 | 감독, 평점, 추천</div>", unsafe_allow_html=True)

# 검색창
search_col, _ = st.columns([3, 1])
with search_col:
    search_query = st.text_input("", placeholder="🔍 영화 제목, 감독명 검색...", label_visibility="collapsed")

# 토글 섹션
st.markdown("<div class='toggle-section'>", unsafe_allow_html=True)
st.markdown("<div class='toggle-title'>📊 선택하여 탐색</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.write("**연도별**")
    selected_years = st.multiselect(
        "연도 선택",
        sorted(df['year'].unique()),
        default=sorted(df['year'].unique()),
        label_visibility="collapsed"
    )

with col2:
    st.write("**장르별**")
    all_genres = sorted(list(set(g for genres_list in df['genre'] for g in genres_list)))
    selected_genres = st.multiselect(
        "장르 선택",
        all_genres,
        default=all_genres,
        label_visibility="collapsed"
    )

st.markdown("</div>", unsafe_allow_html=True)

# 필터 적용
filtered_df = df.copy()

if search_query:
    filtered_df = filtered_df[
        (filtered_df['title'].str.contains(search_query, case=False, na=False)) |
        (filtered_df['director'].str.contains(search_query, case=False, na=False))
    ]

filtered_df = filtered_df[filtered_df['year'].isin(selected_years)]
filtered_df = filtered_df[filtered_df['genre'].apply(lambda x: any(g in selected_genres for g in x))]

# Best 3 & Worst 3 (장르 기반)
best_3 = filtered_df.nlargest(3, 'avg_score')
worst_3 = filtered_df.nsmallest(3, 'avg_score')

st.markdown("<div class='best-worst-section'>", unsafe_allow_html=True)

# Best 3
col_best, col_worst = st.columns(2)

with col_best:
    st.markdown("<div class='best-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>🏆 Best 3</div>", unsafe_allow_html=True)

    for idx, (i, movie) in enumerate(best_3.iterrows(), 1):
        st.markdown(f"""
        <div class='movie-item'>
            <span class='movie-rank'>#{idx}</span>
            <div class='movie-info'>
                <div class='movie-title'>{movie['title']}</div>
                <div class='movie-meta'>{movie['director']} · {movie['year']}</div>
            </div>
            <div class='movie-score'>⭐ {movie['avg_score']:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Worst 3
with col_worst:
    st.markdown("<div class='worst-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>📉 Worst 3</div>", unsafe_allow_html=True)

    for idx, (i, movie) in enumerate(worst_3.iterrows(), 1):
        st.markdown(f"""
        <div class='movie-item'>
            <span class='movie-rank'>#{idx}</span>
            <div class='movie-info'>
                <div class='movie-title'>{movie['title']}</div>
                <div class='movie-meta'>{movie['director']} · {movie['year']}</div>
            </div>
            <div class='movie-score'>⭐ {movie['avg_score']:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# 전체 목록
st.divider()
st.subheader(f"📋 전체 목록 ({len(filtered_df)}개)")

display_df = filtered_df[['title', 'year', 'director', 'critic', 'audience']].copy()
display_df['평균'] = filtered_df['avg_score'].round(1)
display_df.columns = ['제목', '연도', '감독', '평론가', '관객', '평균']
display_df = display_df.sort_values('평균', ascending=False)

st.dataframe(display_df, use_container_width=True, hide_index=True)

st.divider()
st.markdown("<div style='text-align: center; color: #999; font-size: 0.9rem;'>© 2024 원작 기반 영상화 검색 플랫폼</div>", unsafe_allow_html=True)
