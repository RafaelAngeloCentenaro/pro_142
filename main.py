from flask import Flask,jsonify,request
import pandas as pd
from demographic_filtering import output
moviedata=pd.read_csv("movies.csv")
app=Flask(__name__)

all_movies=moviedata[["original_title","release_date","runtime","weighted_rating"]]
liked_movies=[]
not_liked_movies=[]
did_not_watch=[]
@app.route("/")
def assign_val():
    m_data={
        "original_title":all_movies.iloc[0,0],
        "release_date":all_movies.iloc[0,2] or "n/a",
        "duration":all_movies.iloc[0,3],
        "rating":all_movies.iloc[0,4]/2
    }
@app.route("/movies")
def get_movie():
    moviedata=assign_val()
    return jsonify({
        "data":moviedata,
        "status":"success"
    })
@app.route("/like")
def liked_movie():
    global all_movies
    moviedata=assign_val()
    liked_movies.append(moviedata)
    all_movies.drop([0],inplace=True)
    all_movies=all_movies.reset_index(drop=True)
    return jsonify({
        "status":"success"
    })
@app.route("/dislike")
def unlike_movie():
    global all_movies
    moviedata=assign_val()
    not_liked_movies.append(moviedata)
    all_movies.drop([0],inplace=True)
    all_movies=all_movies.reset_index(drop=True)
    return jsonify({
        "status":"success"
    })
@app.route("/did_not_watch")
def did_not_watch_view():
    global all_movies
    moviedata=assign_val()
    did_not_watch.append(moviedata)
    all_movies.drop([0],inplace=True)
    all_movies=all_movies.reset_index(drop=True)
    return jsonify({
        "status":"success"
    })
@app.route("/liked",methods=["GET"])
def liked():
    global liked_movies
    return jsonify({
        "data":liked_movies,
        "status":"success"
    })
@app.route("/popular_movies")
def popular_movies():
    popular_movies_data=[]
    for index,row in output.iterrows():
        _p={
            "original_title":row["original_title"],
            "release_date":row["release_date"] or "n/a",
            "duration":row["runtime"],
            "rating":row["weighted_rating"]/2
        }
        popular_movies_data.append(_p)
        return jsonify({
            "data":popular_movies_data,
            "status":"success"
        })
@app.route("/recomended_movies")
def recomended_movies():
    global liked_movies
    col_names=["original_title","release_date","runtime","weighted_rating"]
    all_recomended=pd.DataFrame(columns=col_names)
    for liked_movie in liked_movies:
        output=liked_movie["original_title"]
        all_recomended=all_recomended.append(output)
    all_recomended.drop_duplicates(subset=["original_title"],inplace=True)
    recomended_movie_data=[]
    for index,row in all_recomended.iterrows():
        _p={
            "original_title":row["original_title"],
            "release_date":row["release_date"] or "n/a",
            "duration":row["runtime"],
            "rating":row["weighted_rating"]/2
        }
        recomended_movie_data.append(_p)
        return jsonify({
            "data":recomended_movie_data,
            "status":"success"
        })
if __name__=="__main__":
    app.run()