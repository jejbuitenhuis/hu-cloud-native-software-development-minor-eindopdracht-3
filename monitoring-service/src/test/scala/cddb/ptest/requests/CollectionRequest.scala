package cddb.ptest.requests

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._

object CollectionRequest {
  private val contentTypeHeader = Map(
    "Content-Type" -> "application/json;charset=UTF-8",
    "Authorization" -> "Bearer #{authToken}"
    )

  val getCollectionFromUser = http("Get Collection from User")
    .get("/api/collections")
    .headers(contentTypeHeader)

  val addCardToCollection = http("Add Card to Collection")
    .post("/api/collections")
    .headers(contentTypeHeader)
    .body(StringBody("""{ "oracle_id": "#{oracle_id}", "print_id": #{print_id}, "condition": "MINT" }""")).asJson

}