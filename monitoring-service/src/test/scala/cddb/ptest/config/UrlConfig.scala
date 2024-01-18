package cddb.ptest.config

import io.gatling.core.Predef._
import io.gatling.http.Predef._

import software.amazon.awssdk.services.ssm.SsmClient
import software.amazon.awssdk.services.ssm.model.GetParameterRequest

object UrlConfig {
  private val ssmClient: SsmClient = SsmClient.create()

  val stage: String = System.getProperty("Stage", "development")

  val userApiUrl: String = retrieveParameterValue(s"/$stage/MTGUserApi/url")
  val wishlistApiUrl: String = retrieveParameterValue(s"/$stage/MTGWishlistApi/url")
  val cardApiUrl: String = retrieveParameterValue(s"/$stage/MTGCardApi/url")
  val collectionApiUrl: String = retrieveParameterValue(s"/$stage/MTGCollectionApi/url")
  val deckApiUrl: String = retrieveParameterValue(s"/$stage/MTGDeckApi/url")

  private def retrieveParameterValue(parameterName: String): String = {
    println(s"Retrieving parameter: $parameterName")
    val request = GetParameterRequest.builder()
      .name(parameterName)
      .build()

    try {
    val response = ssmClient.getParameter(request)
    response.parameter().value()
  } catch {
    case e: Exception =>
      println(s"Error retrieving parameter: $e")
      throw e
  }
  }
}