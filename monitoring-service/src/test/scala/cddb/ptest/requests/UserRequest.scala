package cddb.ptest.requests

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import cddb.ptest.config.ApiUrlConfig

object UserRequest {
  private val contentTypeHeader = Map("Content-Type" -> "application/json;charset=UTF-8")
  val baseUrl = ApiUrlConfig.userApiUrl

  def createUserRequest(requestName: String) = {
    http(requestName)
      .post(s"$baseUrl/api/users")
      .headers(contentTypeHeader)
      .body(StringBody("""{ "password": "${password}", "email": "${email}" }""")).asJson
  }

  val register = createUserRequest("Register User")
  
  val existingRegister = createUserRequest("Existing Register User")

  val login = http("Login user")
    .post(s"$baseUrl/api/users/login")
    .headers(contentTypeHeader)
    .body(StringBody("""{ "password": "${password}", "email": "${email}" }""")).asJson
    .check(
      status.is(200),
      jsonPath("$.token").saveAs("authToken")
    )
}