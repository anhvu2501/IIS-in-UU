package furhatos.app.assignment2

import furhatos.app.assignment2.flow.*
import furhatos.skills.Skill
import furhatos.flow.kotlin.*

class Assignment2Skill : Skill() {
    override fun start() {
        /*Initial State Idle*/
        Flow().run(Idle)
    }
}

fun main(args: Array<String>) {
    Skill.main(args)
}
