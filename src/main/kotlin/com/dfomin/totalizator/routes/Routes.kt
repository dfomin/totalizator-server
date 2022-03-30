package com.dfomin.totalizator.routes

import com.dfomin.totalizator.models.*
import io.ktor.application.*
import io.ktor.http.*
import io.ktor.request.*
import io.ktor.response.*
import io.ktor.routing.*
import kotlinx.serialization.json.*


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
        if (competition.users.count { it.id == userId } > 0) {
            return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        }
        val user = users.find { it.id == userId }
            ?: return@post call.respondText("Bad Request", status = HttpStatusCode.BadRequest)
        competition.users.add(user)
        call.respondText("User $userId joined the competition $competitionId", status = HttpStatusCode.OK)
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
    }
}
