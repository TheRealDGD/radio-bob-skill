Feature: play-default
    Scenario: play default stream de-de
        Given a german speaking user
         When the user says "spiele rock"
         Then "radio-bob-skill" should reply with dialog from "bob.radio.dialog"

    Scenario: play named stream de-de
        Given a german speaking user
         When the user says "spiele acdc"
         Then "radio-bob-skill" should reply with dialog from "bob.radio.dialog"         
         
    Scenario: play default stream en-us
        Given an english speaking user
         When the user says "play rock"
         Then "radio-bob-skill" should reply with dialog from "bob.radio.dialog"         

    Scenario: play default stream en-us
        Given an english speaking user
         When the user says "play acdc"
         Then "radio-bob-skill" should reply with dialog from "bob.radio.dialog"         

