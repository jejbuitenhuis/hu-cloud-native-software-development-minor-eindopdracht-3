package cddb.ptest.utils

import com.amazonaws.services.dynamodbv2.AmazonDynamoDB
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClientBuilder
import com.amazonaws.services.dynamodbv2.model.AttributeValue
import com.amazonaws.services.dynamodbv2.model.PutItemRequest
import java.util
import scala.io.Source
import com.fasterxml.jackson.databind.ObjectMapper

object AddCardsToDB {
  val dynamoDBClient: AmazonDynamoDB = AmazonDynamoDBClientBuilder.standard().withRegion("us-east-1").build()
  val objectMapper = new ObjectMapper()
  val stage: String = System.getProperty("Stage", "development")

  def cardExistsInTable(pk: String, sk: String, tableName: String): Boolean = {
    val key = new util.HashMap[String, AttributeValue]()
    key.put("PK", new AttributeValue(pk))
    key.put("SK", new AttributeValue(sk))

    val getItemRequest = new GetItemRequest()
      .withTableName(tableName)
      .withKey(key)

    val result: GetItemResult = dynamoDBClient.getItem(getItemRequest)
    !result.getItem.isEmpty
  }

  def addCardsFromJsonToTable(): Unit = {
    val filePath = "src/test/resources/bodies/setup-cards.json"
    val jsonContent = Source.fromFile(filePath).mkString
    val tableName = s"$stage-mtg-card-db"    
  
    val cards = objectMapper.readValue(jsonContent, classOf[List[Map[String, Any]]])

    cards.foreach { card =>
      val pk = card("PK").toString
      val sk = card("SK").toString

      if (!cardExistsInTable(pk, sk, tableName)) {
        val cardAttributes = new util.HashMap[String, AttributeValue]()

        val putItemRequest = new PutItemRequest()
          .withTableName(tableName)
          .withItem(cardAttributes)

        dynamoDBClient.putItem(putItemRequest)
      }
    }
  }
}