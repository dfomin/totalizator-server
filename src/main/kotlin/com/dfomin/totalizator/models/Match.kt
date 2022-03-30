package com.dfomin.totalizator.models

import kotlinx.serialization.Serializable

@Serializable
data class Match(val name: String, val result: Pair<Int, Int>?)
