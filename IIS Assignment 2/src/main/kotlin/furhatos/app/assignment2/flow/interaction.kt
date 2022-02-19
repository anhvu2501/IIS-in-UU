package furhatos.app.assignment2.flow

import furhatos.app.assignment2.nlu.*
import furhatos.nlu.common.*
import furhatos.flow.kotlin.*
import furhatos.gestures.Gestures

val Start = state(Interaction) {

    onEntry {
        random({ furhat.ask("Hello, and welcome to Roboworld Airlines. How can I help you?") }, { furhat.ask("Hi, Welcome to our Airline desk. How can I help you?") })
        furhat.gesture(Gestures.Smile(duration = 2.0, strength = 1.0))
    }

    onResponse<BookFlight> {
        furhat.say("${it.intent.flight}, OK. Let me see what we have available.")
        furhat.ask("Where do you want to travel to?")
    }

    onResponse<No> {
        furhat.ask("How can I help you then?")
    }

    onResponse<RequestOptions> {
        furhat.say("We have ${Destination().optionsToText()}")
        furhat.ask("Which one do you prefer?")
    }

    onResponse<SelectDestination> {
        furhat.say("${it.intent.destination}, excellent!")
        furhat.ask("Do you want to add checked baggage?")
    }
    onResponse<AddBag> {
        val bags = it.intent.bags
        if (bags != null) {
            goto(orderReceived(bags))
        } else {
            propagate()
        }
        furhat.ask("Anything else?")
    }
}

fun orderReceived(bags: BagList): State = state {
    onEntry {
        furhat.say("Ok, I will add a ${bags.text} kg bag to your reservation")
        bags.list.forEach {
            users.current.order.bags.list.add(it)
        }
        furhat.ask("Anything else?")
    }
    onReentry {
        furhat.ask("Do you want something else?")
    }
    onResponse<SelectOtherOptions> {
        furhat.say("Excellent. I will add ${it.intent.options}")
        furhat.say("Okay, you will receive an email with the details of your reservation. " +
                "You have booked a flight ticket with a ${users.current.order.bags} kg bag and ${it.intent.options} option. Have a nice day! " + "Thank you for choosing us!!")
        goto(Idle)
    }
    onResponse<No> {
        furhat.say("Okay, you will receive an email with the details of your reservation. " +
                "You have booked a flight ticket with a ${users.current.order.bags} kg bag. Have a nice day! " + "Thank you for choosing us!!")
        goto(Idle)
    }
}
