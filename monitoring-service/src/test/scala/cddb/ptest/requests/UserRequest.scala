package cddb.ptest.requests

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._

object UserRequest {
  private val contentTypeHeader = Map("Content-Type" -> "application/json;charset=UTF-8")

  val register = http("register user")
    .post("/api/users")
    .headers(contentTypeHeader)
    .body(StringBody("""{ "password": "${password}", "email": "${email}" }""")).asJson

  val login = http("login user")
    .post("/api/users/login")
    .headers(contentTypeHeader)
    .body(StringBody("""{ "password": "${password}", "email": "${email}" }""")).asJson

  val adminConfirm

}