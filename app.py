from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import time

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def upload():
	return render_template('index.html')

@app.route('/team info',methods=['GET','POST'])
def teaminfo():
	return render_template('team info.html')

@app.route('/project',methods=['GET','POST'])
def project():
	return render_template('algo_used.html')


@app.route('/predict/',methods=['GET','POST'])
def predict():
        start_time1 = time.time()
        def createCharacteristicMatrix(filename):

            data_frame = pd.read_csv(filename, sep="::", usecols = [0, 1, 2], names = ['userID', 'movieID', 'rating'], engine = 'python')
            data_mat = np.array(data_frame.pivot(index = 'movieID', columns = 'userID', values = 'rating'))
            data_mat_rev = np.nan_to_num(data_mat)
            return data_mat_rev
        print("\n\n Reading the data into the characteristic matrix... \n\n")
        X = createCharacteristicMatrix('db/bolratings.dat')
        print(X)
        n_movies, n_users = X.shape[0], X.shape[1]
        end_time1 = time.time() - start_time1
        print ("\n\n Time taken to generate the characteristic matrix consisting of", X.shape[0], "movies (in rows) and", X.shape[1], "users (in columns) =", round(end_time1, 2), "seconds\n\n")
        print ("\n\n Defining the utility function ... \n\n")
        # define the utility function
        def maxrate(A):
                if len(A) > 0:
                    X_j = X[list(A)]
                    maxrate = float(np.sum(np.amax(X_j, axis = 0)))/float(n_users)
                else:
                    maxrate = 0
                return maxrate
        K = [1,2,4]
        print ("\n\n Running the 'Lazy Greedy' Submodular Maximization Algorithm ... \n\n")
        start_time4 = time.time()
        lazy_greedy_objective_value_list = []
        lazy_recommended_movies = []
        time_list_lazy = []

        for k in K:

                A_lazy_greedy = set([])
                inter_start_lazy = time.time()
                for i in range(k):
                    if i == 0:

                        marginal_values_list = [maxrate(A_lazy_greedy.union(set([e]))) - maxrate(A_lazy_greedy) for e in range(n_movies)]
                        e_opt = np.argmax(marginal_values_list)
                        A_lazy_greedy = A_lazy_greedy.union(set([e_opt]))
                        marginal_values_list_sorted = sorted(marginal_values_list)[::-1][1:]
                        movie_index_sorted = list(np.argsort(marginal_values_list))[::-1][1:]
                    else:
                        while (maxrate(A_lazy_greedy.union(set([movie_index_sorted[0]]))) - maxrate(A_lazy_greedy)) < marginal_values_list_sorted[1]:
                            marginal_values_list[movie_index_sorted[0]] = maxrate(A_lazy_greedy.union(set([movie_index_sorted[0]]))) - maxrate(A_lazy_greedy)

                            marginal_values_list_sorted = sorted(marginal_values_list)[::-1]

                            movie_index_sorted = list(np.argsort(marginal_values_list))[::-1]

                        A_lazy_greedy = A_lazy_greedy.union(set([movie_index_sorted[0]]))
                        marginal_values_list_sorted = sorted(marginal_values_list)[::-1][1:]
                        movie_index_sorted = list(np.argsort(marginal_values_list))[::-1][1:]

        inter_end_lazy = time.time() - inter_start_lazy
        lazy_recommended_movies=list(A_lazy_greedy)
        lazy_greedy_objective_value_list.append(maxrate(A_lazy_greedy))

        time_list_lazy.append(round(inter_end_lazy, 5))
        end_time4 = time.time() - start_time4
        print ("\n\n Time taken to implement the 'Lazy Greedy' Submodular Maximization Algorithm =", round(end_time4, 5), "seconds\n\n")
        end_time = time.time() - start_time1
        print ("\n\n Time taken by program to run =", round(end_time, 5), "seconds\n\n")
        print(lazy_recommended_movies)
        movies_list=[]
        with open("db/bolmovies.dat", "r") as scan:
            for line in scan:
                iin=line.index(":")
                if(int(line[0:iin]) in lazy_recommended_movies):
                    #lin=line.index("(")
                    movies_list.append(line[iin+2:-1])
        filename=[]
        for x in movies_list:
            t=[]
            t.append('assets/images/movies/' + x +'.jpg')
            t.append(x)
            filename.append(t)
        print(filename)
        return render_template('predict.html',content=filename)
if __name__ == '__main__':
    app.run(debug=True, port=8000)
