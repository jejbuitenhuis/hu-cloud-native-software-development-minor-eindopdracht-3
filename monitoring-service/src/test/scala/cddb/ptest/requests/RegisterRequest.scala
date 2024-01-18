package cddb.ptest.requests

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._

object RegisterRequest {
  private val contentTypeHeader = Map("Content-Type" -> "application/json;charset=UTF-8")

  val register = http("register user")
    .post("/api/users")
    .headers(contentTypeHeader)
    .body(StringBody("""{ "password": "${password}", "email": "${email}" }""")).asJson
}