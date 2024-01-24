package cddb.ptest.scenarios

import scala.concurrent.duration._
import scala.util.Random

import cddb.ptest.requests.UserRequest
import cddb.ptest.requests.DeckRequest
import cddb.ptest.requests.CollectionRequest
import cddb.ptest.requests.CardRequest

import cddb.ptest.utils.ConfirmUser

import io.gatling.core.feeder.Feeder
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

  private val cardFeeder = jsonFile("src/test/resources/bodies/cards.json").shuffle

  private val addCardsScenario = repeat(5) {
    feed(cardFeeder)
      .exec(CollectionRequest.addCardToCollection.check(status.is(201)))
      .exec(session => {
        println("addCard Session::: " + session)
        session
      })
      .pause(50 millis)
  }

  private val deckNameFeeder = Iterator.continually(Map(
    "deckname" -> Random.alphanumeric.take(8).mkString
  ))

  // Registration, Confirmation, Login, Collection, Deck and Cards Scenario
  val registerLoginCollectionDeckAndCardsScenario = scenario("Registration, Confirmation, Login, Collection, Deck and Cards Scenario")
    .feed(credentialsFeeder)

    // Register and confirm user
    .exec(UserRequest.register.check(status.is(201)))
    .pause(50 millis)
    .exec(session => {
      val email = session("email").as[String]
      ConfirmUser.adminConfirmUser(email)
      session
    })
    .pause(50 millis)

    // Login user and extract token
    .exec(UserRequest.login)
    .pause(1 second)
    .exec(session => {
      println("Login Session::: " + session)
      session
    })

    // Add to and get collection
    .exec(addCardsScenario)

  //   // Create deck, add cards and get all deckcards
  //   .feed(deckNameFeeder)
  //   .exec(DeckRequest.createDeck.check(status.is(201)))
  //   .during(5) {
  //     exec(DeckRequest.addCardToDeck.check(status.is(201)))
  //       .pause(5 millis)
  //   }
  //   .exec(DeckRequest.getAllCardsFromDeck.check(status.is(200)))

  // // Register Existing User Scenario
  // val existingUserScenario = scenario("Register Existing User")

  //   // Register existing users
  //   .feed(existingUserFeeder)
  //   .exec(
  //     exec(session => {
  //       if (!session.contains("registered")) {
  //         UserRequest.existingRegister.check(status.is(201))
  //         session.set("registered", true)
  //       } else {
  //         UserRequest.existingRegister.check(status.is(409))
  //         session
  //       }
  //     })
  //   )
}