from enum import Enum

class Service(Enum):
    PLACE = "place"
    REVIEW = "review"
    MANAGEMENT = "management"


SERVICE_URL = {

    Service.PLACE: "https://ta-bot-api-gateway.herokuapp.com/api/",
    Service.REVIEW: "https://ta-bot-api-gateway.herokuapp.com/api/",
    Service.MANAGEMENT: "https://ta-bot-api-gateway.herokuapp.com/api/",
    
}
