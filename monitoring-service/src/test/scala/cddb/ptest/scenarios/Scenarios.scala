package cddb.ptest.scenarios

import scala.concurrent.duration._
import scala.util.Random
import java.io.PrintWriter

import cddb.ptest.requests.UserRequest
import cddb.ptest.config.ConfirmUser

import io.gatling.core.Predef._
import io.gatling.http.Predef._

object Scenarios {

  private val credentialsFeeder = Iterator.continually({
    val randomString = Random.alphanumeric.take(8).mkString
      Map("password" -> randomString, "email" -> (s"p-test@$randomString.com"))
  })

  private val existingUserFeeder = Iterator.continually(Map(
    "password" -> "existingPassword",
    "email" -> "existing@mail.com"
  ))


  val registerAndLoginScenario = scenario("Combined Registration, confirmation and Login")
    .feed(credentialsFeeder)
    .exec(UserRequest.register.check(status.is(201)))
    .exec(session => {
      val email = session("email").as[String]
      ConfirmUser.adminConfirmUser(email)
      session
    })
    .exec(UserRequest.login.check(status.is(200)))

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