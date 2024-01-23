package cddb.ptest.requests

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._

object DeckRequest {
  private val contentTypeHeader = Map(
    "Content-Type" -> "application/json;charset=UTF-8",
    "Authorization" -> "Bearer #{authToken}"
    )

  val getDecksFromUser = http("Get decks from user")
    .get("/api/decks")
    .headers(contentTypeHeader)

  val createDeck = http("Create deck")
    .post("/api/decks")
    .headers(contentTypeHeader)
    .body(StringBody("""{ "name": "${deckname}" }""")).asJson

  val addCardToDeck = http("Add card to deck")
    .post("/api/decks/{deck_id}/cards")
    .headers(contentTypeHeader)
    .body(StringBody("""{ "oracle_id": "#{oracle_id}", "card_instance_id": #{card_instance_id}, "card_location": "MAIN_DECK" }""")).asJson

  val getAllCardsFromDeck = http("Get all cards from deck")
    .get("/api/decks/{deck_id}/cards")
    .headers(contentTypeHeader)
}