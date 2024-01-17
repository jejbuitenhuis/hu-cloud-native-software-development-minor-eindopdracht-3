package cddb.ptest.config

import io.gatling.core.Predef._
import io.gatling.http.Predef._


import com.typesafe.config.ConfigFactory

object UrlConfig {
  private val ssmClient: SsmClient = SsmClient.create()

  val stage: String = ConfigFactory.load().getString("Stage")

  val userApiUrl: String = retrieveParameterValue(s"/$stage/MTGUserApi/url")
  val wishlistApiUrl: String = retrieveParameterValue(s"/$stage/MTGWishlistApi/url")
  val cardApiUrl: String = retrieveParameterValue(s"/$stage/MTGCardApi/url")
  val collectionApiUrl: String = retrieveParameterValue(s"/$stage/MTGCollectionApi/url")
  val deckApiUrl: String = retrieveParameterValue(s"/$stage/MTGDeckApi/url")

  private def retrieveParameterValue(parameterName: String): String = {
    val request = GetParameterRequest.builder()
      .name(parameterName)
      .build()

    val response = ssmClient.getParameter(request)
    response.parameter().value()
  }
}