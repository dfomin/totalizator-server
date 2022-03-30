package com.dfomin.totalizator.models

import kotlinx.serialization.Serializable

@Serializable
data class CompetitionUser(val user: User, val votes: MutableList<Vote>)
