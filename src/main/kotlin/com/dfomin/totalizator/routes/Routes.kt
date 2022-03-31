package com.dfomin.totalizator.routes

import com.dfomin.totalizator.models.*
import io.ktor.application.*
import io.ktor.http.*
import io.ktor.response.*
import io.ktor.routing.*


fun Route.competitionsRoute() {
    get("/competitions") {
        call.respond(competitions)
    }
}

fun Route.createCompetitionRoute() {
    post("/create_competition") {
        val name = call.parameters["name"] ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        if (name.isNotEmpty()) {
            val id = (competitions.lastOrNull()?.id ?: -1) + 1
            competitions.add(Competition(id, name, mutableListOf(), mutableListOf()))
            call.respondText("$id", status = HttpStatusCode.Created)
        } else {
            call.respondText("Competition $name was not created", status = HttpStatusCode.BadRequest)
        }
    }
}

fun Route.deleteCompetitionRoute() {
    delete("/delete_competition") {
        val id = call.parameters["id"]?.toInt() ?: return@delete call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        val result = competitions.removeIf { it.id == id }
        if (result) {
            call.respondText("$id was deleted", status = HttpStatusCode.Created)
        } else {
            call.respondText("Competition $id was not deleted", status = HttpStatusCode.BadRequest)
        }
    }
}

fun Route.usersRoute() {
    get("/users") {
        call.respond(users)
    }
}

fun Route.createUserRoute() {
    post("/create_user") {
        val name = call.parameters["name"] ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        if (name.isNotEmpty()) {
            val id = (users.lastOrNull()?.id ?: -1) + 1
            users.add(User(id, name))
            call.respondText("$id", status = HttpStatusCode.Created)
        } else {
            call.respondText("Competition $name was not created", status = HttpStatusCode.BadRequest)
        }
    }
}

fun Route.userJoinRoute() {
    post("/join") {
        val competitionId = call.parameters["competition_id"]?.toInt()
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        val userId = call.parameters["user_id"]?.toInt()
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        val competition = competitions.find { it.id == competitionId }
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        if (competition.users.count { it.user.id == userId } > 0) {
            return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        }
        val user = users.find { it.id == userId }
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        competition.users.add(CompetitionUser(user, mutableListOf()))
        call.respondText("User $userId joined the competition $competitionId", status = HttpStatusCode.OK)
    }
}

fun Route.matchesRoute() {
    get("/matches") {
        val competitionId = call.parameters["competition_id"]?.toInt()
            ?: return@get call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        val competition = competitions.find { it.id == competitionId }
            ?: return@get call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        call.respond(competition.matches.filter { it.result == null })
    }
}

fun Route.addMatchRoute() {
    post("/add_match") {
        val competitionId = call.parameters["competition_id"]?.toInt()
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        val competition = competitions.find { it.id == competitionId }
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        val name = call.parameters["name"] ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)

        val id = (competition.matches.lastOrNull()?.id ?: -1) + 1
        competition.matches.add(Match(id, name, null))
        call.respondText("OK", status = HttpStatusCode.Created)
    }
}

fun Route.addMatchResultRoute() {
    post("/add_match_result") {
        val competitionId = call.parameters["competition_id"]?.toInt()
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        val competition = competitions.find { it.id == competitionId }
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        val matchId = call.parameters["match_id"]?.toInt()
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        val score1 = call.parameters["score1"]?.toInt()
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        val score2 = call.parameters["score2"]?.toInt()
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)

        val match = competition.matches.find { it.id == matchId }
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        match.result = Pair(score1, score2)

        call.respondText("OK", status = HttpStatusCode.Created)
    }
}

fun Route.addVoteRoute() {
    post("/add_vote") {
        val competitionId = call.parameters["competition_id"]?.toInt()
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        val competition = competitions.find { it.id == competitionId }
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        val userId = call.parameters["user_id"]?.toInt()
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        val matchId = call.parameters["match_id"]?.toInt()
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        val score1 = call.parameters["score1"]?.toInt()
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        val score2 = call.parameters["score2"]?.toInt()
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)

        val competitionUser = competition.users.find { it.user.id == userId }
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        competitionUser.votes.add(Vote(matchId, Pair(score1, score2)))

        call.respondText("OK", status = HttpStatusCode.Created)
    }
}

fun Route.results() {
    get("/results") {
        val competitionId = call.parameters["competition_id"]?.toInt()
            ?: return@get call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        val competition = competitions.find { it.id == competitionId }
            ?: return@get call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        val userResults = mutableMapOf<Int, Int>()
        for (user in competition.users) {
            userResults[user.user.id] = 0
        }
        for (match in competition.matches) {
            val result = match.result ?: continue
            for (user in competition.users) {
                val vote = user.votes.find { it.matchId == match.id } ?: continue
                if (vote.prediction.first == result.first && vote.prediction.second == result.second) {
                    userResults[user.user.id] = (userResults[user.user.id] ?: 0) + 1
                }
            }
        }

        call.respond(userResults)
    }
}


fun Application.registerRoutes() {
    routing {
        competitionsRoute()
        createCompetitionRoute()
        deleteCompetitionRoute()

        usersRoute()
        createUserRoute()
        userJoinRoute()

        matchesRoute()
        addMatchRoute()
        addMatchResultRoute()

        addVoteRoute()
        results()
    }
}
