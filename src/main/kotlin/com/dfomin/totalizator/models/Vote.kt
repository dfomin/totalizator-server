package com.dfomin.totalizator.models

import kotlinx.serialization.Serializable

@Serializable
data class Vote(val user: User, val match: Match, val prediction: Pair<Int, Int>)
