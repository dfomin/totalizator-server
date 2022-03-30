package com.dfomin.totalizator.models

import kotlinx.serialization.Serializable

@Serializable
data class Match(val id: Int, val name: String, var result: Pair<Int, Int>?)
