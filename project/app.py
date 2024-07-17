import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

movie = Movie()
tmdb = TMDb()
tmdb.api_key = "YOUR_API_KEY"
tmdb.language = "ko-KR"

movies = pickle.load(open("data/movie.pickle", "rb"))
cos_sim = pickle.load(open("data/cos_sim.pickle", "rb"))

def get_recommendations(title) :
    # 제목을 통해 그 영화의 idx 얻기
    idx = movies[movies["title"] == title].index[0]

    # 코사인 유사도 매트릭스에서 (cos_sim) idx에 해당하는 데이터를 (idx, 유사도)형태로 출력 (자기 자신은 1), 이 때의 idx는 영화의 idx와 다름
    sim_scores = list(enumerate(cos_sim[idx]))

    # 코사인 유사도 기준으로 내림차순 정렬
    sim_scores = sorted(sim_scores, key = lambda x : x[1], reverse = True)

    # 자기 자신을 제외한 10개의 추천 영화를 슬라이싱
    sim_scores = sim_scores[1:11]

    # 추천 영화 목록 10개의 인덱스 정보 추출
    movie_indices = [i[0] for i in sim_scores]

    # 인덱스 정보를 통해 영화 제목 추출
    imgs = []
    tits = []
    for i in movie_indices :
        id = movies["id"].iloc[i]
        details = movie.details(id)

        image_path = details["poster_path"]
        if image_path :
            image_path = "https://image.tmdb.org/t/p/w500" + image_path
        else :
            image_path = "data/no_image.jpg"

        imgs.append(image_path)
        tits.append(details["title"])

    return imgs, tits

# --- body
st.set_page_config(layout = "wide")
st.header("Ashfilx")

movie_list = movies["title"].values
title = st.selectbox("Choose a movie you like👍", movie_list)
if st.button("Recommend") :
    with st.spinner("Please wait...") :
        imgs, tits = get_recommendations(title)

        idx = 0
        for i in range(0, 2) :
            cols = st.columns(5)
            for i in cols :
                i.image(imgs[idx])
                i.write(tits[idx])
                idx += 1