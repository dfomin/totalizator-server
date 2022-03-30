package com.dfomin.totalizator.models

import kotlinx.serialization.Serializable

@Serializable
data class Competition(val id: Int, val name: String, val users: MutableList<User>, val matches: MutableList<Match>)

val competitions = mutableListOf<Competition>()
