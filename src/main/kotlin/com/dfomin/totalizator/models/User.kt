package com.dfomin.totalizator.models

import kotlinx.serialization.Serializable

@Serializable
data class User(val id: Int, val name: String)

val users = mutableListOf<User>()
