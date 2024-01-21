package cddb.ptest.scenarios

import scala.concurrent.duration._
import scala.util.Random

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import cddb.ptest.requests.UserRequest

object Scenarios {

  private val credentialsFeeder = Iterator.continually({
    val randomString = Random.alphanumeric.take(8).mkString
      Map("password" -> randomString, "email" -> (s"p-test@$randomString.com"))
  })

  private val existingUserFeeder = Iterator.continually(Map(
    "password" -> "existingPassword",
    "email" -> "existing@mail.com"
  ))


  val registerScenario = scenario("Register user")
    .feed(credentialsFeeder)
    .exec(UserRequest.register.check(status.is(201))
      .exec(session => {
        val email = session("email").as[String]
        val password = session("password").as[String]
        session.set("registeredEmail", email).set("registeredPassword", password)
      })
    )

  val loginScenario = scenario("Login with registered user")
    .exec(
      exec(session => {
        val email = session("registeredEmail").as[String]
        val password = session("registeredPassword").as[String]
        session
      })
    )
    .exec(UserRequest.login)

  val existingUserScenario = scenario("Register existing user")
    .feed(existingUserFeeder)
    .exec(
      exec(session => {
        if (!session.contains("registered")) {
          session.set("registered", true)
        } else {
          session
        }
      })
    )
    .exec(UserRequest.register.check(status.is(409)))

  
}