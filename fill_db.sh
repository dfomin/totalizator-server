curl -X POST http://0.0.0.0:8000/create_competition?name=cl2022

curl -X POST http://0.0.0.0:8000/create_user?name=dfomin
curl -X POST http://0.0.0.0:8000/create_user?name=gregzhadko
curl -X POST http://0.0.0.0:8000/create_user?name=sivykh
curl -X POST http://0.0.0.0:8000/create_user?name=tatarintsev
curl -X POST http://0.0.0.0:8000/create_user?name=colapis
curl -X POST http://0.0.0.0:8000/create_user?name=Novikov_N

curl -X POST http://0.0.0.0:8000/join?user_id=1&competition_id=1
curl -X POST http://0.0.0.0:8000/join?user_id=2&competition_id=1
curl -X POST http://0.0.0.0:8000/join?user_id=3&competition_id=1
curl -X POST http://0.0.0.0:8000/join?user_id=4&competition_id=1
curl -X POST http://0.0.0.0:8000/join?user_id=5&competition_id=1
curl -X POST http://0.0.0.0:8000/join?user_id=6&competition_id=1

curl -X POST http://0.0.0.0:8000/add_match?competition_id=1&name=mancity_atletico
curl -X POST http://0.0.0.0:8000/add_match?competition_id=1&name=benfica_liverpool
curl -X POST http://0.0.0.0:8000/add_match?competition_id=1&name=chelsea_real
curl -X POST http://0.0.0.0:8000/add_match?competition_id=1&name=villarreal_bayern

curl -X POST http://0.0.0.0:8000/vote?user_id=1&match_id=1&score1=2&score2=0
curl -X POST http://0.0.0.0:8000/vote?user_id=1&match_id=2&score1=0&score2=0
curl -X POST http://0.0.0.0:8000/vote?user_id=2&match_id=1&score1=1&score2=0
curl -X POST http://0.0.0.0:8000/vote?user_id=2&match_id=2&score1=0&score2=1
curl -X POST http://0.0.0.0:8000/vote?user_id=3&match_id=1&score1=3&score2=1
curl -X POST http://0.0.0.0:8000/vote?user_id=3&match_id=2&score1=1&score2=2
curl -X POST http://0.0.0.0:8000/vote?user_id=4&match_id=1&score1=3&score2=1
curl -X POST http://0.0.0.0:8000/vote?user_id=4&match_id=2&score1=0&score2=2
curl -X POST http://0.0.0.0:8000/vote?user_id=5&match_id=1&score1=2&score2=1
curl -X POST http://0.0.0.0:8000/vote?user_id=5&match_id=2&score1=1&score2=3
curl -X POST http://0.0.0.0:8000/vote?user_id=6&match_id=1&score1=1&score2=0
curl -X POST http://0.0.0.0:8000/vote?user_id=6&match_id=2&score1=1&score2=2

curl -X POST http://0.0.0.0:8000/add_match_result?match_id=1&score1=1&score2=0
curl -X POST http://0.0.0.0:8000/add_match_result?match_id=2&score1=1&score2=3

curl -X POST http://0.0.0.0:8000/vote?user_id=1&match_id=3&score1=0&score2=1
curl -X POST http://0.0.0.0:8000/vote?user_id=1&match_id=4&score1=0&score2=3
curl -X POST http://0.0.0.0:8000/vote?user_id=2&match_id=3&score1=1&score2=0
curl -X POST http://0.0.0.0:8000/vote?user_id=2&match_id=4&score1=0&score2=1
curl -X POST http://0.0.0.0:8000/vote?user_id=3&match_id=3&score1=1&score2=1
curl -X POST http://0.0.0.0:8000/vote?user_id=3&match_id=4&score1=1&score2=3
curl -X POST http://0.0.0.0:8000/vote?user_id=4&match_id=3&score1=1&score2=1
curl -X POST http://0.0.0.0:8000/vote?user_id=4&match_id=4&score1=1&score2=3
curl -X POST http://0.0.0.0:8000/vote?user_id=5&match_id=3&score1=2&score2=2
curl -X POST http://0.0.0.0:8000/vote?user_id=5&match_id=4&score1=1&score2=3
curl -X POST http://0.0.0.0:8000/vote?user_id=6&match_id=3&score1=1&score2=1
curl -X POST http://0.0.0.0:8000/vote?user_id=6&match_id=4&score1=0&score2=2

curl -X POST http://0.0.0.0:8000/add_match_result?match_id=3&score1=1&score2=3
curl -X POST http://0.0.0.0:8000/add_match_result?match_id=4&score1=1&score2=0

curl -X POST http://0.0.0.0:8000/add_match?competition_id=1&name=real_chelsea
curl -X POST http://0.0.0.0:8000/add_match?competition_id=1&name=bayern_villarreal

curl -X POST http://0.0.0.0:8000/vote?user_id=1&match_id=5&score1=1&score2=0
curl -X POST http://0.0.0.0:8000/vote?user_id=1&match_id=6&score1=3&score2=0
curl -X POST http://0.0.0.0:8000/vote?user_id=2&match_id=5&score1=1&score2=0
curl -X POST http://0.0.0.0:8000/vote?user_id=2&match_id=6&score1=2&score2=0
#curl -X POST http://0.0.0.0:8000/vote?user_id=3&match_id=5&score1=1&score2=1
#curl -X POST http://0.0.0.0:8000/vote?user_id=3&match_id=6&score1=1&score2=3
curl -X POST http://0.0.0.0:8000/vote?user_id=4&match_id=5&score1=1&score2=2
curl -X POST http://0.0.0.0:8000/vote?user_id=4&match_id=6&score1=2&score2=1
#curl -X POST http://0.0.0.0:8000/vote?user_id=5&match_id=5&score1=2&score2=2
#curl -X POST http://0.0.0.0:8000/vote?user_id=5&match_id=6&score1=1&score2=3
#curl -X POST http://0.0.0.0:8000/vote?user_id=6&match_id=5&score1=1&score2=1
#curl -X POST http://0.0.0.0:8000/vote?user_id=6&match_id=6&score1=0&score2=2