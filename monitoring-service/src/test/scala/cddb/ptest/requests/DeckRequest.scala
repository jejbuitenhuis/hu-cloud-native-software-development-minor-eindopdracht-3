package cddb.ptest.requests

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._

object DeckRequest {

  val getDecksFromUser = http("Get decks from user")
    .get("/api/decks")

  val createDeck = http("Create deck")
    .post("/api/decks")
    .body(StringBody("""{ "name": "${deckname}" }""")).asJson

  val addCardToDeck = http("Add card to deck")
    .post("/api/decks/{deck_id}/cards")

  val getAllCardsFromDeck = http("Get all cards from deck")
    .get("/api/decks/{deck_id}/cards")
}