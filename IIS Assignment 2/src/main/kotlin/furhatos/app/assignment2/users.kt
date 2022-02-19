package furhatos.app.assignment2.flow

// script: users.kt
import furhatos.app.assignment2.nlu.BagList
import furhatos.records.User

/* Storing a user's order on the user object
* We define a Kotlin data class OrderData with a variable
* 'bags' of type BagList*/
class OrderData (
    var bags : BagList = BagList()
)
/* We add an extension variable 'order' to the User model of type OrderData*/
val User.order : OrderData
    get() = data.getOrPut(OrderData::class.qualifiedName, OrderData())