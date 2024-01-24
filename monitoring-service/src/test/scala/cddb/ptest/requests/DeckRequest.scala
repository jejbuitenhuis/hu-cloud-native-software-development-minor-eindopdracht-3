package cddb.ptest.requests

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import cddb.ptest.config.ApiUrlConfig

object DeckRequest {
  private val contentTypeHeader = Map(
    "Content-Type" -> "application/json;charset=UTF-8",
    "Authorization" -> "Bearer #{authToken}"
    )
  val baseUrl = ApiUrlConfig.deckApiUrl

  val getDecksFromUser = http("Get decks from user")
    .get(s"$baseUrl/api/decks")
    .headers(contentTypeHeader)

  val createDeck = http("Create deck")
    .post(s"$baseUrl/api/decks")
    .headers(contentTypeHeader)
    .body(StringBody("""{ "name": "#{deckname}" }""")).asJson

  val addCardToDeck = http("Add card to deck")
    .post(s"$baseUrl/api/decks/{deck_id}/cards")
    .headers(contentTypeHeader)
    .body(StringBody("""{ "oracle_id": "#{oracle_id}", "card_instance_id": "#{card_instance_id}", "card_location": "MAIN_DECK" }""")).asJson

  val getAllCardsFromDeck = http("Get all cards from deck")
    .get(s"$baseUrl/api/decks/{deck_id}/cards")
    .headers(contentTypeHeader)
}