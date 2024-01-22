package cddb.ptest.config

import com.amazonaws.services.cognitoidp.AWSCognitoIdentityProvider
import com.amazonaws.services.cognitoidp.AWSCognitoIdentityProviderClientBuilder
import com.amazonaws.services.cognitoidp.model.AdminConfirmSignUpRequest

import cddb.ptest.config.SSMParameterStore.retrieveParameterValue

object ConfirmUser {
  private val cognitoClient: AWSCognitoIdentityProvider = AWSCognitoIdentityProviderClientBuilder.defaultClient()
  
  val stage: String = System.getProperty("Stage", "development")
  val userPool: String = retrieveParameterValue(s"/$stage/Cognito/UserPoolId")

  def adminConfirmUser(username: String) = {
    val confirmRequest = new AdminConfirmSignUpRequest()
      .withUsername(username)
      .withUserPoolId("userPool")

    cognitoClient.adminConfirmSignUp(confirmRequest)
  }
}