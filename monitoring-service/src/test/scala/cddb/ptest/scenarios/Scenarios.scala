package cddb.ptest.scenarios

import scala.concurrent.duration._
import scala.util.Random

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import cddb.ptest.requests.RegisterRequest

object Scenarios {

  private val credentialsFeeder = Iterator.continually({
    val randomString = Random.alphanumeric.take(8).mkString
      Map("password" -> randomString, "email" -> (s"p-test@$randomString.com"))
  })

  val registerScenario = scenario("Register user")
    .feed(credentialsFeeder)
    .exec(RegisterRequest.register.check(status.is(201)))
}