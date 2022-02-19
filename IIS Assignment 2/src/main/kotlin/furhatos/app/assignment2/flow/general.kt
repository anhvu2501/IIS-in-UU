package furhatos.app.assignment2.flow

import furhatos.flow.kotlin.*
import furhatos.util.*

val Idle: State = state {

    init {
        furhat.setVoice(Language.ENGLISH_US, Gender.MALE)
        if (users.count > 0) {
            furhat.attend(users.random)
            goto(Start)
        }
    }

    onEntry {
        furhat.attendNobody()
    }

    onUserEnter () {
        furhat.attend(it)
        goto(Start)
    }

    onUserLeave (instant = true) {
        furhat.attend(users.other)
        goto(Start)
    }
}

val Interaction: State = state {

    onUserLeave() {
        if (users.count > 0) {
            if (it == users.current) {
                furhat.attend(users.other)
                goto(Start)
            } else {
                furhat.glance(it)
            }
        } else {
            goto(Idle)
        }
    }

    onUserEnter() {
        furhat.glance(users.other)
        furhat.say("I am taking care of another customer. Could you please wait me for a moment?")
        reentry()
    }

}