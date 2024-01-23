package cddb.ptest.requests

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._

object CardRequest {
  private val contentTypeHeader = Map(
    "Content-Type" -> "application/json;charset=UTF-8", "Authorization" -> "Bearer ${authToken}"
    )

  val searchSwamp = http("Search Swamp Cards")
    .get("/api/cards")
    .queryParam("q", "swamp")

  val getCardByOracleId = http("Get Card with Oracle_id")
    .get("/api/cards/{oracle_id}")

  val getCardByOracleIdAndPrintId = http("Get Card with Oracle_id and Print_id")
    .get("/api/cards/{oracle_id}/{print_id}")

  // val getCollectionFromUser = http("get collection from user")
  //   .get("/api/collections")
  //   .headers(contentTypeHeader)

  // val addCardToCollection = http("add card to collection")
  //   .post("/api/collections")
  //   .headers(contentTypeHeader)
  //   .body(StringBody("""{ "oracle_id": "${oracle_id}", "print_id": ${print_id}, "condition": "MINT" }""")).asJson

}