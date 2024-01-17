package cddb.ptest.config

import io.gatling.core.Predef._
import io.gatling.http.Predef._

object UrlConfig {

  val userApiUrl: String = "${UserApiUrl}"
  val wishlistApiUrl: String = "${WishlistApiUrl}"
  val cardApiUrl: String = "${CardApiUrl}"
  val collectionApiUrl: String = "${CollectionApiUrl}"
  val deckApiUrl: String = "${DeckApiUrl}"

}