package cddb.ptest.simulations

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import io.gatling.jdbc.Predef._

import cddb.ptest.config.ApiUrlConfig.userApiUrl
import cddb.ptest.scenarios.Scenarios._

class AllSimulations extends Simulation {

  val levelDuration = System.getProperty("levelDuration", "2").toInt seconds
  val rampDuration = System.getProperty("rampDuration", "2").toInt seconds
  val userIncrease = System.getProperty("userIncrease", "1").toDouble
  val levels = System.getProperty("levels", "2").toInt
  val startingRate = System.getProperty("startingRate", "0").toDouble


  def httpProtocol = http.baseUrl(userApiUrl).userAgentHeader("Gatling/test")

  val users = incrementUsersPerSec(userIncrease)
               .times(levels)
               .eachLevelLasting(levelDuration)
               .separatedByRampsLasting(rampDuration)
               .startingFrom(startingRate)

  setUp(
    registerAndLoginScenario.inject(users),
    existingUserScenario.inject(users)
  ).protocols(httpProtocol)
}