package furhatos.app.assignment2.nlu

import furhatos.nlu.ComplexEnumEntity
import furhatos.nlu.EnumEntity
import furhatos.nlu.Intent
import furhatos.nlu.ListEntity
import furhatos.util.Language

class RequestOptions : Intent() {
    override fun getExamples(lang: Language): List<String> {
        return listOf("What options do we have?")
    }
}

class Flight : EnumEntity(stemming = true, speechRecPhrases = true) {
    override fun getEnum(lang: Language): List<String> {
        return listOf("trip", "flight", "travel", "ticket", "hello")
    }
}

class BookFlight(var flight: Flight? = null) : Intent() {
    override fun getExamples(lang: Language): List<String> {
        return listOf("@flight", "I want to book a ticket", "I want to travel to @flight", "I want to buy a @flight")
    }
}

class Destination : EnumEntity(stemming = true, speechRecPhrases = true) {
    override fun getEnum(lang: Language): List<String> {
        return listOf("Stockholm", "Paris", "Rome", "Madrid", "Germany")
    }
}

class SelectDestination(val destination: Destination? = null) : Intent() {
    override fun getExamples(lang: Language): List<String> {
        return listOf("@destination", "I want to visit @destination", "I would like to go to Lisbon", "I want to travel to @destination")
    }
}

class OtherOptions : EnumEntity(stemming = true, speechRecPhrases = true) {
    override fun getEnum(lang: Language): List<String> {
        return listOf("Business Class", "Premium Economy", "Insurance")
    }
}

class SelectOtherOptions(val options: OtherOptions? = null) : Intent() {
    override fun getExamples(lang: Language): List<String> {
        return listOf("@options")
    }
}

// Add different Suitcases intent
class Bag : EnumEntity(stemming = true, speechRecPhrases = true) {
    override fun getEnum(lang: Language): List<String> {
        return listOf("12", "8", "23", "20", "10")
    }
}
class AddBag(var bags: BagList? = null) : Intent() {
    override fun getExamples(lang: Language): List<String> {
        return listOf("@bags", "just a suitcase", "I want to travel with @bags", "please add @bags")
    }
}
// More than one option
class BagList : ListEntity<QuantifiedBag>()

class QuantifiedBag(
    val count : furhatos.nlu.common.Number? = furhatos.nlu.common.Number(1),
    val bag: Bag? = null) : ComplexEnumEntity() {

    override fun getEnum(lang: Language): List<String> {
        return listOf("@count @bag", "@bag")
    }

    override fun toText(): String {
        return generate("$count $bag")
    }
}
