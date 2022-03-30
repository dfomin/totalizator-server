package com.dfomin.totalizator.models

import kotlinx.serialization.Serializable

@Serializable
data class Vote(val matchId: Int, val prediction: Pair<Int, Int>)
