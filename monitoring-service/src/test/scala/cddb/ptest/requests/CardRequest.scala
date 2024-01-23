package cddb.ptest.requests

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import cddb.ptest.config.ApiUrlConfig

object CardRequest {
  private val contentTypeHeader = Map(
    "Content-Type" -> "application/json;charset=UTF-8",
    "Authorization" -> "Bearer ${authToken}"
    )
  val baseUrl = ApiUrlConfig.cardApiUrl

  val searchSwamp = http("Search Swamp Cards")
    .get(s"$baseUrl/api/cards")
    .queryParam("q", "swamp")

  val getCardByOracleId = http("Get Card with Oracle_id")
    .get(s"$baseUrl/api/cards/{oracle_id}")

  val getCardByOracleIdAndPrintId = http("Get Card with Oracle_id and Print_id")
    .get(s"$baseUrl/api/cards/{oracle_id}/{print_id}")

}