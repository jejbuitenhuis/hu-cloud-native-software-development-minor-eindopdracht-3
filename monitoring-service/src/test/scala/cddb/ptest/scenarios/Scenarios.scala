package cddb.ptest.scenarios

import scala.concurrent.duration._
import scala.util.Random

import cddb.ptest.requests.UserRequest
import cddb.ptest.requests.DeckRequest
import cddb.ptest.requests.CollectionRequest
import cddb.ptest.requests.CardRequest

import cddb.ptest.utils.ConfirmUser

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

  private val deckNameFeeder = Iterator.continually(Map(
    "deckname" -> Random.alphanumeric.take(8).mkString
  ))

  // Add Cards to DB on initial setup
  val addCardsScenario = scenario("Add Cards to DB on initial setup")
    .exec(addCardsFromJsonToTable())

  // Registration, Confirmation, Login, Collection, Deck and Cards Scenario
  val registerLoginCollectionDeckAndCardsScenario = scenario("Registration, Confirmation, Login, Collection, Deck and Cards Scenario")
    .feed(credentialsFeeder)

    // Register and confirm user
    .exec(UserRequest.register.check(status.is(201)))
    .exec(session => {
      val email = session("email").as[String]
      ConfirmUser.adminConfirmUser(email)
      session
    })

    // Login user and extrqact token
    .exec(UserRequest.login.check(status.is(200))
      .check(jsonPath("$.token").saveAs("authToken"))
      .exec(session => {
        val authToken = session("authToken").as[String]
        session.set("authToken", authToken)
      })
    )

    // Add to and get collection
    .during(5) {
      exec(CollectionRequest.addCardToCollection)
        .pause(5 millis)
    }
    .exec(CollectionRequest.getCollectionFromUser)

    // Create deck, add cards and get all deckcards
    .feed(deckNameFeeder)
    .exec(DeckRequest.createDeck(deckNameFeeder).check(status.is(201)))
    .during(5) {
      exec(DeckRequest.addCardToDeck.check(status.is(201)))
        .pause(5 millis)
    }
    .exec(DeckRequest.getAllCardsFromDeck.check(status.is(200)))

  // Register Existing User Scenario
  val existingUserScenario = scenario("Register Existing User")

    // Register existing users
    .feed(existingUserFeeder)
    .exec(
      exec(session => {
        if (!session.contains("registered")) {
          UserRequest.existingRegister.check(status.is(201))
          session.set("registered", true)
        } else {
          UserRequest.existingRegister.check(status.is(409))
          session
        }
      })
    )
}