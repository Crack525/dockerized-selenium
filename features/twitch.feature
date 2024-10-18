Feature: Twitch Search Feature

Scenario: User searches for a streamer
  Given the user is on the Twitch mobile website
  Then the user click on search icon
  Then the user enters StarCraft II
  Then the user scrolls 2 times
  Then the user selects starcraft ii - stream
  Then on the streamer page wait until all is load  
