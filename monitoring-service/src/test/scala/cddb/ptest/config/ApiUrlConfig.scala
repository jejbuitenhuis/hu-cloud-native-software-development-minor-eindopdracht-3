package cddb.ptest.config

import cddb.ptest.utils.SSMParameterStore.retrieveParameterValue

object ApiUrlConfig {
  val stage: String = System.getProperty("Stage", "development")

  val userApiUrl: String = retrieveParameterValue(s"/$stage/MTGUserApi/url")
  val wishlistApiUrl: String = retrieveParameterValue(s"/$stage/MTGWishlistApi/url")
  val cardApiUrl: String = retrieveParameterValue(s"/$stage/MTGCardApi/url")
  val collectionApiUrl: String = retrieveParameterValue(s"/$stage/MTGCollectionApi/url")
  val deckApiUrl: String = retrieveParameterValue(s"/$stage/MTGDeckApi/url")

}