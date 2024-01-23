package cddb.ptest.utils

import com.amazonaws.services.cognitoidp.AWSCognitoIdentityProvider
import com.amazonaws.services.cognitoidp.AWSCognitoIdentityProviderClientBuilder
import com.amazonaws.services.cognitoidp.model.AdminConfirmSignUpRequest

import cddb.ptest.utils.SSMParameterStore.retrieveParameterValue

object ConfirmUser {
  private val cognitoClient: AWSCognitoIdentityProvider = AWSCognitoIdentityProviderClientBuilder.defaultClient()
  
  val stage: String = System.getProperty("Stage", "development")
  // val userPool: String = retrieveParameterValue(s"/$stage/Cognito/UserPoolId")

  def adminConfirmUser(username: String) = {
    val confirmRequest = new AdminConfirmSignUpRequest()
      .withUsername(username)
      .withUserPoolId("us-east-1_xL2nw1K58")

    cognitoClient.adminConfirmSignUp(confirmRequest)
  }
}