package cddb.ptest.simulations

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import io.gatling.jdbc.Predef._

import cddb.ptest.scenarios.Scenarios._


class AllSimulations extends Simulation {

  val levelDuration = System.getProperty("levelDuration", "1").toInt seconds
  val rampDuration = System.getProperty("rampDuration", "2").toInt seconds
  val userIncrease = System.getProperty("userIncrease", "0").toDouble
  val levels = System.getProperty("levels", "1").toInt
  val startingRate = System.getProperty("startingRate", "1").toDouble

  val pauseDuration = 1

  val users = incrementUsersPerSec(userIncrease)
               .times(levels)
               .eachLevelLasting(levelDuration)
               .separatedByRampsLasting(rampDuration)
               .startingFrom(startingRate)

  setUp(
    registerLoginCollectionDeckAndCardsScenario.inject(users)//,
    // existingUserScenario.inject(users)
  )
}